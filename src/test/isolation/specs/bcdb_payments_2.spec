
setup
{
  CREATE TABLE bank (
	account		int PRIMARY KEY,
	balance	    int
  );
  CREATE FUNCTION simple_pay(payer integer, payee integer, amount integer) RETURNS void AS $$
  DECLARE
    a integer;
    b integer;
  BEGIN
    SELECT balance INTO a FROM bank WHERE account = payer;
    SELECT balance INTO b FROM bank WHERE account = payee;
    a = a - amount;
    b = b + amount;
    IF a < 0 THEN 
      RAISE EXCEPTION 'insufficient balance';
    END IF;
    UPDATE bank SET balance = a WHERE account = payer;
    UPDATE bank SET balance = b WHERE account = payee;
  END;
  $$ LANGUAGE plpgsql;
  CREATE FUNCTION joint_pay(payer1 integer, payer2 integer, payee integer, amount1 integer, amount2 integer) RETURNS void AS $$
  DECLARE
    a integer;
    b integer;
    c integer;
    tid record;
  BEGIN
    SELECT balance INTO a FROM bank WHERE account = payer1;
    SELECT balance INTO b FROM bank WHERE account = payer2;
    SELECT balance INTO c FROM bank WHERE account = payee;
    a = a - amount1;
    b = b - amount2;
    c = c + amount1 + amount2;
    IF a < 0 OR b < 0 THEN 
      RAISE EXCEPTION 'insufficient balance';
    END IF;
    UPDATE bank SET balance = a WHERE account = payer1;
    UPDATE bank SET balance = b WHERE account = payer2;
    UPDATE bank SET balance = c WHERE account = payee;

  END;
  $$ LANGUAGE plpgsql;

INSERT INTO bank VALUES(0, 100);
INSERT INTO bank VALUES(1, 100);
INSERT INTO bank VALUES(2, 100);
INSERT INTO bank VALUES(3, 100);
INSERT INTO bank VALUES(4, 100);
INSERT INTO bank VALUES(5, 100);
INSERT INTO bank VALUES(6, 100);
INSERT INTO bank VALUES(7, 100);
INSERT INTO bank VALUES(8, 100);
INSERT INTO bank VALUES(9, 100);
INSERT INTO bank VALUES(10, 100);
INSERT INTO bank VALUES(11, 100);
INSERT INTO bank VALUES(12, 100);
INSERT INTO bank VALUES(13, 100);
INSERT INTO bank VALUES(14, 100);
INSERT INTO bank VALUES(15, 100);
INSERT INTO bank VALUES(16, 100);
INSERT INTO bank VALUES(17, 100);
INSERT INTO bank VALUES(18, 100);
INSERT INTO bank VALUES(19, 100);
INSERT INTO bank VALUES(20, 100);
INSERT INTO bank VALUES(21, 100);
INSERT INTO bank VALUES(22, 100);
INSERT INTO bank VALUES(23, 100);
INSERT INTO bank VALUES(24, 100);
INSERT INTO bank VALUES(25, 100);
INSERT INTO bank VALUES(26, 100);
INSERT INTO bank VALUES(27, 100);
INSERT INTO bank VALUES(28, 100);
INSERT INTO bank VALUES(29, 100);
INSERT INTO bank VALUES(30, 100);
INSERT INTO bank VALUES(31, 100);
INSERT INTO bank VALUES(32, 100);
INSERT INTO bank VALUES(33, 100);
INSERT INTO bank VALUES(34, 100);
INSERT INTO bank VALUES(35, 100);
INSERT INTO bank VALUES(36, 100);
INSERT INTO bank VALUES(37, 100);
INSERT INTO bank VALUES(38, 100);
INSERT INTO bank VALUES(39, 100);
INSERT INTO bank VALUES(40, 100);
INSERT INTO bank VALUES(41, 100);
INSERT INTO bank VALUES(42, 100);
INSERT INTO bank VALUES(43, 100);
INSERT INTO bank VALUES(44, 100);
INSERT INTO bank VALUES(45, 100);
INSERT INTO bank VALUES(46, 100);
INSERT INTO bank VALUES(47, 100);
INSERT INTO bank VALUES(48, 100);
INSERT INTO bank VALUES(49, 100);
SELECT ctid FROM bank WHERE account = 32;
SELECT ctid FROM bank WHERE account = 23;
}

teardown
{
  SELECT bcdb_reset();
  DROP TABLE bank;
  DROP FUNCTION simple_pay;
  DROP FUNCTION joint_pay;
}

session "s1"
step "s1p1" { select bcdb_init(True, 2); }
step "s1t2" { SELECT bcdb_tx_submit('{"hash": "1_0", "sql": "SELECT joint_pay(32, 23, 34, 57, 9)"}'); }
step "s1t3" { SELECT bcdb_tx_submit('{"hash": "1_1", "sql": "SELECT joint_pay(32, 23, 43, 80, 1)"}'); }
step "s1t4" { SELECT bcdb_block_submit('{"bid": 1, "txs": [ "1_0", "1_1" ]}'); }
step "s1t5" { SELECT bcdb_tx_submit('{"hash": "2_0", "sql": "SELECT joint_pay(2, 37, 43, 21, 56)"}'); }
step "s1t6" { SELECT bcdb_block_submit('{"bid": 2, "txs": [ "2_0" ]}'); }
step "s1t7" { SELECT bcdb_wait_to_finish(); }
step "s1t8" { SELECT * FROM bank; SELECT sum(balance) FROM bank; }
step "s1t9" { SELECT bcdb_check_block_status(1); }
step "s1t10" { SELECT bcdb_check_block_status(2); }

permutation "s1p1" "s1t2" "s1t3" "s1t4" "s1t5" "s1t6" "s1t7" "s1t8" "s1t9" "s1t10"
