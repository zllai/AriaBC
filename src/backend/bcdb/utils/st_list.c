#include "postgres.h"
#include "bcdb/utils/st_list.h"
#include "utils/memutils.h"

/* this file is abandoned */

STList *
create_stl(void)
{
    STList *list = palloc(sizeof(*list));
    stl_init(list);
    return list;
}

void
stl_init(STList *list)
{
    LIST_INIT(&list->head);
}

void
stl_push_front_e(STList *list, STLEntry *entry)
{
    if (!list)
        return;
    LIST_INSERT_HEAD(&list->head, entry, links);
}

STLEntry *
stl_push_front_v(STList *list, void *value)
{
    STLEntry* elem;
    if (!list)
        return NULL;

    elem = palloc(sizeof(*elem));
    elem->value = value;
    LIST_INSERT_HEAD(&list->head, elem, links);
    return elem;
}

STLEntry *
stl_pop_front_e(STList *list)
{
    STLEntry *head;
    head = LIST_FIRST(&list->head);
    if (!head)
        return NULL;
    LIST_REMOVE(head, links);
    return head;
}

void *
stl_pop_front_v(STList *list)
{
    STLEntry *head;
    void     *value;
    if (!list)
        return NULL;

    head = LIST_FIRST(&list->head);
    if (!head)
        return NULL;

    value = head->value;
    LIST_REMOVE(head, links);

    pfree(head);
    return value;
}

void 
stl_remove(STList *list, STLEntry* elem)
{
    LIST_REMOVE(elem, links);
}

void
stl_clear(STList *list)
{
    STLEntry* elem;

    while((elem = LIST_FIRST(&list->head)))
    {
        LIST_REMOVE(elem, links);
        pfree(elem);
    }
    pfree(list);
}
