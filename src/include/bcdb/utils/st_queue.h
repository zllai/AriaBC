#ifndef BCDB_STQUEUE_H
#define BCDB_STQUEUE_H

#include "postgres.h"
#include "sys/queue.h"

typedef struct _STQEntry
{
    void                    *value;
    TAILQ_ENTRY(_STQEntry)   links;
} STQEntry;

typedef struct
{
    TAILQ_HEAD(CQHEAD, _STQEntry) head;
} STQueue;

#define stq_entry_value(x) x->value;

extern STQueue *create_stq(void);
extern STQEntry *stq_enqueue_v(STQueue* queue, void* elem);
extern void *stq_dequeue_v(STQEntry* queue);
extern STQEntry *stq_dequeue_e(STQueue* queue);
extern void stq_enqueue_e(STQueue* queue, STQEntry* elem);
extern void stq_clear(STQueue* queue);

#endif
