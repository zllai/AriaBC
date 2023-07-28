#include "bcdb/utils/concurrent_queue.h"
#include "bcdb/bcdb.h"
#include "utils/elog.h"

/* this file is abandoned, because we want to keep everything in single thread */

ConcurrentQueue *
create_cq(void)
{
    ConcurrentQueue *queue = bcdb_alloc(sizeof(*queue));
    queue->head.tqh_first = NULL;
    queue->head.tqh_last = &queue->head.tqh_first;
    TAILQ_INIT(&queue->head);
    pthread_mutex_init(&queue->lock, NULL);
    return queue;
}


CQEntry *
cq_enqueue_v(ConcurrentQueue* queue, void* value)
{
    CQEntry *entry;
    if (queue == NULL)
        return NULL;
    entry = bcdb_alloc(sizeof(*entry));
    pthread_mutex_lock(&queue->lock);
    entry->value = value;
    TAILQ_INSERT_TAIL(&queue->head, entry, links);
    pthread_mutex_unlock(&queue->lock);
    return entry;
}

void *
cq_dequeue_v(ConcurrentQueue* queue)
{
    CQEntry *front;
    void    *value;
    if (queue == NULL)
        return NULL;
    
    pthread_mutex_lock(&queue->lock);
    front = TAILQ_FIRST(&queue->head);
    if (front == NULL)
    {
        pthread_mutex_unlock(&queue->lock);
        return NULL;
    }
    value = front->value;
    TAILQ_REMOVE(&queue->head, front, links);
    pthread_mutex_unlock(&queue->lock);

    bcdb_free(front);
    return value;
}

CQEntry *
cq_dequeue_e(ConcurrentQueue* queue)
{
    CQEntry *front;
    if (queue == NULL)
        return NULL;
    
    pthread_mutex_lock(&queue->lock);
    front = TAILQ_FIRST(&queue->head);
    if (front == NULL)
    {
        pthread_mutex_unlock(&queue->lock);
        return NULL;
    }
    TAILQ_REMOVE(&queue->head, front, links);
    pthread_mutex_unlock(&queue->lock);
    return front;
}

void
cq_enqueue_e(ConcurrentQueue* queue, CQEntry* elem)
{
    if (queue == NULL)
        return;
    pthread_mutex_lock(&queue->lock);
    TAILQ_INSERT_HEAD(&queue->head, elem, links);
    pthread_mutex_unlock(&queue->lock);
}

void 
cq_clear(ConcurrentQueue* queue)
{
    CQEntry *entry, *next;

    entry = TAILQ_FIRST(&queue->head);
    while (entry != NULL)
    {
        next = TAILQ_NEXT(entry, links);
        bcdb_free(entry);
        entry = next;
    }
    pthread_mutex_destroy(&queue->lock);
    bcdb_free(queue);
}
