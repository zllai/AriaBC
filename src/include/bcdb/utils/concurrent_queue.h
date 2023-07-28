#ifndef BCDB_UTILS_CONCURRENT_QUEUE_H
#define BCDB_UTILS_CONCURRENT_QUEUE_H

#include "postgres.h"
#include "sys/queue.h"

typedef struct _CQEntry
{
    void                    *value;
    TAILQ_ENTRY(_CQEntry)   links;
} CQEntry;

typedef struct
{
    TAILQ_HEAD(CQHEAD, _CQEntry) head;
    pthread_mutex_t              lock;
} ConcurrentQueue;

#define cq_entry_value(x) x->value;

extern ConcurrentQueue *create_cq(void);
extern CQEntry *cq_enqueue_v(ConcurrentQueue* queue, void* elem);
extern void *cq_dequeue_v(ConcurrentQueue* queue);
extern CQEntry *cq_dequeue_e(ConcurrentQueue* queue);
extern void cq_enqueue_e(ConcurrentQueue* queue, CQEntry* elem);
extern void cq_clear(ConcurrentQueue* queue);


#endif
