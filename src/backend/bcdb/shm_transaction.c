#include "postgres.h"
#include "bcdb/shm_transaction.h"
#include "bcdb/utils/aligned_heap.h"
#include "utils/elog.h"
#include "libpq-fe.h"
#include "storage/shmem.h"
#include "string.h"
#include "utils/memutils.h"
#include "utils/palloc.h"
#include "utils/relcache.h"
#include "nodes/pg_list.h"
#include "nodes/nodes.h"
#include "catalog/index.h"
#include "utils/rel.h"
#include <access/tableam.h>
#include <executor/executor.h>
#include <bcdb/worker.h>
#include "bcdb/bcdb_dsa.h"
#include "utils/hsearch.h"
#include <stddef.h>
#include <access/genam.h>
#include "access/xact.h"
#include "access/heapam.h"
#include "storage/bufmgr.h"
#include "storage/predicate.h"
#include "utils/hashutils.h"
#include "access/itup.h"
#include "utils/hsearch.h"
#include "bcdb/worker_controller.h"
#include "storage/spin.h"
#include "storage/predicate_internals.h"
#include <time.h>

BCDBShmXact  *activeTx;
HTAB         *tx_pool;
slock_t      *tx_pool_lock;
HTAB         *xid_map;
slock_t      *xid_map_lock;
TxQueue       *tx_queues;
WSTable       *ws_table;
WSTable       *rs_table;
WSTableRecord  ws_table_record;
WSTableRecord  rs_table_record;
extern HTAB   *PredicateLockTargetHash;
extern HTAB   *PredicateLockHash;

static TupleTableSlot* clone_slot(TupleTableSlot* slot);

#define WSTableGetPartitionIdx(hashcode) ((hashcode) % WRITE_CONFLICT_MAP_NUM_PARTITIONS)
#define WSTablePartitionLock(hashcode) (&(ws_table->map_locks[(hashcode) % WRITE_CONFLICT_MAP_NUM_PARTITIONS]))
#define RSTableGetPartitionIdx(hashcode) ((hashcode) % WRITE_CONFLICT_MAP_NUM_PARTITIONS)
#define RSTablePartitionLock(hashcode) (&(rs_table->map_locks[(hashcode) % WRITE_CONFLICT_MAP_NUM_PARTITIONS]))

uint32
dummy_hash(const void *key, Size key_size)
{
    return *(uint32*)key;
}

BCDBShmXact *
create_tx(char *hash, char *sql, BCTxID tx_id, BCBlockID snapshot_block, int isolation, bool pred_lock)
{
    BCDBShmXact *tx;
    bool found;
    Assert(tx_pool != NULL);
    SpinLockAcquire(tx_pool_lock);
    tx = hash_search(tx_pool, hash, HASH_ENTER, &found);
    if (found)
    {
        ereport(DEBUG3,
            (errmsg("[ZL] transaction (%s) exists", hash)));
        SpinLockRelease(tx_pool_lock);
        return NULL;
    }
    LWLockInitialize(&tx->lock, LWTRANCHE_TX);
    LWLockAcquire(&tx->lock, LW_EXCLUSIVE);
    SpinLockRelease(tx_pool_lock);

    strcpy(tx->hash, hash);
    strcpy(tx->sql, sql);
    tx->block_id_snapshot = snapshot_block;
    tx->block_id_committed = BCDBMaxBid;
    tx->tx_id = tx_id;
    tx->status = TX_SCHEDULING;
    tx->queryDesc = NULL;
    tx->portal = NULL;
    tx->sxact = NULL;
    tx->worker_pid = 0;
    tx->why_doomed[0] = '\0';
    tx->xid = InvalidTransactionId;
    tx->isolation = isolation;
    tx->pred_lock = pred_lock;
    tx->queue_link.tqe_prev = NULL;
    tx->create_time = 0;
    tx->has_raw = false;
    tx->has_war = false;
    SHA256_Init(&tx->state_hash);
    SIMPLEQ_INIT(&tx->optim_write_list);


    ConditionVariableInit(&tx->cond);
    LWLockRelease(&tx->lock);
    return tx;
}

void
compose_tx_hash(BCBlockID bid, BCTxID tx_id, char* out_hash)
{
    sprintf(out_hash, "%d_%d", bid, tx_id);
}

void
delete_tx(BCDBShmXact *tx)
{
    bool found;
    if (!tx)
        return;

    DEBUGNOCHECK("[ZL] deleting tx %s", tx->hash);
    remove_tx_xid_map(tx->xid);

    SpinLockAcquire(tx_pool_lock);
    hash_search(tx_pool, tx->hash, HASH_REMOVE, &found);
    SpinLockRelease(tx_pool_lock);
    if (found)
        DEBUGNOCHECK("[ZL] removed tx %s", tx->hash);
}

uint32
compose_tuple_hash(Oid relation_id, ItemPointer tid)
{
    return hash_uint32((uint32)relation_id) + hash_any((unsigned char*)tid, sizeof(ItemPointerData));
}

uint32
compose_index_hash(Oid relation_id, IndexTuple itup)
{
    return hash_uint32((uint32)relation_id) + 
           hash_any((unsigned char*)itup + IndexInfoFindDataOffset(itup->t_info),
                    IndexTupleSize(itup) - IndexInfoFindDataOffset(itup->t_info));
}

void
create_tx_pool(void)
{
    HASHCTL info;
    slock_t *tx_pool_lock_array;
    bool    found;
    tx_pool_lock_array = ShmemInitStruct("tx_pool_lock", sizeof(slock_t) * 2, &found);
    tx_pool_lock = tx_pool_lock_array;
    xid_map_lock = tx_pool_lock + 1;

    if (!found)
    {
        SpinLockInit(tx_pool_lock);
        SpinLockInit(xid_map_lock);
    }

    MemSet(&info, 0, sizeof(info));
	info.keysize = TX_HASH_SIZE;
	info.entrysize = sizeof(BCDBShmXact);
	info.hash = string_hash;
    tx_pool = ShmemInitHash("bcdb_tx_pool", 
                   MAX_SHM_TX,
                   MAX_SHM_TX,
                   &info, HASH_ELEM | HASH_FUNCTION | HASH_FIXED_SIZE);
    
    info.keysize = sizeof(TransactionId);
    info.entrysize = sizeof(XidMapEntry);
    info.hash = uint32_hash;
    xid_map = ShmemInitHash("bcdb_xid_map",
                   MAX_SHM_TX,
                   MAX_SHM_TX,
                   &info, HASH_ELEM | HASH_FUNCTION | HASH_FIXED_SIZE);

    tx_queues = ShmemInitStruct("bcdb_tx_queue", sizeof(TxQueue) * NUM_TX_QUEUE_PARTITION, &found);
    for (int i = 0; i < NUM_TX_QUEUE_PARTITION; i++)
    {
        TAILQ_INIT(&tx_queues[i].list);
        SpinLockInit(&tx_queues[i].lock);
        tx_queues[i].size = 0;
        ConditionVariableInit(&tx_queues[i].empty_cond);
        ConditionVariableInit(&tx_queues[i].full_cond);
    } 

    ws_table = ShmemInitStruct("bcdb_tx_ws_table", sizeof(WSTable), &found);
    if (!found)
    {
        info.keysize = sizeof(PREDICATELOCKTARGETTAG);
        info.entrysize = sizeof(WSTableEntry);
        info.hash = dummy_hash;
        info.num_partitions = WRITE_CONFLICT_MAP_NUM_PARTITIONS;
        ws_table->map = ShmemInitHash("bcdb_write_conflict_map",
                                     MAX_WRITE_CONFLICT,
                                     MAX_WRITE_CONFLICT,
                                     &info, HASH_ELEM | HASH_FUNCTION | HASH_FIXED_SIZE | HASH_PARTITION);
        for (int i=0; i < WRITE_CONFLICT_MAP_NUM_PARTITIONS; i++)
            SpinLockInit(&(ws_table->map_locks[i]));
    }

    rs_table = ShmemInitStruct("bcdb_tx_rs_table", sizeof(WSTable), &found);
    if (!found)
    {
        info.keysize = sizeof(PREDICATELOCKTARGETTAG);
        info.entrysize = sizeof(WSTableEntry);
        info.hash = dummy_hash;
        info.num_partitions = WRITE_CONFLICT_MAP_NUM_PARTITIONS;
        rs_table->map = ShmemInitHash("bcdb_read_conflict_map",
                                     MAX_WRITE_CONFLICT,
                                     MAX_WRITE_CONFLICT,
                                     &info, HASH_ELEM | HASH_FUNCTION | HASH_FIXED_SIZE | HASH_PARTITION);
        for (int i=0; i < WRITE_CONFLICT_MAP_NUM_PARTITIONS; i++)
            SpinLockInit(&(rs_table->map_locks[i]));
    }
}

Size
tx_pool_size(void)
{
    Size ret = hash_estimate_size(MAX_SHM_TX, sizeof(BCDBShmXact));
    ret = add_size(ret, hash_estimate_size(MAX_SHM_TX, sizeof(XidMapEntry)));
    ret = add_size(ret, sizeof(slock_t) * 2);
    ret = add_size(ret, sizeof(TxQueue) * NUM_TX_QUEUE_PARTITION);
    ret = add_size(ret, sizeof(WSTable));
    ret = add_size(ret, hash_estimate_size(MAX_WRITE_CONFLICT, sizeof(WSTableEntry)));
    return ret; 
}

void
clear_tx_pool(void)
{
    shm_hash_clear(tx_pool, MAX_SHM_TX);
    shm_hash_clear(xid_map, MAX_SHM_TX); 
    for (int i = 0; i < NUM_TX_QUEUE_PARTITION; i++)
        TAILQ_INIT(&tx_queues[i].list);
}

void
rs_table_reserve(const PREDICATELOCKTARGETTAG *tag)
{
    bool found;
    WSTableEntry* entry;
    uint32  tuple_hash = PredicateLockTargetTagHashCode(tag);
    slock_t *partition_lock = RSTablePartitionLock(tuple_hash);
    WSTableEntryRecord *record;

    SpinLockAcquire(partition_lock);
    entry = hash_search_with_hash_value(rs_table->map, tag, tuple_hash, HASH_ENTER, &found);
    if (!found)
    {
        entry->tx_id = activeTx->tx_id;
        DEBUGMSG("[ZL] tx %s reserving read %d success, because not found", activeTx->hash, tuple_hash);
    }
    else
    {
        if (entry->tx_id > activeTx->tx_id)
        {
            DEBUGMSG("[ZL] tx %s reserving read %d success, replacing %d", activeTx->hash, tuple_hash, entry->tx_id);
            entry->tx_id = activeTx->tx_id;
        }
    }

    if (entry->tx_id != activeTx->tx_id)
    {
        DEBUGMSG("[ZL] tx %s reserving read %d fail: winner %d", activeTx->hash, tuple_hash, entry->tx_id);
    }
    SpinLockRelease(partition_lock);

    record= MemoryContextAlloc(bcdb_tx_context, sizeof(WSTableEntryRecord));
    record->tag = *tag;
    LIST_INSERT_HEAD(&rs_table_record, record, link);
}

void
ws_table_reserve(PREDICATELOCKTARGETTAG *tag)
{
    bool found;
    WSTableEntry* entry;
    uint32  tuple_hash = PredicateLockTargetTagHashCode(tag);
    slock_t *partition_lock = WSTablePartitionLock(tuple_hash);
    WSTableEntryRecord *record;

    SpinLockAcquire(partition_lock);
    entry = hash_search_with_hash_value(ws_table->map, tag, tuple_hash, HASH_ENTER, &found);
    if (!found)
    {
        entry->tx_id = activeTx->tx_id;
        DEBUGMSG("[ZL] tx %s reserving write %d success, because not found", activeTx->hash, tuple_hash);
    }
    else
    {
        if (entry->tx_id > activeTx->tx_id)
        {
            DEBUGMSG("[ZL] tx %s reserving write %d success, replacing %d", activeTx->hash, tuple_hash, entry->tx_id);
            entry->tx_id = activeTx->tx_id;
        }
    }

    if (entry->tx_id != activeTx->tx_id)
    {
        DEBUGMSG("[ZL] tx %s reserving write %d fail: winner %d", activeTx->hash, tuple_hash, entry->tx_id);
    }
    SpinLockRelease(partition_lock);

    record= MemoryContextAlloc(bcdb_tx_context, sizeof(WSTableEntryRecord));
    record->tag = *tag;
    LIST_INSERT_HEAD(&ws_table_record, record, link);
}

bool
ws_table_check(PREDICATELOCKTARGETTAG *tag)
{
    bool found;
    WSTableEntry* entry;
    uint32  tuple_hash = PredicateLockTargetTagHashCode(tag);
    slock_t *partition_lock = WSTablePartitionLock(tuple_hash);

    SpinLockAcquire(partition_lock);
    entry = hash_search_with_hash_value(ws_table->map, tag, tuple_hash, HASH_FIND, &found);
    if (found && entry->tx_id < activeTx->tx_id)
    {
        DEBUGMSG("[ZL] tx %s check write %d failed, winner: %d", activeTx->hash, tuple_hash, entry->tx_id);
        SpinLockRelease(partition_lock);
        return true;
    }
    DEBUGMSG("[ZL] tx %s check write %d win", activeTx->hash, tuple_hash);
    SpinLockRelease(partition_lock);
    return false;
}

bool
rs_table_check(PREDICATELOCKTARGETTAG *tag)
{
    bool found;
    WSTableEntry* entry;
    uint32  tuple_hash = PredicateLockTargetTagHashCode(tag);
    slock_t *partition_lock = RSTablePartitionLock(tuple_hash);

    SpinLockAcquire(partition_lock);
    entry = hash_search_with_hash_value(rs_table->map, tag, tuple_hash, HASH_FIND, &found);
    if (found && entry->tx_id < activeTx->tx_id)
    {
        DEBUGMSG("[ZL] tx %s check read %d failed, winner: %d", activeTx->hash, tuple_hash, entry->tx_id);
        SpinLockRelease(partition_lock);
        return true;
    }
    DEBUGMSG("[ZL] tx %s check read %d win", activeTx->hash, tuple_hash);
    SpinLockRelease(partition_lock);
    return false;
}

void
clean_ws_table_record(void)
{
    WSTableEntryRecord *record;
    while ((record = LIST_FIRST(&ws_table_record)))
    {
        bool found;
        WSTableEntry* entry;
        uint32  tuple_hash = PredicateLockTargetTagHashCode(&record->tag);
        slock_t *partition_lock = WSTablePartitionLock(tuple_hash);

        SpinLockAcquire(partition_lock);
        entry = hash_search_with_hash_value(ws_table->map, &record->tag, tuple_hash, HASH_FIND, &found);
        if (found)
        {
            if (entry->tx_id == activeTx->tx_id)
            {
                DEBUGMSG("[ZL] tx %s deleting write entry %d", activeTx->hash, tuple_hash);
                hash_search_with_hash_value(ws_table->map, &record->tag, tuple_hash, HASH_REMOVE, &found);
            }
        }
        SpinLockRelease(partition_lock);
        LIST_REMOVE(record, link);
    }
}

void
clean_rs_table_record(void)
{
    WSTableEntryRecord *record;
    while ((record = LIST_FIRST(&rs_table_record)))
    {
        bool found;
        WSTableEntry* entry;
        uint32  tuple_hash = PredicateLockTargetTagHashCode(&record->tag);
        slock_t *partition_lock = RSTablePartitionLock(tuple_hash);

        SpinLockAcquire(partition_lock);
        entry = hash_search_with_hash_value(rs_table->map, &record->tag, tuple_hash, HASH_FIND, &found);
        if (found)
        {
            if (entry->tx_id == activeTx->tx_id)
            {
                DEBUGMSG("[ZL] tx %s deleting read entry %d", activeTx->hash, tuple_hash);
                hash_search_with_hash_value(rs_table->map, &record->tag, tuple_hash, HASH_REMOVE, &found);
            }
        }
        SpinLockRelease(partition_lock);
        LIST_REMOVE(record, link);
    }
}
void
tx_queue_insert(BCDBShmXact *tx, int32 partition)
{
    int num_queue = OEP_mode ? blocksize * 2 : blocksize;
    TxQueue *queue = tx_queues + (partition % num_queue);
    ConditionVariablePrepareToSleep(&queue->full_cond);
    SpinLockAcquire(&queue->lock);
    while (queue->size > QUEUEING_BLOCKS)
    {
        SpinLockRelease(&queue->lock);
        ConditionVariableSleep(&queue->full_cond, WAIT_EVENT_BLOCK_COMMIT);
        SpinLockAcquire(&queue->lock);
    }
    ConditionVariableCancelSleep();
    TAILQ_INSERT_TAIL(&queue->list, tx, queue_link);
    tx->queue_partition = partition;
    queue->size += 1;
    SpinLockRelease(&queue->lock);
    ConditionVariableSignal(&queue->empty_cond);
}

BCDBShmXact*
tx_queue_next(int32 partition)
{
    BCDBShmXact *tx;
    int num_queue = OEP_mode ? blocksize * 2 : blocksize;
    TxQueue *queue = tx_queues + (partition % num_queue);
    ConditionVariablePrepareToSleep(&queue->empty_cond);
    SpinLockAcquire(&queue->lock);
    while (queue->size <= 0)
    {
        SpinLockRelease(&queue->lock);
        ConditionVariableSleep(&queue->empty_cond, WAIT_EVENT_TX_READY_TO_COMMIT);
        SpinLockAcquire(&queue->lock);
    }
    ConditionVariableCancelSleep();
    tx = TAILQ_FIRST(&queue->list);
    TAILQ_REMOVE(&queue->list, tx, queue_link);
    tx->queue_link.tqe_prev = NULL;
    queue->size -= 1;
    SpinLockRelease(&queue->lock);
    ConditionVariableSignal(&queue->full_cond);
    return tx; 
}

static TupleTableSlot*
clone_slot(TupleTableSlot* slot)
{
    TupleTableSlot* ret;
    ret = MakeTupleTableSlot(slot->tts_tupleDescriptor, slot->tts_ops);
    ExecCopySlot(ret, slot);
    ret->tts_tableOid = slot->tts_tableOid;
    ret->tts_tupleDescriptor = CreateTupleDescCopy(slot->tts_tupleDescriptor);
    return ret;
}

BCDBShmXact*
get_tx_by_hash(const char *hash)
{
    BCDBShmXact *ret;
    SpinLockAcquire(tx_pool_lock);
    ret = hash_search(tx_pool, hash, HASH_FIND, NULL);
    SpinLockRelease(tx_pool_lock);
    return ret;
}

BCDBShmXact*
get_tx_by_xid(TransactionId xid)
{
    XidMapEntry *ret;

    SpinLockAcquire(xid_map_lock);
    ret = hash_search(xid_map, &xid, HASH_FIND, NULL);
    SpinLockRelease(xid_map_lock);
    if (!ret)
    {
        ereport(FATAL, (errmsg("[ZL] no conflict xid")));
    }
    return ret->tx;
}

BCDBShmXact*
get_tx_by_xid_locked(TransactionId xid, bool exclusive)
{
    XidMapEntry *ret;
    LWLockMode lockmode = exclusive ? LW_EXCLUSIVE : LW_SHARED;
    SpinLockAcquire(xid_map_lock);
    ret = hash_search(xid_map, &xid, HASH_FIND, NULL);
    if (!ret)
    {
        ereport(FATAL, (errmsg("[ZL] no conflict xid")));
    }
    LWLockAcquire(&ret->tx->lock, lockmode);
    SpinLockRelease(xid_map_lock);
    return ret->tx;
}

void
add_tx_xid_map(TransactionId xid, BCDBShmXact *tx)
{
    XidMapEntry *entry;
    bool    found;

    DEBUGNOCHECK("[ZL] add xid map: %d -> %s", (int)xid, tx->hash);
    SpinLockAcquire(xid_map_lock);
    entry = hash_search(xid_map, &xid, HASH_ENTER, &found);
    if (!found)
    {
        entry->xid = xid;
        entry->tx = tx;
    }
    else
    {
        ereport(FATAL, (errmsg("[ZL] already occupied by %d", (int)entry->xid)));
    }
    SpinLockRelease(xid_map_lock);
}

void
remove_tx_xid_map(TransactionId xid)
{
    bool found;
    XidMapEntry *entry;
    if (!TransactionIdIsValid(xid))
        return;

    DEBUGNOCHECK("[ZL] removing xid map: %d", (int)xid);
    SpinLockAcquire(xid_map_lock);
    entry = hash_search(xid_map, &xid, HASH_FIND, &found);
    if (entry)
    {
        LWLockAcquire(&entry->tx->lock, LW_EXCLUSIVE);
        hash_search(xid_map, &xid, HASH_REMOVE, &found);
        LWLockRelease(&entry->tx->lock);
    }
    SpinLockRelease(xid_map_lock);
    if (!found)
        ereport(FATAL, (errmsg("[ZL] xid map %d is already deleted!", (int)xid)));
}

void
store_optim_update(TupleTableSlot* slot, ItemPointer old_tid)
{
    OptimWriteEntry *write_entry;
    MemoryContext    old_context;
    DEBUGMSG("[ZL] tx %s storing update to (%d %d %d)", activeTx->hash, slot->tts_tableOid, *(int*)&old_tid->ip_blkid, (int)old_tid->ip_posid);
    old_context = MemoryContextSwitchTo(bcdb_tx_context);
    write_entry = palloc(sizeof(WriteTuple));
    write_entry->operation = CMD_UPDATE;
    write_entry->old_tid = *old_tid;
    write_entry->slot = clone_slot(slot);
    write_entry->cid = GetCurrentCommandId(true);
    SIMPLEQ_INSERT_TAIL(&activeTx->optim_write_list, write_entry, link);
    MemoryContextSwitchTo(old_context);
}

void
store_optim_insert(TupleTableSlot* slot)
{
    OptimWriteEntry *write_entry;
    MemoryContext    old_context;
    DEBUGMSG("[ZL] tx %s storing insert to (rel: %d)", activeTx->hash, slot->tts_tableOid);
    old_context = MemoryContextSwitchTo(bcdb_tx_context);
    write_entry = palloc(sizeof(WriteTuple));
    write_entry->operation = CMD_INSERT;
    write_entry->slot = clone_slot(slot);
    write_entry->cid = GetCurrentCommandId(true);
    SIMPLEQ_INSERT_TAIL(&activeTx->optim_write_list, write_entry, link);
    MemoryContextSwitchTo(old_context);
}

void
apply_optim_insert(TupleTableSlot* slot, CommandId cid)
{
    Relation relation = RelationIdGetRelation(slot->tts_tableOid);

    DEBUGMSG("[ZL] tx %s applying optim insert (rel: %d)", activeTx->hash, relation->rd_id);
    table_tuple_insert(relation, slot, cid, 0, NULL);

    heap_apply_index(relation, slot, true, true);
    RelationClose(relation);
}

void
apply_optim_update(ItemPointer tid, TupleTableSlot* slot, CommandId cid)
{
    TM_FailureData tmfd;
    TM_Result result;
    LockTupleMode lockmode;
    bool update_indexes;
    Relation relation = RelationIdGetRelation(slot->tts_tableOid);

    DEBUGMSG("[ZL] tx %s applying optim update (%d %d %d)", activeTx->hash, relation->rd_id, *(int*)&tid->ip_blkid, (int)tid->ip_posid);
    result = table_tuple_update(relation, tid, slot,
                       cid,
                       InvalidSnapshot,
                       InvalidSnapshot,
                       false, /* do not wait for commit */
                       &tmfd, &lockmode, &update_indexes);


    if (result != TM_Ok)
    {
        RelationClose(relation);
		ereport(ERROR,
				(errcode(ERRCODE_T_R_SERIALIZATION_FAILURE),
    			 errmsg("tx %s doomed because of ww-conflict", activeTx->hash)));
    }


    if (update_indexes)
        heap_apply_index(relation, slot, false, false);

    RelationClose(relation);
}

void
apply_optim_writes(void)
{
    OptimWriteEntry *write_entry;
    while ((write_entry = SIMPLEQ_FIRST(&activeTx->optim_write_list)))
    {
        switch (write_entry->operation)
        {
            case CMD_UPDATE:
                apply_optim_update(&write_entry->old_tid, write_entry->slot, write_entry->cid);
                break;
            case CMD_INSERT:
                apply_optim_insert(write_entry->slot, write_entry->cid);
                break;
            default:
                ereport(ERROR, (errmsg("[ZL] tx %s applying unknown operation", activeTx->hash)));
        }
        SIMPLEQ_REMOVE_HEAD(&activeTx->optim_write_list, link);
    }
}

bool
check_stale_read(void)
{
    RWConflict       conflict;
    LWLockAcquire(SerializableXactHashLock, LW_SHARED);
    conflict = (RWConflict)
		SHMQueueNext(&activeTx->sxact->outConflicts,
					 &activeTx->sxact->outConflicts,
					 offsetof(RWConflictData, outLink));
	while (conflict)
	{
		if (BCDB_TX(conflict->sxactIn)->block_id_committed < activeTx->block_id_committed)
    		ereport(ERROR,
    				(errcode(ERRCODE_T_R_SERIALIZATION_FAILURE),
    				 errmsg("tx %s stale read found, %s update first", activeTx->hash, BCDB_TX(conflict->sxactIn)->hash)));

		conflict = (RWConflict)
			SHMQueueNext(&activeTx->sxact->outConflicts,
						 &conflict->outLink,
						 offsetof(RWConflictData, outLink));
	}
    LWLockRelease(SerializableXactHashLock);
    return true;
}

void
conflict_check(void)
{
    WSTableEntryRecord *record;
    
    LIST_FOREACH(record, &ws_table_record, link)
    {
        if (ws_table_check(&record->tag))
    		ereport(ERROR,
 				(errcode(ERRCODE_T_R_SERIALIZATION_FAILURE),
   				 errmsg("tx %s aborted due to waw", activeTx->hash)));           
    }

    LIST_FOREACH(record, &ws_table_record, link)
    {
        if (rs_table_check(&record->tag))
        {
            WSTableEntryRecord *raw_record;
            LIST_FOREACH(raw_record, &rs_table_record, link)
            {
                if (ws_table_check(&raw_record->tag))
            		ereport(ERROR,
         				(errcode(ERRCODE_T_R_SERIALIZATION_FAILURE),
           				 errmsg("tx %s aborted due to raw and war", activeTx->hash)));
            }
            break;
        }
    }

}

void
clean_rs_ws_table(void)
{
    shm_hash_clear(ws_table->map, MAX_WRITE_CONFLICT);
    shm_hash_clear(rs_table->map, MAX_WRITE_CONFLICT);
}