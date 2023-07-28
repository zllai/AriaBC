//
// Created by Chris Liu on 2/6/2020.
//

#ifndef BLOCKCHAIN_DATABASE_FUNC_H
#define BLOCKCHAIN_DATABASE_FUNC_H

#include "postgres.h"
#include "fmgr.h"

extern Datum bcdb_tx_submit(PG_FUNCTION_ARGS);
extern Datum bcdb_add_tx_with_block_id(PG_FUNCTION_ARGS);
extern Datum bcdb_allow_txs_commit_by_block_id(PG_FUNCTION_ARGS);
extern Datum bcdb_check_txs_result(PG_FUNCTION_ARGS);
extern Datum bcdb_reset(PG_FUNCTION_ARGS);
extern Datum bcdb_init(PG_FUNCTION_ARGS);
extern Datum bcdb_check_block_status(PG_FUNCTION_ARGS);
extern Datum bcdb_block_submit(PG_FUNCTION_ARGS);
extern Datum bcdb_wait_to_finish(PG_FUNCTION_ARGS);
extern Datum bcdb_num_committed(PG_FUNCTION_ARGS);
extern Datum bcdb_verify(PG_FUNCTION_ARGS);



#endif //BLOCKCHAIN_DATABASE_FUNC_H
