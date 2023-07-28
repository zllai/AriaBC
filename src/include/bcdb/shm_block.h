#ifndef BCDB_SHM_BLOCK_H
#define BCDB_SHM_BLOCK_H

#include "postgres.h"
#include "storage/lwlock.h"
#include "bcdb/shm_transaction.h"
#include "bcdb/bcdb_dsa.h"
#include "lib/dshash.h"
#include "sys/queue.h"
#include "bcdb/globals.h"
#include "storage/condition_variable.h"
#include "storage/spin.h"
#include "c.h"


/* unfortunately, the name Block conflicts with another component in postgres, so use ugly BCBlock for now */
typedef struct
{
    BCBlockID  id;
    int        num_tx;
    int volatile       num_ready;
    int volatile       num_finished;
    BCDBShmXact*       txs[MAX_TX_PER_BLOCK];
    ConditionVariable  cond;
} BCBlock;

typedef struct
{
    /* bid < global_bmin: block committed */
    /* bid < global_bmin - CLEANING_DELAY_BLOCKS: block cleaned*/
    BCBlockID volatile global_bmin;
    BCBlockID volatile global_bmax;
    ConditionVariable  conds[NUM_BMIN_COND];
    ConditionVariable  token_cond;
    uint32 debug_seq;
    int32 volatile     num_committed;
    int32 volatile     num_aborted;
    uint64 volatile    previous_report_ts;
    int32 volatile    previous_report_commit; 
#ifdef LOG_STATUS
    char log[1024 * 1024 * 10];
    int  log_counter;
#endif
} BlockMeta;

/* todo: change it to HTAB */
extern HTAB          *block_pool;
extern slock_t       *block_pool_lock;
extern BlockMeta     *block_meta;

extern Size     block_pool_size(void);
extern void     create_block_pool(void);
extern BCBlock* get_block_by_id(BCBlockID id, bool create_if_not_found);
extern void     delete_block(BCBlock *block);
extern void     delete_block_by_id(BCBlockID id);
extern void     block_add_tx(BCBlock* block, BCDBShmXact* tx);
extern char*    print_block_status(BCBlockID block_id);



#endif