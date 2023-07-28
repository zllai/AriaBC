# BCDB version of read-write-unique-3.spec

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

session "s1"
step "s1a1" { SHOW TRANSACTION ISOLATION LEVEL; }
step "s1s1"	{ select bcdb_tx_submit('{"block_id":1, "sql": "SELECT insert_unique(1, 1)", "hash":"1"}'); }
step "s1c1"	{ select bcdb_add_tx_with_block_id('1', 2); }
step "s1s2"	{ select bcdb_tx_submit('{"block_id":1, "sql": "SELECT insert_unique(1, 2)", "hash":"2"}'); }
step "s1c2"	{ select bcdb_add_tx_with_block_id('2', 2); }
step "s1b2"	{ select bcdb_allow_txs_commit_by_block_id(2); }
step "s1r1"	{ select bcdb_check_txs_result('1'); }
step "s1r2"	{ select bcdb_check_txs_result('2'); }

# Why the sequence care
permutation "s1a1" "s1s1" "s1s2" "s1c1" "s1c2" "s1b2" "s1r1" "s1r2"
