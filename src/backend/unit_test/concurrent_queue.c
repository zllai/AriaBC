#include "bcdb/utils/concurrent_queue.h"
#include "stdio.h"

int
main()
{
	MemoryContextInit();
    ConcurrentQueue *cq = create_cq();
    cq_enqueue(cq, (void*) 1);
    cq_enqueue(cq, (void*) 2);
    cq_enqueue(cq, (void*) 3);
    int r = (int)cq_dequeue(cq);
    if (r != 1)
    {
        printf("dequeue error, expected: %d get: %d\n", 1, r);
        exit(1);
    }
    r = (int)cq_dequeue(cq);
    if (r != 2)
    {
        printf("dequeue error, expected: %d get: %d\n", 2, r);
        exit(1);
    }
    r = (int)cq_dequeue(cq);
    if (r != 3)
    {
        printf("dequeue error, expected: %d get: %d\n", 3, r);
        exit(1);
    }
    void* nr = cq_dequeue(cq);
    if (nr != NULL)
    {
        printf("dequeue error, expected: NULL get: %X\n",  nr);
        exit(1);
    }
    nr = cq_dequeue(cq);
    if (nr != NULL)
    {
        printf("dequeue error, expected: NULL get: %X\n",  nr);
        exit(1);
    }
    nr = cq_dequeue(cq);
    if (nr != NULL)
    {
        printf("dequeue error, expected: NULL get: %X\n",  nr);
        exit(1);
    }

    cq_enqueue(cq, (void*) 3);
    if ((int)cq_dequeue(cq) != 3)
    {
        printf("dequeue error after empty, expected: %d\n", 3);
        exit(1);
    }

    cq_clear(cq);
    return 0;
    
}