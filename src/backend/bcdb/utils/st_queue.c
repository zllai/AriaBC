#include "bcdb/utils/st_queue.h"
#include "utils/elog.h"
#include "utils/memutils.h"

/* this file is abandoned */

STQueue *
create_cq(void)
{
    STQueue *queue = palloc(sizeof(*queue));
    TAILQ_INIT(&queue->head);
    return queue;
}


STQEntry *
stq_enqueue_v(STQueue* queue, void* value)
{
    STQEntry *entry;
    if (queue == NULL)
        return NULL;
    entry = palloc(sizeof(*entry));
    entry->value = value;
    TAILQ_INSERT_TAIL(&queue->head, entry, links);
    return entry;
}

void *
cq_dequeue_v(STQueue* queue)
{
    STQEntry *front;
    void    *value;
    if (queue == NULL)
        return NULL;
    
    front = TAILQ_FIRST(&queue->head);
    if (front == NULL)
        return NULL;

    value = front->value;
    TAILQ_REMOVE(&queue->head, front, links);

    pfree(front);
    return value;
}

STQEntry *
cq_dequeue_e(STQueue* queue)
{
    STQEntry *front;
    if (queue == NULL)
        return NULL;
    
    front = TAILQ_FIRST(&queue->head);
    if (front == NULL)
        return NULL;

    TAILQ_REMOVE(&queue->head, front, links);
    return front;
}

void
cq_enqueue_e(STQueue* queue, STQEntry* elem)
{
    if (queue == NULL)
        return;
    TAILQ_INSERT_HEAD(&queue->head, elem, links);
}

void 
cq_clear(STQueue* queue)
{
    STQEntry *entry, *next;

    entry = TAILQ_FIRST(&queue->head);
    while (entry != NULL)
    {
        next = TAILQ_NEXT(entry, links);
        pfree(entry);
        entry = next;
    }
    pfree(queue);
}
