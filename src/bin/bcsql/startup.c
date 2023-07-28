#include "startup.h"
#include "getopt_long.h"
#include "signal.h"

#define PARAMS_ARRAY_SIZE 5

CMDOptions  options;
PGconn      *conn;

int
main(int argc, char **argv) 
{
    const char* keywords[PARAMS_ARRAY_SIZE];
    const char* values[PARAMS_ARRAY_SIZE];

    if (argc > 1)
    {
        if (strcmp(argv[1], "-?") == 0 || strcmp(argv[1], "--help") == 0)
        {
            show_help();
            exit(0);
        }
    }
    parse_cmd_potions(argc, argv);

    keywords[0] = "host";
    values[0] = options.host;
    keywords[1] = "port";
    values[1] = options.port;
    keywords[2] = "dbname";
    values[2] = options.dbname;
    keywords[3] = "options";
    values[3] = "-c is_bcdb_master=true";
    keywords[4] = NULL;
    values[4] = NULL;
    conn = PQconnectdbParams(keywords, values, true);

    if (PQstatus(conn) == CONNECTION_BAD)
    {
        fprintf(stderr, "Failed to connect to server: %s", PQerrorMessage(conn));
        exit(1);
    }

    PQsetNoticeProcessor(conn, notice_processor, NULL);

    signal(SIGINT, quit_cleaning);
    main_loop(stdin);
    return 0;
}

void
show_help(void)
{
    printf("usage:\n\t bcsql <-h host> <-p port> <-d dbname>\n");
}

void
notice_processor(void *arg, const char *message)
{
    fprintf(stderr, "[backend] %s", message);
}

void
quit_cleaning(int arg)
{
    PQfinish(conn);
    exit(0);
}

void
parse_cmd_potions(int argc, char **argv)
{
    static struct option long_options[] = 
    {
        {"host", required_argument, NULL, 'h'},
        {"port", required_argument, NULL, 'p'},
        {"dbname", required_argument, NULL, 'd'},
        {NULL, 0, NULL, 0}
    };

    int optindex;
    int c;
    memset(&options, 0, sizeof(options));
    while((c = getopt_long(argc, argv, "h:p:d:", long_options, &optindex)) != -1)
    {
        switch (c)
        {
            case 'h':
                options.host = pg_strdup(optarg);
                break;
            case 'p':
                options.port = pg_strdup(optarg);
                break;
            case 'd':
                options.dbname = pg_strdup(optarg);
                break;
            default:
                fprintf(stderr, "Invalid option %c", c);
                exit(1);
        }
    }
}

int
send_tx(char *tx)
{
    PGresult *result;
    result = PQexecBCTx(conn, tx);
    clear_result(result);
    pg_free(tx);
    return 1;
}

void
clear_result(PGresult *result)
{
    if (!result)
    {
        fprintf(stderr, "Failed to send tx: %s\n", PQerrorMessage(conn));
    }
    else
    {
        if (PQresultStatus(result) == PGRES_NONFATAL_ERROR || PQresultStatus(result) == PGRES_FATAL_ERROR)
        {
            fprintf(stderr, "Failed to send tx: %s\n", PQresultErrorMessage(result));
        }
        PQclear(result);
    }
}

void
main_loop(FILE *source)
{
    FlexBuffer  *flex = create_flex_buffer(FLEX_PAGE_SIZE);
    char        c;
    int         json_brackets = 0;
    char        *json_segment = NULL;

    while ((c = getc(source)) != EOF)
    {
        if (c == '{')
            json_brackets++;

        if (json_brackets > 0)
            flex_buffer_add(flex, c);

        if (c == '}')
        {
            json_brackets--;
            if (json_brackets == 0) 
            {
                flex_buffer_add(flex, '\0');
                flex_buffer_yield(flex, &json_segment);
                send_tx(json_segment);
            }
        }
    }
    flex_buffer_free(flex);
    quit_cleaning(0);
}
