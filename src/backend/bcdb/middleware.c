//
// Created by Chris Liu on 6/5/2020.
//

#include "bcdb/shm_transaction.h"
#include "bcdb/worker.h"
#include "bcdb/middleware.h"
#include "bcdb/shm_block.h"
#include "bcdb/worker_controller.h"
#include "libpq/libpq.h"
#include "libpq-fe.h"
#include "storage/condition_variable.h"
#include "pgstat.h"
#include "utils/memutils.h"
#include "storage/lwlock.h"
#include "storage/predicate.h"
#include "bcdb/globals.h"
#include <unistd.h>
#include <stdlib.h>
#include <string.h>

MemoryContext bcdb_middleware_context;
int32         tx_num = 0;
int32         blocksize = 0;
uint64        start_time;

static BCDBShmXact *parse_tx(const char* json);
//static BCBlock     *parse_block(const char* json);
static void bcdb_middleware_attach_tx_to_block(BCDBShmXact *tx, BCBlock *block);
//static void bcdb_middleware_conflict_check(BCBlock *block);
//static void dfs_conflict_check_recursive(SERIALIZABLEXACT *sxact, BCBlockID bid, int *counter);
//static RWConflict find_min_conflict(SHM_QUEUE *queue);
static BCBlock *parse_block_with_txs(const char *json);
//void signal_stale_read(SERIALIZABLEXACT *sxact);

void
bcdb_middleware_init(bool is_oep_mode, int32 block_size)
{
    MemoryContext    old_context;

    /* Aria does not have oep mode */
    is_bcdb_master = true;
    blocksize = block_size;
    bcdb_middleware_context = 
        AllocSetContextCreate(TopMemoryContext, 
                              "middleware memory context", 
                              ALLOCSET_DEFAULT_SIZES);
    old_context = MemoryContextSwitchTo(bcdb_middleware_context);
    idle_worker_list_init(block_size);
    MemoryContextSwitchTo(old_context);
    pid = getpid();
    start_time = bcdb_get_time();
}

BCDBShmXact *
parse_tx(const char* json)
{
    cJSON   *parsed   = NULL;
    cJSON   *sql      = NULL;
    cJSON   *hash     = NULL;
    cJSON   *create_time = NULL;
    BCDBShmXact   *tx;
    int     isolation;
    bool    pred_lock = false;

    parsed = cJSON_Parse(json);
    if (!parsed)
        goto error;

    sql = cJSON_GetObjectItemCaseSensitive(parsed, "sql");
    if (!cJSON_IsString(sql) || (sql->valuestring == NULL))
        goto error;

    hash = cJSON_GetObjectItemCaseSensitive(parsed, "hash");
    if (!cJSON_IsString(hash))
        goto error;
    
    isolation = XACT_SERIALIZABLE;
    pred_lock = true;

    tx = create_tx(hash->valuestring, sql->valuestring, BCDBInvalidTid, BCDBInvalidBid, isolation, pred_lock);

    create_time = cJSON_GetObjectItemCaseSensitive(parsed, "create_ts");

    if (cJSON_IsString(create_time))
    {
        char *endpt;
        tx->create_time = strtoll(create_time->valuestring, &endpt, 10);
    }

    if (tx == NULL)
    {
        ereport(ERROR,
            (errmsg("[ZL] cannot create transaction in shared memory")));
        return NULL;
    }
    cJSON_Delete(parsed);
    return tx;

error:
    ereport(ERROR,
        (errmsg("[ZL] Cannot parse transaction: %s", json)));
    /* no need to do clean here, because memory context will do that for us */
    return NULL;
}

BCBlock *
parse_block_with_txs(const char *json)
{
    cJSON *parsed;
    cJSON *tx_list;
    cJSON *block_id;
    cJSON *tx_json;
    BCBlock *block;
    int   tx_id_counter = 0;

    parsed = cJSON_Parse(json);
    if (!parsed)
        goto error;
    
    block_id = cJSON_GetObjectItemCaseSensitive(parsed, "bid");
    if (!cJSON_IsNumber(block_id) || block_id->valueint != block_meta->global_bmax)
        goto error;
    
    tx_list = cJSON_GetObjectItemCaseSensitive(parsed, "txs");
    if (!cJSON_IsArray(tx_list))
        goto error;

    block = get_block_by_id(block_id->valueint, true);
    Assert(block->num_tx == 0);
    block->num_tx = cJSON_GetArraySize(tx_list);
    cJSON_ArrayForEach(tx_json, tx_list)
    {
        cJSON   *sql      = NULL;
        cJSON   *hash     = NULL;
        cJSON   *create_time = NULL;
        BCDBShmXact   *tx;
        int     isolation;
        bool    pred_lock = false;

        sql = cJSON_GetObjectItemCaseSensitive(tx_json, "sql");
        if (!cJSON_IsString(sql) || (sql->valuestring == NULL))
            goto error;

        hash = cJSON_GetObjectItemCaseSensitive(tx_json, "hash");
        if (!cJSON_IsString(hash))
            goto error;

        isolation = XACT_SERIALIZABLE;
        pred_lock = true;

        tx = create_tx(hash->valuestring, sql->valuestring, BCDBInvalidTid, BCDBInvalidBid, isolation, pred_lock);

        create_time = cJSON_GetObjectItemCaseSensitive(tx_json, "create_ts");

        if (cJSON_IsString(create_time))
        {
            char *endpt;
            tx->create_time = strtoll(create_time->valuestring, &endpt, 10);
        }
        
        tx->tx_id = tx_id_counter + (block->id - 1) * blocksize;
        tx->block_id_committed = block->id;
        block->txs[tx_id_counter] = tx;
        tx_id_counter += 1;
    }
    return block;

error:
    ereport(FATAL,
        (errmsg("[ZL] cannot create block in shared memory")));
    return NULL;
}

int 
bcdb_middleware_submit_tx(const char* tx_string)
{
    BCDBShmXact *tx;
    tx = parse_tx(tx_string);
    tx_queue_insert(tx, tx_num++);
    return 0;
}

void
bcdb_middleware_submit_block(const char* block_json)
{
    BCBlock     *block;
    ++block_meta->global_bmax;
    block = parse_block_with_txs(block_json);
    for (int i=0; i < block->num_tx; i++)
    {
        tx_queue_insert(block->txs[i], tx_num++);
    }
}

void 
bcdb_wait_tx_finish(char *tx_hash)
{
    BCDBShmXact *tx;
    tx = get_tx_by_hash(tx_hash);
    ConditionVariablePrepareToSleep(&tx->cond);
    while(tx->status != TX_COMMITED && tx->status != TX_ABORTED)
        ConditionVariableSleep(&tx->cond, WAIT_EVENT_TX_FINISH);
    ConditionVariableCancelSleep();
}

void
bcdb_middleware_wait_all_to_finish()
{
    WaitGlobalBmin(block_meta->global_bmax + 1);
    ereport(LOG, (errmsg("[ZL] total throughput: %.3f", (double)block_meta->num_committed * 1e6 / (bcdb_get_time() - start_time))));
}

void 
bcdb_middleware_set_txs_committed_block(char * tx_hash, int32 block_id)
{
    BCDBShmXact *tx;
    BCBlock     *block;
    tx = get_tx_by_hash(tx_hash);
    block = get_block_by_id(block_id, true);
    bcdb_middleware_attach_tx_to_block(tx, block);
}

void
bcdb_middleware_attach_tx_to_block(BCDBShmXact *tx, BCBlock *block)
{
    block_add_tx(block, tx);
    tx->block_id_committed = block->id;
}

void
block_cleaning(BCBlockID current_block_id)
{
    BCBlock *block_to_clean;
    uint64 cur_report_ts = bcdb_get_time();
    int32  cur_num_committed = block_meta->num_committed;
    float abort_rate = (float)block_meta->num_aborted / (block_meta->num_aborted + block_meta->num_committed);

    if (current_block_id > CLEANING_DELAY_BLOCKS)
    {
        block_to_clean = get_block_by_id(current_block_id - CLEANING_DELAY_BLOCKS, false);
        if (block_to_clean != NULL)
        {
            for (int i=0; i < block_to_clean->num_tx; i++)
            {
#ifdef LOG_STATUS
                block_meta->log_counter += sprintf(block_meta->log + block_meta->log_counter, "%s %d\n", block_to_clean->txs[i]->hash, block_to_clean->txs[i]->status);
                if (block_meta->log_counter > 1024 * 1024 * 10)
                    ereport(FATAL, (errmsg("[ZL] log overflow")));
#endif
                delete_tx(block_to_clean->txs[i]);
            }
        }
        delete_block(block_to_clean);
    }

    if (cur_report_ts - block_meta->previous_report_ts > 1e6 * REPORT_INTERVAL)
    {
        if (block_meta->previous_report_ts != 0)
        {
            ereport(LOG, (errmsg("[ZL] throughput: %.3f", (cur_num_committed - block_meta->previous_report_commit) * 1e6 / (cur_report_ts - block_meta->previous_report_ts))));
            ereport(LOG, (errmsg("[ZL] abort rate: %.3f", abort_rate)));
        }
        block_meta->previous_report_ts = cur_report_ts;
        block_meta->previous_report_commit = cur_num_committed;
    }
}

void
allow_all_block_txs_to_commit(BCBlock *block)
{
    return;
}
/*
RWConflict
find_min_conflict(SHM_QUEUE *queue)
{
	RWConflict    cur_min;
    RWConflict    iter;
    iter = (RWConflict)SHMQueueNext(queue, queue, offsetof(RWConflictData, outLink));
    cur_min = iter;
    while(iter)
    {
        if (BCDB_TX(iter->sxactIn)->tx_id < BCDB_TX(cur_min->sxactIn)->tx_id)
            cur_min = iter;
        iter = (RWConflict)SHMQueueNext(queue, &iter->outLink, offsetof(RWConflictData, outLink));
    }
    return cur_min;
}
*/

/*
void
signal_stale_read(SERIALIZABLEXACT *sxact)
{
    RWConflict iter;
    iter = (RWConflict)SHMQueueNext(&sxact->inConflicts, &sxact->inConflicts, offsetof(RWConflictData, inLink));
    while (iter)
    {
        if (BCDB_TX(iter->sxactOut)->block_id_committed > BCDB_TX(iter->sxactIn)->block_id_committed)
        {
            iter->sxactOut->flags |= SXACT_FLAG_DOOMED;
            sprintf(BCDB_TX(iter->sxactOut)->why_doomed, "stale read, %s update first", BCDB_TX(iter->sxactIn)->hash);
            ConditionVariableBroadcast(&BCDB_TX(iter->sxactOut)->cond);
        }
        iter = (RWConflict)SHMQueueNext(&sxact->inConflicts, &iter->inLink, offsetof(RWConflictData, inLink));
    }
}
*/
/*
void
dfs_conflict_check_recursive(SERIALIZABLEXACT *sxact, BCBlockID bid, int *counter)
{
	RWConflict        outConflict;
    SERIALIZABLEXACT *decendant;
    sxact->pre_ts = (*counter)++;

    if (BCDB_TX(sxact)->status != TX_WAIT_FOR_COMMIT || SxactIsDoomed(sxact) || SxactIsRolledBack(sxact))
        return;

    DEBUGNOCHECK("[ZL] dfs step in Tx: %s", BCDB_TX(sxact)->hash);

    outConflict = find_min_conflict(&sxact->outConflicts);
    while (outConflict)
    {
        decendant = outConflict->sxactIn;
        if (!SxactIsDoomed(decendant) && !SxactIsRolledBack(decendant))
        {
            if (BCDB_TX(decendant)->block_id_committed == block_meta->global_bmin)
            {
                DEBUGNOCHECK("[ZL] dfs visiting Tx: %d_%d", BCDB_TX(decendant)->block_id_committed, BCDB_TX(decendant)->tx_id);
                if (decendant->pre_ts != -1 && decendant->pre_ts < sxact->pre_ts && decendant->post_ts == -1)
                {
                    sxact->flags |= SXACT_FLAG_DOOMED;
                    BCDB_TX(sxact)->status = TX_ABORTING;
                    sprintf(BCDB_TX(sxact)->why_doomed, "failed conflict check");
                    DEBUGNOCHECK("[ZL] dfs Tx doomed: %d_%d", BCDB_TX(sxact)->block_id_committed, BCDB_TX(sxact)->tx_id);
                    break;
                }
                if (decendant->pre_ts == -1)
                    dfs_conflict_check_recursive(decendant, bid, counter);
            }
        }
        if (ShmemAddrIsValid(outConflict->inLink.next) && ShmemAddrIsValid(outConflict->inLink.prev))
            ReleaseRWConflict(outConflict);

        outConflict = find_min_conflict(&sxact->outConflicts);
    }
    sxact->post_ts = (*counter)++;
    //if (!SxactIsDoomed(sxact))
    //    signal_stale_read(sxact);

    DEBUGNOCHECK("[ZL] dfs step out Tx: %s", BCDB_TX(sxact)->hash);
}
*/

void
bcdb_middleware_conflict_check(BCBlock *block)
{
    /* we assume no one is touching the conflict graph here */
    return;
}


void bcdb_middleware_allow_txs_exec_write_set_and_commit(BCBlock *block) {

//    bcdb_middleware_allow_execute_write_set(block);

    allow_all_block_txs_to_commit(block);
}

void bcdb_middleware_allow_txs_exec_write_set_and_commit_by_id(int32 id){
    BCBlock *block;
    
    block = get_block_by_id(id, false);
    Assert(block != NULL);
    bcdb_middleware_allow_txs_exec_write_set_and_commit(block);
}

bool bcdb_is_tx_commited(char * tx_hash){
    BCDBShmXact* target_tx = get_tx_by_hash(tx_hash);

    if(target_tx->status == TX_COMMITED){
        return true;
    }else{
        return false;
    }
}

void 
bcdb_clear_block_txs_store()
{
    shm_hash_clear(block_pool, MAX_NUM_BLOCKS);
    clear_tx_pool();
    block_meta->global_bmin = 1;
    block_meta->global_bmax = 0;
    block_meta->debug_seq += 1;
    block_meta->num_committed = 0;
    while(!LIST_EMPTY(&idle_workers.list))
    {
        WorkerController *worker = LIST_FIRST(&idle_workers.list);
        worker_finish(worker);
        LIST_REMOVE(worker, link);
        pfree(worker);
    }
    idle_workers.num = 0;
}

/*
void bcdb_middleware_new_block_handler(BCBlock* block){
    // Search the SHM_TX and notify the the backend to process
    Transaction *tmp_tx;

    //notify the backend to proceed 1 by 1
    for(int x=0; x < block->num_tx; x++){
        if(!bcdb_middleware_set_txs_committed_blcok(tmp_tx->hash, block->id, false)){
            //todo: should wait for tx execution
        }
    }

    bcdb_middleware_allow_txs_exec_write_set_and_commit(block);
}
*/

/*
// assume dummy file contains jsons per line
Transaction* parsing_dummy_block_file(const char* file_path){
    FILE *fptr;
    char line_buffer[10000];
    Transaction *tmp_tx, *last, *first;

    last = NULL;

    if ((fptr = fopen(file_path, "r")) != NULL){
        while(fscanf(fptr, "%[^\n]\n", line_buffer) != EOF) {
            tmp_tx = parse_tx(line_buffer);
            //todo clean up
            if (last) {
                LIST_INSERT_AFTER(last, tmp_tx, link);
            } else{
                first = tmp_tx;
            }
            last = tmp_tx;
        }
        return first;
    }

    return NULL;
}
*/

/*
//dummy function called by frontend
void bcdb_middleware_dummy_block(const char* file_path, uint32 block_id){
    BCBlock* block;
    //read the file
    Transaction* head_tx = parsing_dummy_block_file(file_path);

    //construct BCBlock here
    block = ShmemAlloc(sizeof(BCBlock));
    block_initialize(block);

    block->id = block_id;
    block_set_txs(block, head_tx);

    bcdb_middleware_new_block_handler(block);
}
*/

/*
void bcdb_middleware_dummy_submit_tx(const char* file_path){
    FILE *fptr;
    char line_buffer[10000];

    if ((fptr = fopen(file_path, "r")) != NULL){
        while(fscanf(fptr, "%[^\n]\n", line_buffer) != EOF) {
            bcdb_master_process_tx(line_buffer);
        }
    }
}
*/

//Return false if 1)no tx with that hash or 2) tx is not finish execution

