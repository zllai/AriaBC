#include "common/flex_buffer.h"


FlexBuffer* 
create_flex_buffer(int init_cap)
{
    FlexBuffer* flex;

    init_cap = init_cap % FLEX_PAGE_SIZE ? (init_cap / FLEX_PAGE_SIZE + 1) * FLEX_PAGE_SIZE : init_cap;
    flex = pg_malloc(sizeof(FlexBuffer));
    flex->cap = init_cap;
    flex->size = 0;
    flex->buf = pg_malloc(init_cap);
    return flex;
}

void 
flex_buffer_push(FlexBuffer *flex, char *data, int size)
{
    if (size + flex->size > flex->cap)
    {
        int     new_cap;
        char*   new_buf;

        new_cap = ((flex->cap + size) / FLEX_PAGE_SIZE + 1) * FLEX_PAGE_SIZE;
        new_buf = pg_malloc(new_cap);
        memcpy(new_buf, flex->buf, flex->size);
        flex->buf = new_buf;
        flex->cap = new_cap;
    }
    memcpy(flex->buf + flex->size, data, size);
    flex->size += size;
}

void 
flex_buffer_add(FlexBuffer *flex, char data)
{
    if (flex->size + 1> flex->cap)
    {
        int     new_cap;
        char*   new_buf;

        new_cap = flex->cap + FLEX_PAGE_SIZE;
        new_buf = pg_malloc(new_cap);
        memcpy(new_buf, flex->buf, flex->size);
        flex->buf = new_buf;
        flex->cap = new_cap;
    }
    flex->buf[flex->size++] = data;
}

int
flex_buffer_yield(FlexBuffer *flex, char **out_buf)
{
    int out_size;

    *out_buf = flex->buf;
    out_size = flex->size;
    flex->buf = pg_malloc(FLEX_PAGE_SIZE);
    flex->cap = FLEX_PAGE_SIZE;
    flex->size = 0;
    return out_size;
}

void 
flex_buffer_free(FlexBuffer *flex)
{
    pg_free(flex->buf);
    pg_free(flex);
}
