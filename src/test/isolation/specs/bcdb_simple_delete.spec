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
#
# Assume block 1 insert 1 record
# 		 block 2 insert 1 record
# 		 block 3 update all record + 1 base on block 1
#
session "s1"
step "s1s1"	{ select bcdb_tx_submit('{"block_id":1, "sql": "INSERT INTO foo VALUES(1, 1)", "hash":"1"}'); }
step "s1c1"	{ select bcdb_add_tx_with_block_id('1', 2); }
step "s1s2"	{ select bcdb_tx_submit('{"block_id":2, "sql": "DELETE FROM foo WHERE key = 1", "hash":"2"}'); }
step "s1c2"	{ select bcdb_add_tx_with_block_id('2', 3); }

step "s1b2"	{ select bcdb_allow_txs_commit_by_block_id(2); }
step "s1b3"	{ select bcdb_allow_txs_commit_by_block_id(3); }

step "s1r1" { select key, value FROM foo WHERE key = 1; }

permutation "s1s1" "s1c1" "s1b2" "s1r1" "s1s2" "s1c2" "s1b3" "s1r1"
