setup
{
  CREATE TABLE foo (
	key		int PRIMARY KEY,
	value	int
  );
  INSERT INTO foo VALUES(1, 100);
  INSERT INTO foo VALUES(2, 100);
  CREATE FUNCTION withdraw(x integer, y integer) RETURNS void AS $$
  DECLARE
    a integer;
    b integer;
  BEGIN
    SELECT value INTO a FROM foo WHERE key = 1;
    SELECT value INTO b FROM foo WHERE key = 2;
    a = a - x;
    b = b - y;
    IF a + b < 0 THEN 
      ROLLBACK;
    END IF;
    IF x <> 0 THEN
      UPDATE foo SET value = a WHERE key = 1;
    END IF;
    IF y <> 0 THEN
      UPDATE foo SET value = b WHERE key = 2;
    END IF;
  END;
  $$ LANGUAGE plpgsql;
}

teardown
{
  SELECT bcdb_reset();
  DROP TABLE foo;
  DROP FUNCTIOn withdraw;
}

session "s1"
step "s1p1" { select bcdb_init(); }
step "s1a1"	{ select bcdb_tx_submit('{"block_id":0, "sql": "SELECT withdraw(200, 0)", "hash": "1"}' ); }
step "s1a2"	{ select bcdb_tx_submit('{"block_id":0, "sql": "SELECT withdraw(0, 200)", "hash": "2"}' ); }

step "s1a3"	{ select bcdb_add_tx_with_block_id('1', 1); }
step "s1a4"	{ select bcdb_add_tx_with_block_id('2', 1); }
step "s1a5"	{ select bcdb_allow_txs_commit_by_block_id(1); }
step "s1a6" { select * from foo; }
step "s1a7"	{ select bcdb_check_txs_result('1'); }
step "s1a8"	{ select bcdb_check_txs_result('2'); }

permutation "s1p1" "s1a1" "s1a2" "s1a3" "s1a4" "s1a5" "s1a6" "s1a7" "s1a8"