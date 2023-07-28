#ifndef BCDB_CONCURRENT_LIST_H
#define BCDB_CONCURRENT_LIST_H

#include "sys/queue.h"
#include "pthread.h"

typedef struct _CLEntry
{
    void*                   value;
    LIST_ENTRY(_CLEntry)    links;
} CLEntry;


typedef struct 
{
    LIST_HEAD(CLHead, _CLEntry) head;
    pthread_mutex_t             lock;

} ConcurrentList;

#define cl_entry_value(x) x->value;

extern ConcurrentList *create_cl(void);
extern CLEntry *cl_push_front_v(ConcurrentList *list, void *value);
extern void *cl_pop_front_v(ConcurrentList *list);
extern void cl_remove(ConcurrentList *list, CLEntry* elem);
extern void cl_clear(ConcurrentList *list);
#endif