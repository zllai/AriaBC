#ifndef BCDB_SHM_TRANSACTION_H
#define BCDB_SHM_TRANSACTION_H

/*
 * Transaction structure in shared memrory
 */
#include "postgres.h"
#include <access/xact.h>
#include <executor/tuptable.h>
#include "executor/execdesc.h"
#include <utils/relcache.h>
#include <nodes/execnodes.h>
#include "storage/lwlock.h"
#include "nodes/execnodes.h"
#include "executor/tuptable.h"
#include "bcdb/utils/sys-queue.h"
#include "storage/predicate_internals.h"
#include "utils/portal.h"
#include "lib/dshash.h"
#include "bcdb/globals.h"
#include "storage/condition_variable.h"
#include "storage/predicate_internals.h"
#include "utils/hsearch.h"
#include <sys/types.h>
#include <semaphore.h>
#include "storage/spin.h"
#include "openssl/sha.h"

typedef enum 
{
    TX_SCHEDULING,
    TX_WAITING,
    TX_EXECUTING,
    TX_WAIT_FOR_BLOCK,
    TX_EXEC_WRITE_SET,
    TX_WAIT_FOR_COMMIT,
    TX_COMMITTING,
    TX_COMMITED,
    TX_ABORTED,
    TX_ABORTING,
    TX_RETRYING,
} TxStatus;

typedef struct _WriteTuple{

    Oid relationOid;

//    indicate whether it is INSERT,UPDATE,DELETE
    CmdType operation;

//    For update and delete
    ItemPointerData tupleid;

//    For udpate and insert
    TupleTableSlot* slot;

//    Linked list to point nex WriteTuple
    LIST_ENTRY(_WriteTuple) list_entry;

} WriteTuple;

typedef struct _ReadTuple{
    HeapTuple tuple;
    LIST_ENTRY(_ReadTuple) list_entry;
} ReadTuple;

typedef struct _WriteEntry
{
    CmdType         operation;
    ItemPointerData old_tid;
    HeapTuple       newtup;
    bool            hot_attr_updated;
    bool            keys_updated;
    bool            cid_is_combo;
    CommandId       cid;
    SIMPLEQ_ENTRY(_WriteEntry) link;
} WriteEntry;

typedef struct _OptimWriteEntry
{
    CmdType         operation;
    TupleTableSlot  *slot;
    ItemPointerData old_tid;
    CommandId       cid;
    SIMPLEQ_ENTRY(_OptimWriteEntry) link;
} OptimWriteEntry;

/* to do: move non-shared element out */
typedef struct _BCDBShmXact
{
    /* hash servers as a unique ID accross the blocks */
    char               hash[TX_HASH_SIZE];
    BCTxID             tx_id;

    BCBlockID          block_id_snapshot;
    BCBlockID volatile block_id_committed;
    char               sql[1024];

    TxStatus volatile  status;
    QueryDesc          *queryDesc;
    Portal             portal;

    int                isolation;
    bool               pred_lock;

    SIMPLEQ_ENTRY(_BCDBShmXact)              link;
    TAILQ_ENTRY(_BCDBShmXact)                queue_link;
    int32                                    queue_partition;
    SIMPLEQ_HEAD(_OptimWriteList, _OptimWriteEntry) optim_write_list;
    SERIALIZABLEXACT         *sxact;
    ConditionVariable         cond;
    LWLock                    lock;
    TransactionId             xid;
    pid_t                     worker_pid;
    /* void* is a dirty trick to avoid including frontend headers */
    void*           worker;
    char            why_doomed[258];
    SHA256_CTX      state_hash;
    bool            has_war;
    bool            has_raw;

    uint64          create_time;
    uint64          start_simulation_time;
    uint64          start_parsing_time;
    uint64          start_checking_time;
    uint64          end_checking_time;
    uint64          end_parsing_time;
    uint64          end_simulation_time;
    uint64          start_local_copy_time;
    uint64          end_local_copy_time;
    uint64          commit_time;
} BCDBShmXact;

typedef struct _TxQueue
{
    TAILQ_HEAD(_TxAttachedQueueHead, _BCDBShmXact) list;
    slock_t                                   lock;
    ConditionVariable                        empty_cond;
    ConditionVariable                        full_cond;
    int32 volatile                           size;
} TxQueue;

typedef struct _XidMapEntry
{
    TransactionId    xid;
    BCDBShmXact     *tx;
} XidMapEntry;

typedef struct _WSTableEntry
{
    PREDICATELOCKTARGETTAG tag;
    BCTxID  tx_id;
} WSTableEntry;

typedef struct _WSTable
{
    /* partition the available list and HTAB to avoid contention */
    HTAB               *map;
    slock_t             map_locks[WRITE_CONFLICT_MAP_NUM_PARTITIONS];
} WSTable;

typedef struct _WSTableEntryRecord
{
    PREDICATELOCKTARGETTAG tag;
    LIST_ENTRY(_WSTableEntryRecord) link;
} WSTableEntryRecord;

typedef LIST_HEAD(_WSTableRecord, _WSTableEntryRecord) WSTableRecord;

extern BCDBShmXact  *activeTx;
extern HTAB         *tx_pool;
extern TxQueue      *tx_queues;
extern WSTableRecord ws_table_record;
extern WSTableRecord rs_table_record;

extern BCDBShmXact* tx_queue_next(int32 partition);
extern void         tx_queue_insert(BCDBShmXact *tx, int32 partition);

extern void         create_tx_pool(void);
extern void         clear_tx_pool(void);
extern Size         tx_pool_size(void);
extern BCDBShmXact* get_tx_by_hash(const char *hash);
extern BCDBShmXact* get_tx_by_xid(TransactionId xid);
extern void         add_tx_xid_map(TransactionId id, BCDBShmXact *tx);
extern void         remove_tx_xid_map(TransactionId id);
extern BCDBShmXact* create_tx(char *hash, char *sql, BCTxID tx_id, BCBlockID snapshot_block, int isolation, bool pred_lock);
extern void         delete_tx(BCDBShmXact* tx);

extern uint32 compose_tuple_hash(Oid relation_id, ItemPointer tid);
extern uint32 compose_index_hash(Oid relation_id, IndexTuple itup);
extern void  compose_tx_hash(BCBlockID bid, BCTxID tx_id, char* out_hash);
extern BCDBShmXact* get_tx_by_xid_locked(TransactionId xid, bool exclusive);

extern uint32 dummy_hash(const void *key, Size key_size);
extern void store_optim_update(TupleTableSlot* slot, ItemPointer old_tid);
extern void store_optim_insert(TupleTableSlot* slot);
extern void apply_optim_update(ItemPointer tid, TupleTableSlot* slot, CommandId cid);
extern void apply_optim_insert(TupleTableSlot* slot, CommandId cid);
extern void apply_optim_writes(void);
extern bool check_stale_read(void);
extern void ws_table_reserve(PREDICATELOCKTARGETTAG *tag);
extern bool ws_table_check(PREDICATELOCKTARGETTAG *tag);
extern void clean_ws_table_record(void);
extern void rs_table_reserve(const PREDICATELOCKTARGETTAG *tag);
extern bool rs_table_check(PREDICATELOCKTARGETTAG *tag);
extern void clean_rs_table_record(void);
extern void conflict_check(void);
extern void clean_rs_ws_table(void);
#endif