#ifndef BCDB_STLIST_H
#define BCDB_STLIST_H

#include "sys/queue.h"

typedef struct _STLEntry
{
    void*                    value;
    LIST_ENTRY(_STLEntry)    links;
} STLEntry;


typedef struct 
{
    LIST_HEAD(STLHead, _STLEntry) head;
} STList;

#define stl_entry_value(x) x->value;

extern STList *create_stl(void);
extern void stl_init(STList *list);
extern STLEntry *stl_push_front_v(STList *list, void *value);
extern void stl_push_front_e(STList *list, STLEntry *entry);
extern void *stl_pop_front_v(STList *list);
extern STLEntry *stl_pop_front_e(STList *list);
extern void stl_remove(STList *list, STLEntry* elem);
extern void stl_clear(STList *list);
#endif