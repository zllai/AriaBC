#ifndef BCDB_GLOBAL_H
#define BCDB_GLOBAL_H

#include "postgres.h"
#include "utils/memutils.h"
#include "utils/ps_status.h"
#include <unistd.h>
#include <stdlib.h>
#include <sys/resource.h>

extern PGDLLIMPORT bool                is_bcdb_master; 
extern PGDLLIMPORT bool                is_bcdb_worker; 
extern PGDLLIMPORT int                 gdb_pause_sig; 
extern PGDLLIMPORT char                *bcdb_host;
extern PGDLLIMPORT char                *bcdb_port;
extern PGDLLIMPORT bool                OEP_mode;

typedef enum BcdbIsolationLevel{
    BCDB_READ_COMMITED,
    BCDB_SERIALIZABLE
} BcdbIsolationLevel;

typedef int32 BCBlockID;
typedef int32 BCTxID;

extern BcdbIsolationLevel BcdbCurrentIsolationLevel;
extern MemoryContext bcdb_middleware_context;
extern MemoryContext bcdb_tx_context;
extern bool          skip_conflict_checking;
extern pid_t         pid;
extern int32         blocksize;
extern int32         worker_id;

//#define FIRST_WRITER_WINS
#define WAIT_GDB while(gdb_pause_sig == 0) {set_ps_display("waiting gdb", false); sleep(1);}
#define BCDBInvalidBid -1
#define BCDBMaxBid     0x7FFFFFFF
#define BCDBInvalidTid -1
#define CLEANING_DELAY_BLOCKS 5
#define QUEUEING_BLOCKS 32
#define MAX_NUM_BLOCKS (QUEUEING_BLOCKS + CLEANING_DELAY_BLOCKS + 100)
#define MAX_TX_PER_BLOCK 200
#define WORK_TOKENS 64
#define WORKER_INIT_NUM 64
#define NUM_BMIN_COND 1
#define MAX_SHM_TX ((CLEANING_DELAY_BLOCKS + QUEUEING_BLOCKS + 100) * MAX_TX_PER_BLOCK)
#define MAX_WRITE_CONFLICT (MAX_TX_PER_BLOCK * 128)
#define TX_HASH_SIZE 32
#define WRITE_CONFLICT_MAP_NUM_PARTITIONS 8
#define AVAILABLE_LIST_PARTITION_SIZE (MAX_WRITE_CONFLICT * MAX_TX_PER_BLOCK / WRITE_CONFLICT_MAP_NUM_PARTITIONS)
#define NUM_TX_QUEUE_PARTITION MAX_TX_PER_BLOCK
//#define DEBUGMSG(f_, ...) do { if (activeTx) ereport(DEBUG3, (errmsg((f_), ##__VA_ARGS__))); } while(0)
//#define DEBUGNOCHECK(f_, ...) ereport(DEBUG3, (errmsg((f_), ##__VA_ARGS__)))
#define DEBUGMSG(...) {}
#define DEBUGNOCHECK(...) {}
//#define LOG_STATUS
#define REPORT_INTERVAL 2

#define SetPriority(prio) \
do { \
    if (setpriority(PRIO_PROCESS, pid, prio) != 0) \
        ereport(FATAL, (errmsg("[ZL] cannot set priority"))); \
} while(0)

#define ReleaseToken() \
do {\
if (activeTx->holding_token) { \
	if (__sync_add_and_fetch(&block_meta->work_token, 1) > 0) \
        ConditionVariableSignal(&block_meta->token_cond); \
    activeTx->holding_token = false; \
}} while(0)

#define ForceGetToken() \
do { \
if (!activeTx->holding_token) { \
    __sync_sub_and_fetch(&block_meta->work_token, 1); \
    tx->holding_token = true; \
}} while(0)

#define WaitCondition(v, cond) \
do {\
if (!(cond)) { \
    ConditionVariablePrepareToSleep(v); \
    while(!(cond)) \
        ConditionVariableSleep(v, WAIT_EVENT_BLOCK_COMMIT); \
    ConditionVariableCancelSleep(); \
}} while(0)

#define WaitConditionWithBackOff(v, cond) \
do {\
if (!(cond)) { \
    volatile uint64 backoff = 1000 + (rand() % 100) * 10; \
    for (; backoff > 0; backoff--); \
    if (!(cond)) { \
        ConditionVariablePrepareToSleep(v); \
        while(!(cond)) \
            ConditionVariableSleep(v, WAIT_EVENT_BLOCK_COMMIT); \
        ConditionVariableCancelSleep(); \
    } \
}} while(0)

#define WaitConditionAndReleaseToken(v, cond) \
do {\
if (!(cond)) { \
    ReleaseToken(); \
    ConditionVariablePrepareToSleep(v); \
    while(!(cond)) \
        ConditionVariableSleep(v, WAIT_EVENT_BLOCK_COMMIT); \
    ConditionVariableCancelSleep(); \
}} while(0)

#define WaitConditionAndReleaseTokenWithBackoff(v, cond) \
do {\
if (!(cond)) { \
    if (activeTx->holding_token) { \
        volatile uint64 backoff = 10000 + (rand() % 1000) * 10; \
        for (; backoff > 0; backoff--); \
    } \
    if (!(cond)) { \
        ReleaseToken(); \
        ConditionVariablePrepareToSleep(v); \
        while(!(cond)) \
            ConditionVariableSleep(v, WAIT_EVENT_BLOCK_COMMIT); \
        ConditionVariableCancelSleep(); \
    } \
}} while(0)

#define WaitGlobalBmin(bmin) \
do \
{ \
    WaitCondition(&block_meta->conds[(bmin) % NUM_BMIN_COND], block_meta->global_bmin == (bmin)); \
} while(0)

#define WaitGlobalBminGreaterOrEqual(bmin) \
do \
{ \
    WaitCondition(&block_meta->conds[(bmin) % NUM_BMIN_COND], block_meta->global_bmin >= (bmin)); \
} while(0)

#define WaitGlobalBminAndReleaseToken(bmin) \
do \
{ \
    WaitConditionAndReleaseToken(&block_meta->conds[(bmin) % NUM_BMIN_COND], block_meta->global_bmin == (bmin)); \
} while(0)


#define CLOCKS_PER_MICRO_SECOND (CLOCKS_PER_SEC / 1000000l)
uint64 bcdb_get_time(void);
int Base64Encode(const unsigned char* buffer, size_t length, char** b64text);
#endif
