#ifndef BCDB_ALIGNED_HEAP_H
#define BCDB_ALIGNED_HEAP_H

#include "stdbool.h"
#include "stdint.h"
#include "stddef.h"

/*
 * A bit map based dynamic memory management module.
 * different from malloc, each data item is in fixed length.
 * it is mainly used for shared memory management.
 */


/*
 * bitmap is composed of bitmap_units. each unit is 64 bit, and further divided to smaller segement
 * this design is for fast searching free spaces
 * search from l1, if not all one (have free spaces), find that in l2...and l3
 */
union _bitmap_unit {
    uint64_t    l1;
    uint32_t    l2[2];
    uint8_t     l3[8];
};

/* this struct is actually the header struct */
typedef struct
{
    int                 num_slots;
    size_t              slot_size;
    size_t              num_units;
    size_t              meta_size;
} AlignedHeap;

extern AlignedHeap  *create_aligend_heap(void* heap_base, size_t heap_size, size_t slot_size);
extern void         *ah_alloc(AlignedHeap* heap);
extern bool         ah_free(AlignedHeap* heap, void* p);

#endif