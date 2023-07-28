#ifndef BCSQL_STARTUP_H
#define BCSQL_STARTUP_H
#include "postgres_fe.h"
#include "common/flex_buffer.h"
#include "stdio.h"
#include "libpq-fe.h"

typedef struct 
{
    char* host;
    char* port;
    char* dbname;
    char* test_dummy_block_file;
} CMDOptions;


void    show_help(void);
void    notice_processor(void *arg, const char *message);
void    parse_cmd_potions(int argc, char **argv);
int     send_tx(char *tx);
void    main_loop(FILE *source);
void    quit_cleaning(int);
void    clear_result(PGresult *result);

#endif