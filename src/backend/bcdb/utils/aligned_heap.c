#include "bcdb/utils/aligned_heap.h"
#include "stdio.h"
#include "string.h"
#include "stdlib.h"

#define BITS_PER_UNIT 64
#define BITS_PER_L2   32
#define BITS_PER_L3   8
#define L2_PER_UNIT   (BITS_PER_UNIT/BITS_PER_L2)
#define L3_PER_UNIT   (BITS_PER_UNIT/BITS_PER_L3)
#define L3_PER_L2     (BITS_PER_L2/BITS_PER_L3)
const uint64_t  L1_ALL_ONES = (~(uint64_t)0);
const uint32_t  L2_ALL_ONES = (~(uint32_t)0);
const uint8_t   L3_ALL_ONES = (~(uint8_t)0);

/* ceil(x / (float)y) = (x + y - 1) / y */
#define div_ceil(x, y) ((x + y - 1) / y)
#define div_floor(x, y) (x / y)

static int search_free_space(AlignedHeap* heap, uint32_t *bitmap_ori, uint32_t **bitmap_pos);


AlignedHeap *
create_aligend_heap(void* heap_base, size_t heap_size, size_t slot_size)
{
    AlignedHeap        *heap       = heap_base;
    size_t             header_size = sizeof(*heap);
    /* type casting here is just to make compiler happy */
    union _bitmap_unit *bitmap     = (union _bitmap_unit*)((char *)heap_base + header_size);
    size_t             occupied_slots;
    int                idx         = 0;

    heap->slot_size = slot_size;
    heap->num_slots  = div_floor(heap_size, slot_size);
    heap->num_units = div_ceil(heap->num_slots, BITS_PER_UNIT);
    heap->meta_size        = header_size + heap->num_units * sizeof(*bitmap);
    occupied_slots   = div_ceil(heap->meta_size, slot_size); 

    if (heap_size <= occupied_slots * slot_size)
        return NULL;

    heap->num_slots -= occupied_slots;
    memset(bitmap, 0, heap->num_units * sizeof(*bitmap));

    while(idx < occupied_slots)
    {
        if (idx % BITS_PER_UNIT == 0 && (occupied_slots - idx) > BITS_PER_UNIT)
        {
            bitmap[idx / BITS_PER_UNIT].l1 = L1_ALL_ONES;
            idx += BITS_PER_UNIT;
        } 
        else if (idx % BITS_PER_L2 == 0 && (occupied_slots - idx) > BITS_PER_L2)
        {
            bitmap[idx / BITS_PER_UNIT].l2[idx % BITS_PER_UNIT / BITS_PER_L2] = L2_ALL_ONES;
            idx += BITS_PER_L2;
        }
        else if (idx % BITS_PER_L3 == 0 && (occupied_slots - idx) > BITS_PER_L3)
        {
            bitmap[idx / BITS_PER_UNIT].l3[idx % BITS_PER_UNIT / BITS_PER_L3] = L3_ALL_ONES;
            idx += BITS_PER_L3;
        }
        else
        {
            bitmap[idx / BITS_PER_UNIT].l3[idx % BITS_PER_UNIT / BITS_PER_L3] 
                                    = ~(L3_ALL_ONES << (occupied_slots - idx));
            idx = occupied_slots;
        }
    }

    return heap;
}

static int
search_free_space(AlignedHeap* heap, uint32_t *bitmap_ori, uint32_t **bitmap_pos)
{
    union _bitmap_unit  *bitmap = (union _bitmap_unit*)(heap + 1);
    union _bitmap_unit  bitmap_r;
    int                 l1_idx;
    int                 l2_idx;
    int                 l3_idx;

    for (l1_idx = 0; l1_idx < heap->num_units; l1_idx++)
    {
        bitmap_r.l1 = ~bitmap[l1_idx].l1;
        if (bitmap_r.l1)
        {
            l2_idx = bitmap_r.l2[0] ? 0 : 1;
            for (l3_idx = l2_idx * L3_PER_L2; l3_idx < L3_PER_UNIT; l3_idx++)
            {
                if (bitmap_r.l3[l3_idx])
                {
                    *bitmap_pos = &bitmap[l1_idx].l2[l2_idx];
                    *bitmap_ori = **bitmap_pos;
                    /* update bitmap_r here to make it consistent with bitmap_ori*/
                    bitmap_r.l2[l2_idx] = ~(*bitmap_ori);
                    if (bitmap_r.l3[l3_idx] & (uint8_t)1 << 0) return l1_idx * BITS_PER_UNIT + l3_idx * BITS_PER_L3 + 0;
                    if (bitmap_r.l3[l3_idx] & (uint8_t)1 << 1) return l1_idx * BITS_PER_UNIT + l3_idx * BITS_PER_L3 + 1;
                    if (bitmap_r.l3[l3_idx] & (uint8_t)1 << 2) return l1_idx * BITS_PER_UNIT + l3_idx * BITS_PER_L3 + 2;
                    if (bitmap_r.l3[l3_idx] & (uint8_t)1 << 3) return l1_idx * BITS_PER_UNIT + l3_idx * BITS_PER_L3 + 3;
                    if (bitmap_r.l3[l3_idx] & (uint8_t)1 << 4) return l1_idx * BITS_PER_UNIT + l3_idx * BITS_PER_L3 + 4;
                    if (bitmap_r.l3[l3_idx] & (uint8_t)1 << 5) return l1_idx * BITS_PER_UNIT + l3_idx * BITS_PER_L3 + 5;
                    if (bitmap_r.l3[l3_idx] & (uint8_t)1 << 6) return l1_idx * BITS_PER_UNIT + l3_idx * BITS_PER_L3 + 6;
                    if (bitmap_r.l3[l3_idx] & (uint8_t)1 << 7) return l1_idx * BITS_PER_UNIT + l3_idx * BITS_PER_L3 + 7;
                }
            }
        }
    }
    return -1;
}

void *
ah_alloc(AlignedHeap* heap)
{
    uint32_t             bitmap_ori;
    uint32_t             *bitmap_pos;
    uint32_t             bitmap_swap;
    int                 free_idx;
 
    do
    {
        free_idx = search_free_space(heap, &bitmap_ori, &bitmap_pos);
        if (free_idx < 0)
            return NULL;
        bitmap_swap = bitmap_ori | (uint32_t)1  << (free_idx % BITS_PER_L2);

    } while (!__sync_bool_compare_and_swap(bitmap_pos, bitmap_ori, bitmap_swap));
    
    return (char*)heap + heap->slot_size * free_idx;
}

bool
ah_free(AlignedHeap* heap, void* p)
{
    union _bitmap_unit  *bitmap  = (union _bitmap_unit*)(heap + 1);
    uint32_t            bitmap_ori;
    uint32_t            bitmap_swap;
    uint32_t            *bitmap_pos;
    int                 free_idx = ((char*)p - (char*)heap) / heap->slot_size;

    if (free_idx < div_ceil(heap->meta_size, heap->slot_size) || free_idx >= heap->num_slots || ((char*)p - (char*)heap) % heap->slot_size != 0)
        return false;
    
    do
    {
        bitmap_pos = &bitmap[free_idx / BITS_PER_UNIT].l2[free_idx % BITS_PER_UNIT / BITS_PER_L2];
        bitmap_ori = *bitmap_pos;
        bitmap_swap = bitmap_ori & ~((uint32_t)1 << free_idx % BITS_PER_L2);
    } while (!__sync_bool_compare_and_swap(bitmap_pos, bitmap_ori, bitmap_swap));
    
    return true;
}


