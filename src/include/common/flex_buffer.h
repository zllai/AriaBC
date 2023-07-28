#ifndef FLEX_BUFFER_H
#define FLEX_BUFFER_H
#include "postgres_fe.h"

#define FLEX_PAGE_SIZE (8 * 1024) 

typedef struct
{
    char *buf;
    int cap;
    int size;
} FlexBuffer;

extern FlexBuffer* create_flex_buffer(int init_cap);
extern void flex_buffer_push(FlexBuffer *flex, char *data, int size);
extern void flex_buffer_add(FlexBuffer *flex, char data);
extern void flex_buffer_free(FlexBuffer *flex);
extern int flex_buffer_yield(FlexBuffer *flex, char **out_buf);
#endif