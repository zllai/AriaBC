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
step "s1a4" { SELECT bcdb_check_block_status(1); }
step "s1a5" { SELECT bcdb_block_submit('{"txs": ["SELECT simple_pay(12, 15, 5)", "SELECT simple_pay(7, 45, 29)", "SELECT simple_pay(10, 21, 55)", "SELECT simple_pay(6, 9, 219)", "SELECT simple_pay(2, 36, 82)", "SELECT simple_pay(34, 38, 88)", "SELECT joint_pay(7, 40, 12, 39, 74)", "SELECT joint_pay(5, 23, 7, 3, 78)", "SELECT joint_pay(11, 45, 7, 62, 14)", "SELECT simple_pay(3, 43, 6)"]}'); }
step "s1a6" { SELECT bcdb_check_block_status(2); }
step "s1a7" { SELECT bcdb_block_submit('{"txs": ["SELECT simple_pay(39, 6, 67)", "SELECT joint_pay(4, 41, 19, 12, 56)", "SELECT joint_pay(32, 29, 2, 20, 13)", "SELECT simple_pay(25, 12, 34)", "SELECT simple_pay(46, 30, 146)", "SELECT joint_pay(43, 13, 49, 4, 82)", "SELECT simple_pay(21, 33, 33)", "SELECT joint_pay(28, 42, 11, 1, 61)", "SELECT simple_pay(36, 32, 80)", "SELECT simple_pay(24, 42, 9)"]}'); }
step "s1a8" { SELECT bcdb_check_block_status(3); }
step "s1a9" { SELECT bcdb_block_submit('{"txs": ["SELECT joint_pay(44, 0, 29, 2, 43)", "SELECT simple_pay(34, 17, 1)", "SELECT simple_pay(30, 22, 313)", "SELECT simple_pay(22, 37, 325)", "SELECT simple_pay(8, 45, 40)", "SELECT simple_pay(26, 41, 11)", "SELECT joint_pay(12, 44, 21, 82, 4)", "SELECT simple_pay(28, 24, 23)", "SELECT simple_pay(36, 26, 5)", "SELECT simple_pay(44, 36, 4)"]}'); }
step "s1a10" { SELECT bcdb_check_block_status(4); }
step "s1a11" { SELECT bcdb_block_submit('{"txs": ["SELECT simple_pay(45, 2, 22)", "SELECT simple_pay(16, 44, 6)", "SELECT simple_pay(31, 35, 310)", "SELECT simple_pay(2, 31, 42)", "SELECT simple_pay(29, 3, 107)", "SELECT joint_pay(40, 5, 46, 5, 1)", "SELECT simple_pay(43, 26, 11)", "SELECT joint_pay(0, 45, 48, 1, 44)", "SELECT simple_pay(6, 12, 16)", "SELECT simple_pay(12, 19, 144)"]}'); }
step "s1a12" { SELECT bcdb_check_block_status(5); }
step "s1a13" { SELECT bcdb_block_submit('{"txs": ["SELECT simple_pay(11, 6, 61)", "SELECT simple_pay(25, 40, 11)", "SELECT joint_pay(28, 7, 16, 1, 168)", "SELECT simple_pay(41, 22, 8)", "SELECT simple_pay(17, 1, 6)", "SELECT joint_pay(43, 16, 35, 11, 94)", "SELECT simple_pay(2, 47, 31)", "SELECT simple_pay(41, 31, 46)", "SELECT simple_pay(29, 40, 14)", "SELECT simple_pay(34, 11, 1)"]}'); }
step "s1a14" { SELECT bcdb_check_block_status(6); }
step "s1a15" { SELECT bcdb_block_submit('{"txs": ["SELECT simple_pay(18, 0, 18)", "SELECT joint_pay(21, 23, 45, 24, 11)", "SELECT simple_pay(17, 10, 20)", "SELECT simple_pay(18, 23, 51)", "SELECT simple_pay(8, 18, 8)", "SELECT simple_pay(15, 3, 20)", "SELECT joint_pay(33, 46, 4, 78, 7)", "SELECT simple_pay(19, 26, 28)", "SELECT joint_pay(30, 21, 7, 123, 30)", "SELECT simple_pay(27, 2, 39)"]}'); }
step "s1a16" { SELECT bcdb_check_block_status(7); }
step "s1a17" { SELECT bcdb_block_submit('{"txs": ["SELECT simple_pay(43, 9, 3)", "SELECT simple_pay(24, 40, 6)", "SELECT joint_pay(5, 12, 47, 15, 16)", "SELECT simple_pay(6, 25, 72)", "SELECT simple_pay(28, 31, 1)", "SELECT simple_pay(23, 14, 17)", "SELECT simple_pay(10, 27, 25)", "SELECT simple_pay(4, 44, 4)", "SELECT simple_pay(28, 48, 1)", "SELECT joint_pay(25, 16, 13, 83, 6)"]}'); }
step "s1a18" { SELECT bcdb_check_block_status(8); }
step "s1a19" { SELECT bcdb_block_submit('{"txs": ["SELECT simple_pay(13, 39, 75)", "SELECT joint_pay(29, 24, 23, 9, 10)", "SELECT joint_pay(38, 31, 9, 145, 104)", "SELECT simple_pay(27, 33, 64)", "SELECT simple_pay(20, 31, 64)", "SELECT simple_pay(12, 34, 79)", "SELECT simple_pay(0, 21, 41)", "SELECT simple_pay(2, 33, 10)", "SELECT simple_pay(38, 9, 25)", "SELECT simple_pay(45, 30, 5)"]}'); }
step "s1a20" { SELECT bcdb_check_block_status(9); }
step "s1a21" { SELECT bcdb_block_submit('{"txs": ["SELECT simple_pay(33, 2, 17)", "SELECT simple_pay(2, 19, 1)", "SELECT simple_pay(21, 10, 39)", "SELECT simple_pay(29, 23, 2)", "SELECT simple_pay(32, 2, 74)", "SELECT joint_pay(33, 48, 38, 20, 48)", "SELECT simple_pay(48, 13, 5)", "SELECT simple_pay(38, 26, 62)", "SELECT simple_pay(24, 38, 19)", "SELECT simple_pay(1, 42, 1)"]}'); }
step "s1a22" { SELECT bcdb_check_block_status(10); }
step "s1a23" { SELECT bcdb_block_submit('{"txs": ["SELECT simple_pay(19, 32, 146)", "SELECT simple_pay(4, 31, 34)", "SELECT simple_pay(19, 49, 27)", "SELECT simple_pay(24, 3, 2)", "SELECT simple_pay(8, 15, 19)", "SELECT simple_pay(21, 3, 5)", "SELECT simple_pay(9, 31, 84)", "SELECT simple_pay(9, 22, 211)", "SELECT joint_pay(24, 3, 6, 2, 78)", "SELECT joint_pay(38, 39, 8, 41, 83)"]}'); }
step "s1a24" { SELECT bcdb_check_block_status(11); }
step "s1a25" { SELECT bcdb_block_submit('{"txs": ["SELECT joint_pay(35, 41, 22, 100, 1)", "SELECT simple_pay(49, 31, 29)", "SELECT simple_pay(39, 44, 60)", "SELECT simple_pay(21, 41, 16)", "SELECT simple_pay(45, 39, 19)", "SELECT simple_pay(8, 24, 76)", "SELECT simple_pay(43, 7, 5)", "SELECT simple_pay(12, 2, 26)", "SELECT simple_pay(48, 12, 4)", "SELECT simple_pay(40, 4, 3)"]}'); }
step "s1a26" { SELECT bcdb_check_block_status(12); }
step "s1a27" { SELECT bcdb_block_submit('{"txs": ["SELECT simple_pay(2, 31, 66)", "SELECT simple_pay(33, 42, 73)", "SELECT simple_pay(13, 14, 24)", "SELECT simple_pay(40, 49, 33)", "SELECT simple_pay(26, 32, 79)", "SELECT simple_pay(9, 27, 229)", "SELECT simple_pay(5, 6, 14)", "SELECT joint_pay(26, 49, 9, 94, 8)", "SELECT simple_pay(27, 43, 107)", "SELECT joint_pay(20, 46, 16, 3, 3)"]}'); }
step "s1a28" { SELECT bcdb_check_block_status(13); }
step "s1a29" { SELECT bcdb_block_submit('{"txs": ["SELECT joint_pay(22, 44, 1, 177, 45)", "SELECT joint_pay(14, 23, 4, 37, 27)", "SELECT joint_pay(42, 43, 46, 16, 96)", "SELECT joint_pay(23, 44, 1, 39, 8)", "SELECT simple_pay(11, 29, 4)", "SELECT simple_pay(45, 16, 5)", "SELECT joint_pay(13, 21, 30, 75, 38)", "SELECT simple_pay(35, 40, 168)", "SELECT joint_pay(5, 6, 34, 10, 79)", "SELECT joint_pay(9, 8, 14, 41, 66)"]}'); }
step "s1a30" { SELECT bcdb_check_block_status(14); }
step "s1a31" { SELECT bcdb_block_submit('{"txs": ["SELECT simple_pay(48, 11, 2)", "SELECT simple_pay(42, 2, 17)", "SELECT simple_pay(25, 4, 5)", "SELECT joint_pay(19, 35, 26, 5, 152)", "SELECT simple_pay(40, 22, 22)", "SELECT simple_pay(40, 23, 136)", "SELECT joint_pay(26, 0, 46, 83, 29)", "SELECT simple_pay(18, 30, 3)", "SELECT simple_pay(6, 17, 8)", "SELECT simple_pay(44, 9, 15)"]}'); }
step "s1a32" { SELECT bcdb_check_block_status(15); }
step "s1a33" { SELECT bcdb_block_submit('{"txs": ["SELECT simple_pay(11, 49, 7)", "SELECT simple_pay(15, 29, 22)", "SELECT simple_pay(9, 22, 60)", "SELECT simple_pay(5, 30, 2)", "SELECT simple_pay(44, 28, 2)", "SELECT joint_pay(19, 7, 49, 11, 78)", "SELECT simple_pay(9, 27, 31)", "SELECT joint_pay(31, 48, 14, 279, 1)", "SELECT simple_pay(1, 7, 139)", "SELECT simple_pay(2, 0, 33)"]}'); }
step "s1a34" { SELECT bcdb_check_block_status(16); }
step "s1a35" { SELECT bcdb_block_submit('{"txs": ["SELECT simple_pay(37, 45, 203)", "SELECT simple_pay(47, 16, 91)", "SELECT simple_pay(43, 12, 10)", "SELECT joint_pay(4, 16, 19, 88, 31)", "SELECT simple_pay(15, 48, 6)", "SELECT joint_pay(18, 33, 8, 19, 34)", "SELECT simple_pay(34, 6, 106)", "SELECT simple_pay(34, 25, 48)", "SELECT simple_pay(17, 18, 57)", "SELECT simple_pay(40, 8, 6)"]}'); }
step "s1a36" { SELECT bcdb_check_block_status(17); }
step "s1a37" { SELECT bcdb_block_submit('{"txs": ["SELECT joint_pay(7, 24, 25, 152, 60)", "SELECT joint_pay(42, 19, 22, 61, 96)", "SELECT simple_pay(30, 31, 129)", "SELECT simple_pay(41, 3, 15)", "SELECT simple_pay(47, 31, 7)", "SELECT simple_pay(13, 1, 46)", "SELECT simple_pay(0, 33, 5)", "SELECT simple_pay(5, 43, 3)", "SELECT simple_pay(25, 0, 185)", "SELECT joint_pay(39, 0, 17, 38, 187)"]}'); }
step "s1a38" { SELECT bcdb_check_block_status(18); }
step "s1a39" { SELECT bcdb_block_submit('{"txs": ["SELECT simple_pay(9, 48, 3)", "SELECT joint_pay(27, 29, 45, 85, 13)", "SELECT joint_pay(26, 41, 43, 56, 1)", "SELECT simple_pay(45, 9, 269)", "SELECT simple_pay(13, 11, 29)", "SELECT simple_pay(24, 27, 16)", "SELECT simple_pay(14, 12, 225)", "SELECT simple_pay(37, 45, 13)", "SELECT simple_pay(2, 14, 41)", "SELECT joint_pay(11, 23, 3, 12, 60)"]}'); }
step "s1a40" { SELECT bcdb_check_block_status(19); }
step "s1a41" { SELECT bcdb_block_submit('{"txs": ["SELECT simple_pay(39, 5, 23)", "SELECT simple_pay(48, 18, 6)", "SELECT simple_pay(3, 40, 265)", "SELECT simple_pay(35, 47, 28)", "SELECT simple_pay(31, 16, 181)", "SELECT simple_pay(21, 17, 3)", "SELECT joint_pay(10, 22, 0, 38, 336)", "SELECT joint_pay(4, 27, 43, 15, 78)", "SELECT simple_pay(14, 29, 99)", "SELECT simple_pay(6, 38, 22)"]}'); }
step "s1a42" { SELECT bcdb_check_block_status(20); }
step "s1a43" { SELECT bcdb_block_submit('{"txs": ["SELECT simple_pay(20, 34, 15)", "SELECT simple_pay(16, 1, 268)", "SELECT joint_pay(23, 5, 13, 68, 12)", "SELECT joint_pay(12, 16, 43, 187, 39)", "SELECT simple_pay(24, 16, 1)", "SELECT simple_pay(45, 15, 3)", "SELECT simple_pay(35, 4, 1)", "SELECT simple_pay(46, 28, 13)", "SELECT simple_pay(26, 31, 30)", "SELECT simple_pay(5, 15, 2)"]}'); }
step "s1a44" { SELECT bcdb_check_block_status(21); }
step "s1a45" { SELECT bcdb_block_submit('{"txs": ["SELECT simple_pay(9, 26, 110)", "SELECT simple_pay(4, 27, 26)", "SELECT joint_pay(11, 15, 31, 8, 3)", "SELECT simple_pay(17, 22, 82)", "SELECT simple_pay(6, 35, 74)", "SELECT simple_pay(12, 45, 19)", "SELECT simple_pay(32, 38, 119)", "SELECT simple_pay(16, 17, 15)", "SELECT joint_pay(39, 45, 6, 2, 54)", "SELECT simple_pay(18, 47, 1)"]}'); }
step "s1a46" { SELECT bcdb_check_block_status(22); }
step "s1a47" { SELECT bcdb_block_submit('{"txs": ["SELECT simple_pay(32, 27, 110)", "SELECT joint_pay(17, 7, 47, 145, 46)", "SELECT simple_pay(45, 34, 10)", "SELECT simple_pay(15, 4, 9)", "SELECT simple_pay(20, 14, 3)", "SELECT simple_pay(18, 37, 22)", "SELECT joint_pay(0, 35, 32, 168, 47)", "SELECT simple_pay(1, 8, 406)", "SELECT joint_pay(11, 32, 4, 5, 196)", "SELECT simple_pay(49, 31, 292)"]}'); }
step "s1a48" { SELECT bcdb_check_block_status(23); }
step "s1a49" { SELECT bcdb_block_submit('{"txs": ["SELECT simple_pay(13, 15, 94)", "SELECT joint_pay(14, 48, 24, 91, 3)", "SELECT simple_pay(40, 31, 56)", "SELECT simple_pay(1, 33, 92)", "SELECT simple_pay(19, 0, 8)", "SELECT simple_pay(10, 42, 32)", "SELECT simple_pay(47, 30, 280)", "SELECT simple_pay(5, 16, 3)", "SELECT simple_pay(45, 12, 6)", "SELECT simple_pay(24, 3, 27)"]}'); }
step "s1a50" { SELECT bcdb_check_block_status(24); }
step "s1a51" { SELECT bcdb_block_submit('{"txs": ["SELECT joint_pay(46, 47, 15, 88, 4)", "SELECT simple_pay(42, 14, 17)", "SELECT simple_pay(10, 19, 1)", "SELECT simple_pay(34, 3, 10)", "SELECT simple_pay(31, 40, 32)", "SELECT joint_pay(2, 0, 14, 21, 84)", "SELECT joint_pay(3, 22, 42, 55, 35)", "SELECT simple_pay(13, 28, 14)", "SELECT joint_pay(19, 11, 41, 11, 7)", "SELECT simple_pay(26, 16, 69)"]}'); }
step "s1a52" { SELECT bcdb_check_block_status(25); }
step "s1a53" { SELECT bcdb_block_submit('{"txs": ["SELECT simple_pay(43, 45, 237)", "SELECT simple_pay(36, 7, 53)", "SELECT simple_pay(10, 0, 3)", "SELECT simple_pay(42, 32, 108)", "SELECT simple_pay(9, 5, 85)", "SELECT simple_pay(11, 15, 1)", "SELECT simple_pay(10, 47, 5)", "SELECT joint_pay(5, 27, 38, 14, 159)", "SELECT simple_pay(45, 9, 158)", "SELECT simple_pay(16, 21, 49)"]}'); }
step "s1a54" { SELECT bcdb_check_block_status(26); }
step "s1a55" { SELECT bcdb_block_submit('{"txs": ["SELECT joint_pay(2, 31, 5, 1, 150)", "SELECT simple_pay(29, 15, 65)", "SELECT simple_pay(47, 48, 4)", "SELECT simple_pay(31, 25, 8)", "SELECT simple_pay(18, 35, 31)", "SELECT simple_pay(49, 34, 10)", "SELECT simple_pay(43, 2, 117)", "SELECT simple_pay(7, 25, 45)", "SELECT simple_pay(1, 17, 48)", "SELECT simple_pay(16, 43, 38)"]}'); }
step "s1a56" { SELECT bcdb_check_block_status(27); }
step "s1a57" { SELECT bcdb_block_submit('{"txs": ["SELECT simple_pay(18, 43, 13)", "SELECT simple_pay(33, 21, 50)", "SELECT simple_pay(16, 13, 1)", "SELECT simple_pay(21, 15, 137)", "SELECT simple_pay(22, 10, 40)", "SELECT simple_pay(47, 0, 1)", "SELECT simple_pay(22, 23, 75)", "SELECT simple_pay(20, 31, 2)", "SELECT simple_pay(10, 0, 10)", "SELECT simple_pay(28, 8, 11)"]}'); }
step "s1a58" { SELECT bcdb_check_block_status(28); }
step "s1a59" { SELECT bcdb_block_submit('{"txs": ["SELECT simple_pay(46, 30, 117)", "SELECT simple_pay(42, 49, 5)", "SELECT simple_pay(12, 4, 36)", "SELECT simple_pay(17, 11, 68)", "SELECT joint_pay(42, 40, 10, 10, 57)", "SELECT simple_pay(40, 34, 155)", "SELECT simple_pay(27, 17, 3)", "SELECT simple_pay(27, 49, 2)", "SELECT simple_pay(34, 33, 142)", "SELECT simple_pay(21, 12, 1)"]}'); }
step "s1a60" { SELECT bcdb_check_block_status(29); }
step "s1a61" { SELECT bcdb_block_submit('{"txs": ["SELECT simple_pay(0, 48, 131)", "SELECT joint_pay(36, 24, 23, 30, 5)", "SELECT simple_pay(26, 40, 40)", "SELECT simple_pay(48, 14, 5)", "SELECT simple_pay(10, 43, 25)", "SELECT simple_pay(40, 44, 64)", "SELECT joint_pay(15, 36, 17, 95, 14)", "SELECT joint_pay(28, 15, 47, 15, 261)", "SELECT simple_pay(45, 6, 25)", "SELECT joint_pay(4, 40, 25, 241, 9)"]}'); }
step "s1a62" { SELECT bcdb_check_block_status(30); }
step "s1a63" { SELECT bcdb_block_submit('{"txs": ["SELECT simple_pay(48, 49, 92)", "SELECT simple_pay(5, 19, 8)", "SELECT simple_pay(48, 16, 13)", "SELECT simple_pay(24, 27, 50)", "SELECT simple_pay(43, 24, 90)", "SELECT simple_pay(2, 37, 60)", "SELECT simple_pay(36, 8, 3)", "SELECT simple_pay(1, 25, 2)", "SELECT simple_pay(8, 2, 42)", "SELECT simple_pay(22, 23, 1)"]}'); }
step "s1a64" { SELECT bcdb_check_block_status(31); }
step "s1a65" { SELECT bcdb_block_submit('{"txs": ["SELECT joint_pay(45, 7, 42, 35, 31)", "SELECT joint_pay(1, 20, 25, 1, 1)", "SELECT simple_pay(9, 38, 38)", "SELECT simple_pay(19, 32, 2)", "SELECT joint_pay(8, 30, 45, 329, 367)", "SELECT simple_pay(2, 46, 67)", "SELECT joint_pay(35, 44, 47, 50, 24)", "SELECT simple_pay(37, 5, 42)", "SELECT simple_pay(16, 12, 9)", "SELECT simple_pay(45, 16, 266)"]}'); }
step "s1a66" { SELECT bcdb_check_block_status(32); }
step "s1a67" { SELECT bcdb_block_submit('{"txs": ["SELECT simple_pay(29, 9, 29)", "SELECT simple_pay(2, 40, 12)", "SELECT simple_pay(2, 48, 11)", "SELECT simple_pay(4, 12, 11)", "SELECT simple_pay(39, 15, 2)", "SELECT simple_pay(45, 21, 336)", "SELECT joint_pay(49, 35, 3, 70, 3)", "SELECT simple_pay(21, 0, 41)", "SELECT joint_pay(38, 22, 36, 232, 43)", "SELECT simple_pay(32, 23, 31)"]}'); }
step "s1a68" { SELECT bcdb_check_block_status(33); }
step "s1a69" { SELECT bcdb_block_submit('{"txs": ["SELECT joint_pay(11, 46, 8, 3, 44)", "SELECT simple_pay(12, 2, 27)", "SELECT simple_pay(44, 19, 25)", "SELECT simple_pay(38, 49, 102)", "SELECT simple_pay(22, 4, 14)", "SELECT joint_pay(22, 38, 39, 5, 10)", "SELECT simple_pay(29, 26, 6)", "SELECT joint_pay(16, 12, 24, 33, 3)", "SELECT joint_pay(22, 11, 25, 5, 2)", "SELECT simple_pay(35, 47, 14)"]}'); }
step "s1a70" { SELECT bcdb_check_block_status(34); }
step "s1a71" { SELECT bcdb_block_submit('{"txs": ["SELECT simple_pay(30, 5, 4)", "SELECT simple_pay(25, 16, 15)", "SELECT simple_pay(6, 5, 86)", "SELECT simple_pay(6, 30, 3)", "SELECT joint_pay(33, 40, 18, 10, 1)", "SELECT simple_pay(10, 35, 19)", "SELECT joint_pay(49, 10, 40, 63, 40)", "SELECT simple_pay(30, 40, 26)", "SELECT joint_pay(15, 40, 18, 22, 44)", "SELECT simple_pay(14, 10, 225)"]}'); }
step "s1a72" { SELECT bcdb_check_block_status(35); }
step "s1a73" { SELECT bcdb_block_submit('{"txs": ["SELECT simple_pay(23, 36, 36)", "SELECT simple_pay(49, 0, 21)", "SELECT simple_pay(0, 43, 50)", "SELECT simple_pay(11, 9, 3)", "SELECT joint_pay(32, 0, 2, 7, 50)", "SELECT simple_pay(36, 39, 76)", "SELECT simple_pay(43, 24, 51)", "SELECT joint_pay(27, 36, 43, 22, 183)", "SELECT simple_pay(8, 23, 131)", "SELECT simple_pay(25, 4, 67)"]}'); }
step "s1a74" { SELECT bcdb_check_block_status(36); }
step "s1a75" { SELECT bcdb_block_submit('{"txs": ["SELECT simple_pay(42, 22, 13)", "SELECT simple_pay(27, 15, 16)", "SELECT simple_pay(25, 15, 331)", "SELECT simple_pay(37, 4, 214)", "SELECT simple_pay(17, 33, 96)", "SELECT simple_pay(38, 39, 8)", "SELECT simple_pay(17, 2, 21)", "SELECT simple_pay(25, 40, 2)", "SELECT simple_pay(3, 9, 92)", "SELECT simple_pay(49, 26, 47)"]}'); }
step "s1a76" { SELECT bcdb_check_block_status(37); }
step "s1a77" { SELECT bcdb_block_submit('{"txs": ["SELECT simple_pay(25, 27, 2)", "SELECT simple_pay(38, 29, 1)", "SELECT joint_pay(30, 26, 10, 5, 37)", "SELECT simple_pay(7, 23, 6)", "SELECT joint_pay(22, 49, 30, 11, 3)", "SELECT simple_pay(12, 16, 1)", "SELECT simple_pay(18, 24, 6)", "SELECT simple_pay(27, 2, 11)", "SELECT simple_pay(24, 46, 54)", "SELECT simple_pay(8, 7, 23)"]}'); }
step "s1a78" { SELECT bcdb_check_block_status(38); }
step "s1a79" { SELECT bcdb_wait_to_finish(); }
step "s1a80" { SELECT bcdb_check_block_status(38); }
step "s1a81" { SELECT bcdb_check_block_status(39); }
step "s1a82" { SELECT bcdb_check_block_status(40); }
step "s1a84" { SELECT * FROM bank ORDER BY account; SELECT sum(balance) FROM bank; }

permutation "s1a0" "s1a1" "s1a2" "s1a3" "s1a4" "s1a5" "s1a6" "s1a7" "s1a8" "s1a9" "s1a10" "s1a11" "s1a12" "s1a13" "s1a14" "s1a15" "s1a16" "s1a17" "s1a18" "s1a19" "s1a20" "s1a21" "s1a22" "s1a23" "s1a24" "s1a25" "s1a26" "s1a27" "s1a28" "s1a29" "s1a30" "s1a31" "s1a32" "s1a33" "s1a34" "s1a35" "s1a36" "s1a37" "s1a38" "s1a39" "s1a40" "s1a41" "s1a42" "s1a43" "s1a44" "s1a45" "s1a46" "s1a47" "s1a48" "s1a49" "s1a50" "s1a51" "s1a52" "s1a53" "s1a54" "s1a55" "s1a56" "s1a57" "s1a58" "s1a59" "s1a60" "s1a61" "s1a62" "s1a63" "s1a64" "s1a65" "s1a66" "s1a67" "s1a68" "s1a69" "s1a70" "s1a71" "s1a72" "s1a73" "s1a74" "s1a75" "s1a76" "s1a77" "s1a78" "s1a79" "s1a80" "s1a81" "s1a82" "s1a84"
