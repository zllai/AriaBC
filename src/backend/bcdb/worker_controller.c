#include "bcdb/worker_controller.h"
#include "bcdb/shm_transaction.h"
#include "bcdb/shm_block.h"
#include "bcdb/globals.h"
#include "utils/elog.h"
#include "libpq/libpq-be.h"
#include "miscadmin.h"
#include "pgstat.h"

IdleWorkerList idle_workers;

void
idle_worker_list_init(int num)
{
    WorkerController *worker;
    LIST_INIT(&idle_workers.list);
    worker = create_worker_controller();
    LIST_INSERT_HEAD(&idle_workers.list, worker, link);
    idle_workers.tail = worker;
    if (!worker_start(worker))
        ereport(FATAL, (errmsg("[ZL] Cannot start worker")));
    for (idle_workers.num = 1; idle_workers.num < num; idle_workers.num++)
    {
        worker = create_worker_controller();
        LIST_INSERT_AFTER(idle_workers.tail, worker, link);
        idle_workers.tail = worker;
        if (!worker_start(worker))
            ereport(FATAL, (errmsg("[ZL] Cannot start worker")));
    }
}

WorkerController*
get_idle_worker()
{
    WorkerController *worker;
    if (idle_workers.num == 0)
    {
        worker = create_worker_controller();
        DEBUGNOCHECK("[ZL] create new idle worker (id: %d), num: %d", worker->id, idle_workers.num);
        return worker;
    }
    else
    {
        worker = LIST_FIRST(&idle_workers.list);
        LIST_REMOVE(worker, link);
        idle_workers.num--;
        DEBUGNOCHECK("[ZL] get an idle worker from the list (id: %d), num: %d", worker->id, idle_workers.num);
        return worker;
    }
}

void
add_idle_worker(WorkerController* worker)
{
    if (idle_workers.num == 0)
        LIST_INSERT_HEAD(&idle_workers.list, worker, link);
    else 
        LIST_INSERT_AFTER(idle_workers.tail, worker, link);

    idle_workers.tail = worker;
    idle_workers.num++;

    DEBUGNOCHECK("[ZL] add worker back to list (id: %d), num: %d", worker->id, idle_workers.num);
}

WorkerController* 
create_worker_controller(void)
{
    static int worker_counter = 0;
    char config_string[258];
    const char *keywords[]  = {"dbname","host","port","options",NULL};
    const char *values[]    = {MyProcPort->database_name,bcdb_host,bcdb_port,config_string,NULL};
    WorkerController* worker = palloc(sizeof(*worker));
    sprintf(config_string, "-c is_bcdb_worker=true -c OEP_mode=%s -c blocksize=%d -c worker_id=%d", OEP_mode ? "true":"false", blocksize, worker_counter++);

    worker->status      = WORKER_STATUS_IDLE;
    worker->conn        = PQconnectdbParams(keywords, values, true);

    if (PQstatus(worker->conn) == CONNECTION_BAD)
    {
        PQfinish(worker->conn);
        pfree(worker);
        ereport(ERROR,
                (errmsg("[ZL] Cannot start worker")));
        return NULL;
    }

    /* connection success */
    worker->id      = PQbackendPID(worker->conn);
    worker->socket  = PQsocket(worker->conn);

    return worker;
}

bool
worker_start(WorkerController* worker)
{
    return worker_execute(worker, "dummy");
}

bool 
worker_execute(WorkerController* worker, const char* tx_hash)
{

    /* wait and discard the result of previous query */
    PQexecFinish(worker->conn);
    if (!PQexecStart(worker->conn))
    {
        ereport(ERROR,
            (errmsg("[ZL] cannot prepare to send tx(%s) to worker(%d): %s", tx_hash, worker->id, PQerrorMessage(worker->conn))));
        return false;
    }
    if (!PQsendBCTx(worker->conn, tx_hash))
    {
        ereport(ERROR,
            (errmsg("[ZL] cannot send tx(%s) to worker(%d): %s", tx_hash, worker->id, PQerrorMessage(worker->conn))));
        return false;
    }
    return true;
}

bool
worker_restart(WorkerController* worker)
{
    const char *keywords[]  = WORKER_KEYWORDS;
    const char *values[]    = WORKER_VALUES;
 
    worker->conn = PQconnectdbParams(keywords, values, true);
    if (PQstatus(worker->conn) == CONNECTION_BAD)
    {
        ereport(ERROR, 
            (errmsg("[ZL] Cannot restart worker")));
        PQfinish(worker->conn);
        return false;
    }

    /* connection success */
    worker->id      = PQbackendPID(worker->conn);
    worker->socket  = PQsocket(worker->conn);
    return true;
}

void
worker_finish(WorkerController *worker)
{
    if (worker)
        PQfinish(worker->conn);
}