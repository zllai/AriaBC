#ifndef BCDB_WORKER_CONTROLLER_H
#define BCDB_WORKER_CONTROLLER_H

#include "postgres.h"
#include "bcdb/utils/st_list.h"
#include "bcdb/utils/st_queue.h"
#include "../interfaces/libpq/libpq-fe.h"
#include "sys/queue.h"
#include "bcdb/globals.h"

/* connection parameters for worker backend */
#define WORKER_KEYWORDS {"dbname","host","port","options",NULL}
#define WORKER_VALUES {MyProcPort->database_name,bcdb_host,bcdb_port,"-c is_bcdb_worker=true",NULL}

typedef enum _worker_status
{
    WORKER_STATUS_BUSY,
    WORKER_STATUS_IDLE
} WorkerStatus;

typedef struct _WorkerController
{
    /* backend conn */
    PGconn       *conn;
    /* use backend pid as worker id*/
    int          id;
    /* backend sorket */
    int          socket;

    WorkerStatus status;

    LIST_ENTRY(_WorkerController)  link;
    
} WorkerController;

typedef struct 
{
    int     num;
    LIST_HEAD(WorkerList, _WorkerController) list;
    WorkerController *tail;
} IdleWorkerList;

extern IdleWorkerList    idle_workers;

extern void              idle_worker_list_init(int num);
extern WorkerController* get_idle_worker(void);
extern void              add_idle_worker(WorkerController* worker);

extern WorkerController* create_worker_controller(void);

/* execute a transaction on worker */
extern bool              worker_execute(WorkerController* worker, const char* tx);
extern bool              worker_start(WorkerController* worker);

/* finish current connection and reconnect */
extern bool              worker_restart(WorkerController* worker);

/* disconnect with backend and clean up */
extern void              worker_finish(WorkerController* worker);

#endif