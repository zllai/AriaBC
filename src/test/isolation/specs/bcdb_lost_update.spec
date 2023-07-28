
setup
{
  CREATE TABLE foo (
	key		int PRIMARY KEY,
	value	int
  );
  INSERT INTO foo VALUES(1, 1);
  INSERT INTO foo VALUES(2, 1);
}

teardown
{
  SELECT bcdb_reset();
  DROP TABLE foo;
}

session "s1"
step "s1p1" { select bcdb_init(TRUE); }
step "s1a1" { select bcdb_tx_submit('{"hash": "1_0", "sql": "UPDATE foo SET value = 2 WHERE key = 1"}'); }
step "s1a2" { select bcdb_tx_submit('{"hash": "1_1", "sql": "UPDATE foo SET value = 3 WHERE key = 1"}'); }
step "s1a3"	{ select bcdb_block_submit('{"bid":1, "txs": ["1_0", "1_1"]}'); }
step "s1a4" { select bcdb_tx_submit('{"hash": "2_0", "sql": "UPDATE foo SET value = 5 WHERE key = 2"}'); }
step "s1a5" { select bcdb_block_submit('{"bid": 2, "txs": ["2_0"]}'); }
step "s1a6" { select bcdb_tx_submit('{"hash": "3_0", "sql": "UPDATE foo SET value = 6 WHERE key = 2"}'); }
step "s1a7" { select bcdb_block_submit('{"bid": 3, "txs": ["3_0"]}'); }
step "s1a8" { SELECT bcdb_wait_to_finish(); }
step "s1a9"	{ select bcdb_check_block_status(1); }
step "s1a10" { select * from foo WHERE key = 1; select * from foo WHERE key = 2; }

permutation "s1p1" "s1a1" "s1a2" "s1a3" "s1a4" "s1a5" "s1a6" "s1a7" "s1a8" "s1a9" "s1a10"