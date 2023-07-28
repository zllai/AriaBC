# Assume tx1 insert (1,1) snapshot block 1 and commit @ block 2
# 		 tx2 insert (2,2) snapshot block 1 and commit @ block 3
# 		 tx3 update all record + 1 snapshot block 2
#			assert (1,1) => (1,2), (2,2) no change
#

setup
{
  CREATE TABLE foo (
	key		int PRIMARY KEY,
	value	int
  );
}

teardown
{
  SELECT bcdb_reset();
  DROP TABLE foo;
}

session "s1"
step "s1s0" { select bcdb_init(); }
step "s1s1"	{ select bcdb_tx_submit('{"block_id":0, "sql": "INSERT INTO foo VALUES(1, 1)", "hash":"1"}'); }
step "s1c1"	{ select bcdb_add_tx_with_block_id('1', 1); }
step "s1s2"	{ select bcdb_tx_submit('{"block_id":1, "sql": "INSERT INTO foo VALUES(2, 2) ", "hash":"2"}'); }
step "s1c2"	{ select bcdb_add_tx_with_block_id('2', 2); }

step "s1b2"	{ select bcdb_allow_txs_commit_by_block_id(1); }
step "s1b3"	{ select bcdb_allow_txs_commit_by_block_id(2); }

# due to block isolation, only key=1 is added
step "s1s3"	{ select bcdb_tx_submit('{"block_id":1, "sql": "UPDATE foo SET value = value + 1", "hash":"3"}'); }
step "s1c3"	{ select bcdb_add_tx_with_block_id('3', 3); }

step "s1b4"	{ select bcdb_allow_txs_commit_by_block_id(3); }

# step "s1r1" { select * from foo; }
# Test the index
step "s1r1" { select * from foo WHERE key = 1; }
step "s1r2" { select * from foo WHERE key = 2; }
step "s1r3"	{ select bcdb_check_txs_result('3'); }

permutation "s1s0" "s1s1" "s1c1" "s1b2" "s1s2" "s1c2" "s1b3" "s1s3" "s1c3" "s1b4" "s1r1" "s1r2" "s1r3"
