#include "common/flex_buffer.h"

int main()
{
    char data1[] = "123";
    char data2[] = "4567";
    char data3[FLEX_PAGE_SIZE] = "abc"; 
    char data4[FLEX_PAGE_SIZE+3] = "efg";
    FlexBuffer* flex = create_flex_buffer(FLEX_PAGE_SIZE);
    flex_buffer_push(flex, data1, strlen(data1));
    flex_buffer_push(flex, data2, sizeof(data2));
    if (strcmp(flex->buf, "1234567") != 0)
    {
        fprintf(stderr, _("failed in testcase 1: %s\n"), flex->buf);
        exit(1);
    }
    flex_buffer_push(flex, data3, sizeof(data3));
    flex_buffer_push(flex, data4, sizeof(data4));
    if (strcmp(flex->buf + strlen(data1) + sizeof(data2), "abc") != 0)
    {
        fprintf(stderr, _("failed in testcase 2: %s\n"), flex->buf + strlen(data1) + sizeof(data2));
        exit(1);
    }
    if (strcmp(flex->buf + FLEX_PAGE_SIZE + strlen(data1) + sizeof(data2), "efg") != 0)
    {   
        fprintf(stderr, _("failed in testcase 3: %s\n"), flex->buf + FLEX_PAGE_SIZE + strlen(data1) + sizeof(data2));
        exit(1);
    }
    if (flex->size != strlen(data1)+sizeof(data2)+sizeof(data3)+sizeof(data4))
    {
        fprintf(stderr, _("flex->size does not match\n"));
        exit(1);
    }
    if (flex->cap != FLEX_PAGE_SIZE * 3)
    {
        fprintf(stderr, _("flex->cap does not match\n"));
        exit(1);
    }
    return 0;
}