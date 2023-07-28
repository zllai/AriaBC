#ifndef BCDB_WORKER_H
#define BCDB_WORKER_H

#include "postgres.h"
#include <unistd.h>
#include <tcop/dest.h>
#include <utils/guc.h>
#include <tcop/tcopprot.h>
#include <pgstat.h>
#include <pg_trace.h>
#include <utils/memutils.h>
#include <utils/portal.h>
#include <utils/palloc.h>
#include <tcop/utility.h>
#include <utils/ps_status.h>
#include <miscadmin.h>
#include <utils/snapmgr.h>
#include <tcop/pquery.h>
#include <access/printtup.h>
#include "libpq/libpq.h"
#include "bcdb/shm_transaction.h"
#include "bcdb/shm_block.h"

bool bcdb_worker_init(void);
void bcdb_worker_process_tx(BCDBShmXact *tx);
void bcdb_on_worker_exit(int code, Datum arg);
BCBlockID GetCurrentTxBlockId(void);
BCBlockID GetCurrentTxBlockIdSnapshot(void);



#endif