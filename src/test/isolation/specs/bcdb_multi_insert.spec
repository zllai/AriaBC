# write in the same block should conflict 
# no conflict in different blocks

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
step "s1a0" { select bcdb_init(False, 3); }
step "s1a1" { select bcdb_tx_submit('{"hash": "1_0", "sql": "INSERT INTO foo VALUES(1, 1)"}'); }
step "s1a2"	{ select bcdb_block_submit('{"bid": 1, "txs": ["1_0"]}'); }

step "s1a3" { select bcdb_tx_submit('{"hash": "2_0", "sql": "INSERT INTO foo VALUES(2, 2)"}'); }
step "s1a4" { select bcdb_tx_submit('{"hash": "2_1", "sql": "INSERT INTO foo VALUES(2, 3)"}'); }
step "s1a5" { select bcdb_tx_submit('{"hash": "2_2", "sql": "INSERT INTO foo VALUES(2, 4)"}'); }
step "s1a6"	{ select bcdb_block_submit('{"bid": 2, "txs": ["2_0", "2_1", "2_2"]}'); }
step "s1a7" { select bcdb_tx_submit('{"hash": "3_0", "sql": "UPDATE foo SET value = 5 WHERE key = 2"}'); }
step "s1a8"	{ select bcdb_block_submit('{"bid": 3, "txs": ["3_0"]}'); }
step "s1a9" { SELECT bcdb_wait_to_finish(); }

step "s1a10" { select bcdb_check_block_status(0); }
step "s1a11" { select * from foo; }


permutation "s1a0" "s1a1" "s1a2" "s1a3" "s1a4" "s1a5" "s1a6" "s1a7" "s1a8" "s1a9" "s1a10" "s1a11"