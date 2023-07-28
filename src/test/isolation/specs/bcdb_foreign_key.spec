setup
{
  CREATE TABLE foo (
	key		int PRIMARY KEY,
	value	int
  );
  CREATE TABLE hoo (
    key     int PRIMARY KEY,
    rkey    int,
    FOREIGN KEY (rkey) REFERENCES foo(key)
  );
  INSERT INTO foo VALUES(1, 1);
  INSERT INTO hoo VALUES(1, 1);
}

teardown
{
  SELECT bcdb_reset();
  DROP TABLE foo CASCADE;
}

session "s1"
step "s1p1" { select bcdb_init(); }
step "s1a1"	{ select bcdb_tx_submit('{"block_id":0, "commit_block": 1, "id": 0, "sql": "UPDATE hoo SET rkey = 2 WHERE key = 1", "hash":"1_0"}'); }
step "s1a2"	{ select bcdb_tx_submit('{"block_id":0, "commit_block": 1, "id": 1, "sql": "UPDATE hoo SET rkey = 1 WHERE key = 1", "hash":"1_1"}'); }
step "s1a3"	{ select bcdb_tx_submit('{"block_id":0, "commit_block": 1, "id": 2, "sql": "INSERT INTO hoo VALUES(2, 2)", "hash":"1_2"}'); }

step "s1a5"	{ select bcdb_allow_txs_commit_by_block_id(1); }
step "s1a6" { select * from hoo; }
step "s1a7" { select * from foo; }
step "s1a8"	{ SELECT bcdb_check_block_status(1); }

permutation "s1p1" "s1a1" "s1a2" "s1a3" "s1a5" "s1a6" "s1a7" "s1a8"