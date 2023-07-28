#include "postgres.h"
#include "bcdb/bcdb.h"
#include "bcdb/utils/concurrent_list.h"
#include "utils/memutils.h"

/* this file is abandoned because we want to keep everything is single thread */

ConcurrentList *
create_cl(void)
{
    ConcurrentList *list = bcdb_alloc(sizeof(*list));
    list->head.lh_first = NULL;
    LIST_INIT(&list->head);
    pthread_mutex_init(&list->lock, NULL);
    return list;
}

CLEntry *
cl_push_front_v(ConcurrentList *list, void *value)
{
    CLEntry* elem;
    if (!list)
        return NULL;

    elem = bcdb_alloc(sizeof(*elem));
    pthread_mutex_lock(&list->lock);
    elem->value = value;
    LIST_INSERT_HEAD(&list->head, elem, links);
    pthread_mutex_unlock(&list->lock);
    return elem;
}

void *
cl_pop_front_v(ConcurrentList *list)
{
    CLEntry *head;
    void    *value;
    if (!list)
        return NULL;
    pthread_mutex_lock(&list->lock);

    head = LIST_FIRST(&list->head);
    if (!head)
    {
        pthread_mutex_unlock(&list->lock);
        return NULL;
    }
    value = head->value;
    LIST_REMOVE(head, links);
    pthread_mutex_unlock(&list->lock);

    bcdb_free(head);
    return value;
}

void 
cl_remove(ConcurrentList *list, CLEntry* elem)
{
    LIST_REMOVE(elem, links);
    bcdb_free(elem);
}

void
cl_clear(ConcurrentList *list)
{
    CLEntry* elem;

    while((elem = LIST_FIRST(&list->head)))
    {
        LIST_REMOVE(elem, links);
        bcdb_free(elem);
    }

    pthread_mutex_destroy(&list->lock);
    bcdb_free(list);
}
