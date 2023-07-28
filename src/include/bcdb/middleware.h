//
// Created by Chris Liu on 16/3/2020.
//

#ifndef BLOCKCHAIN_DATABASE_MIDDLEWARE_H
#define BLOCKCHAIN_DATABASE_MIDDLEWARE_H

#include "postgres.h"
#include "bcdb/utils/cJSON.h"
#include "bcdb/shm_block.h"

#define END_COMMAND_MSG "tx scheduled"

//void bcdb_middleware_dummy_submit_tx(const char* file_path);
void bcdb_middleware_init(bool is_oep_mode, int32 block_size);
int bcdb_middleware_submit_tx(const char* tx_string);
void bcdb_middleware_submit_block(const char* block_json);
void bcdb_middleware_set_txs_committed_block(char * tx_hash, int32 block_id);
void bcdb_wait_tx_finish(char *tx_hash);
void bcdb_clear_block_txs_store(void);

void bcdb_middleware_allow_txs_exec_write_set_and_commit(BCBlock *block);
void allow_all_block_txs_to_commit(BCBlock *block);
void bcdb_middleware_allow_txs_exec_write_set_and_commit(BCBlock *block);
void bcdb_middleware_allow_txs_exec_write_set_and_commit_by_id(int32 id);
bool bcdb_is_tx_commited(char * tx_hash);
void bcdb_middleware_wait_all_to_finish(void);
void bcdb_middleware_conflict_check(BCBlock *block);
void block_cleaning(BCBlockID current_block_id);
#endif //BLOCKCHAIN_DATABASE_MIDDLEWARE_H
