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
}
teardown
{

  SELECT bcdb_reset();
  DROP TABLE bank;
  DROP FUNCTION simple_pay;
  DROP FUNCTION joint_pay;

}

session "s1"

step "s1a0" { SELECT bcdb_init(); }
step "s1a1" { SELECT bcdb_block_submit('{"txs": ["SELECT simple_pay(48, 26, 6)", "SELECT simple_pay(32, 31, 52)", "SELECT simple_pay(19, 30, 46)", "SELECT simple_pay(13, 32, 18)", "SELECT simple_pay(48, 6, 80)", "SELECT simple_pay(34, 45, 78)", "SELECT simple_pay(19, 6, 47)", "SELECT joint_pay(43, 21, 30, 72, 13)", "SELECT simple_pay(20, 39, 82)", "SELECT simple_pay(35, 30, 57)"]}'); }
step "s1a2" { SELECT bcdb_block_submit('{"txs": ["SELECT simple_pay(16, 3, 71)", "SELECT simple_pay(5, 46, 52)", "SELECT simple_pay(42, 40, 1)", "SELECT simple_pay(21, 15, 42)", "SELECT simple_pay(4, 12, 73)", "SELECT simple_pay(9, 34, 58)", "SELECT joint_pay(20, 32, 31, 4, 39)", "SELECT simple_pay(45, 7, 141)", "SELECT simple_pay(34, 13, 78)", "SELECT simple_pay(18, 28, 12)"]}'); }
step "s1a3" { SELECT bcdb_block_submit('{"txs": ["SELECT simple_pay(24, 20, 74)", "SELECT simple_pay(11, 12, 24)", "SELECT joint_pay(42, 16, 30, 9, 3)", "SELECT simple_pay(8, 9, 5)", "SELECT simple_pay(44, 34, 88)", "SELECT simple_pay(45, 33, 18)", "SELECT simple_pay(15, 13, 108)", "SELECT simple_pay(28, 31, 85)", "SELECT simple_pay(44, 22, 2)", "SELECT simple_pay(7, 31, 151)"]}'); }
step "s1r1"	{ select bcdb_check_block_status(1); }
step "s1a4" { SELECT bcdb_block_submit('{"txs": ["SELECT simple_pay(12, 15, 5)", "SELECT simple_pay(7, 45, 29)", "SELECT simple_pay(10, 21, 55)", "SELECT simple_pay(6, 9, 219)", "SELECT simple_pay(2, 36, 82)", "SELECT simple_pay(34, 38, 88)", "SELECT joint_pay(7, 40, 12, 39, 74)", "SELECT joint_pay(5, 23, 7, 3, 78)", "SELECT joint_pay(11, 45, 7, 62, 14)", "SELECT simple_pay(3, 43, 6)"]}'); }
step "s1r2"	{ select bcdb_check_block_status(2); }
step "s1a5" { SELECT bcdb_block_submit('{"txs": ["SELECT simple_pay(39, 6, 67)", "SELECT joint_pay(4, 41, 19, 12, 56)", "SELECT joint_pay(32, 29, 2, 20, 13)", "SELECT simple_pay(25, 12, 34)", "SELECT simple_pay(46, 30, 146)", "SELECT joint_pay(43, 13, 49, 4, 82)", "SELECT simple_pay(21, 33, 33)", "SELECT joint_pay(28, 42, 11, 1, 61)", "SELECT simple_pay(36, 32, 80)", "SELECT simple_pay(24, 42, 9)"]}'); }
step "s1a6" { SELECT bcdb_wait_to_finish(); }
step "s1r3"	{ select bcdb_check_block_status(3); }
step "s1r4"	{ select bcdb_check_block_status(4); }
step "s1r5"	{ select bcdb_check_block_status(5); }
step "s1a7" { SELECT * FROM bank ORDER BY account; SELECT sum(balance) FROM bank; }

permutation "s1a0" "s1a1" "s1a2" "s1a3" "s1r1" "s1a4" "s1r2" "s1a5" "s1a6" "s1r3" "s1r4" "s1r5" "s1a7"
