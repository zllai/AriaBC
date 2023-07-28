# Similar to bcdb_same_blk_ssi_conflict.spec
# Since T1 and T2 are in different block
# No conflict should occur

setup
{
  CREATE TABLE test (
      key   integer UNIQUE,
      val   integer
    );
  CREATE OR REPLACE FUNCTION insert_unique(k integer, v integer) RETURNS void
    LANGUAGE SQL AS $$
      INSERT INTO test (key, val) SELECT k, v WHERE NOT EXISTS (SELECT key FROM test WHERE key = k);
    $$;
}

teardown
{
  SELECT bcdb_reset();
  DROP TABLE test;
}
#
# Assume block 1 insert 1 record
# 		 block 2 insert 1 record
# 		 block 3 update all record + 1 base on block 1
#
session "s1"
step "s1s1"	{ select bcdb_tx_submit('{"block_id":1, "sql": "SELECT insert_unique(1, 1)", "hash":"1"}'); }
step "s1c1"	{ select bcdb_add_tx_with_block_id('1', 2); }
step "s1s2"	{ select bcdb_tx_submit('{"block_id":2, "sql": "SELECT insert_unique(1, 2)", "hash":"2"}'); }
step "s1c2"	{ select bcdb_add_tx_with_block_id('2', 3); }
step "s1b2"	{ select bcdb_allow_txs_commit_by_block_id(2); }
step "s1b3"	{ select bcdb_allow_txs_commit_by_block_id(3); }
step "s1r1"	{ select bcdb_check_txs_result('1'); }
step "s1r2"	{ select bcdb_check_txs_result('2'); }

permutation "s1s1" "s1s2" "s1c1" "s1c2" "s1b2" "s1b3" "s1r1" "s1r2"
