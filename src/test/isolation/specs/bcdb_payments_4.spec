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

SELECT bcdb_reset();
}

session "s1"
step "s1a0" { SELECT bcdb_init(False, 16); }
step "s1a1" { SELECT bcdb_tx_submit('{"hash": "1_0", "iso": "SE", "sql": "SELECT simple_pay(48, 26, 0);"}'); }
step "s1a2" { SELECT bcdb_tx_submit('{"hash": "1_1", "iso": "SE", "sql": "SELECT joint_pay(32, 31, 25, 0, 0);"}'); }
step "s1a3" { SELECT bcdb_tx_submit('{"hash": "1_2", "iso": "SE", "sql": "SELECT simple_pay(19, 30, 0);"}'); }
step "s1a4" { SELECT bcdb_tx_submit('{"hash": "1_3", "iso": "SE", "sql": "SELECT simple_pay(13, 32, 0);"}'); }
step "s1a5" { SELECT bcdb_tx_submit('{"hash": "1_4", "iso": "SE", "sql": "SELECT joint_pay(8, 48, 6, 0, 0);"}'); }
step "s1a6" { SELECT bcdb_tx_submit('{"hash": "1_5", "iso": "SE", "sql": "SELECT simple_pay(16, 34, 0);"}'); }
step "s1a7" { SELECT bcdb_tx_submit('{"hash": "1_6", "iso": "SE", "sql": "SELECT simple_pay(38, 9, 0);"}'); }
step "s1a8" { SELECT bcdb_tx_submit('{"hash": "1_7", "iso": "SE", "sql": "SELECT simple_pay(46, 4, 0);"}'); }
step "s1a9" { SELECT bcdb_tx_submit('{"hash": "1_8", "iso": "SE", "sql": "SELECT simple_pay(43, 21, 0);"}'); }
step "s1a10" { SELECT bcdb_tx_submit('{"hash": "1_9", "iso": "SE", "sql": "SELECT simple_pay(6, 22, 0);"}'); }
step "s1a11" { SELECT bcdb_tx_submit('{"hash": "1_10", "iso": "SE", "sql": "SELECT simple_pay(39, 40, 0);"}'); }
step "s1a12" { SELECT bcdb_tx_submit('{"hash": "1_11", "iso": "SE", "sql": "SELECT simple_pay(35, 30, 0);"}'); }
step "s1a13" { SELECT bcdb_tx_submit('{"hash": "1_12", "iso": "SE", "sql": "SELECT simple_pay(33, 16, 0);"}'); }
step "s1a14" { SELECT bcdb_tx_submit('{"hash": "1_13", "iso": "SE", "sql": "SELECT joint_pay(35, 0, 5, 0, 0);"}'); }
step "s1a15" { SELECT bcdb_tx_submit('{"hash": "1_14", "iso": "SE", "sql": "SELECT simple_pay(25, 45, 0);"}'); }
step "s1a16" { SELECT bcdb_tx_submit('{"hash": "1_15", "iso": "SE", "sql": "SELECT simple_pay(42, 40, 0);"}'); }
step "s1a17" { SELECT bcdb_block_submit('{"bid": 1, "txs": ["1_0", "1_1", "1_2", "1_3", "1_4", "1_5", "1_6", "1_7", "1_8", "1_9", "1_10", "1_11", "1_12", "1_13", "1_14", "1_15"]}'); }
step "s1a18" { SELECT bcdb_tx_submit('{"hash": "2_0", "iso": "SE", "sql": "SELECT joint_pay(31, 21, 15, 0, 0);"}'); }
step "s1a19" { SELECT bcdb_tx_submit('{"hash": "2_1", "iso": "SE", "sql": "SELECT simple_pay(45, 4, 0);"}'); }
step "s1a20" { SELECT bcdb_tx_submit('{"hash": "2_2", "iso": "SE", "sql": "SELECT joint_pay(36, 14, 15, 0, 0);"}'); }
step "s1a21" { SELECT bcdb_tx_submit('{"hash": "2_3", "iso": "SE", "sql": "SELECT simple_pay(9, 34, 0);"}'); }
step "s1a22" { SELECT bcdb_tx_submit('{"hash": "2_4", "iso": "SE", "sql": "SELECT simple_pay(5, 20, 0);"}'); }
step "s1a23" { SELECT bcdb_tx_submit('{"hash": "2_5", "iso": "SE", "sql": "SELECT simple_pay(31, 6, 0);"}'); }
step "s1a24" { SELECT bcdb_tx_submit('{"hash": "2_6", "iso": "SE", "sql": "SELECT simple_pay(18, 45, 0);"}'); }
step "s1a25" { SELECT bcdb_tx_submit('{"hash": "2_7", "iso": "SE", "sql": "SELECT joint_pay(21, 34, 13, 0, 0);"}'); }
step "s1a26" { SELECT bcdb_tx_submit('{"hash": "2_8", "iso": "SE", "sql": "SELECT simple_pay(38, 35, 0);"}'); }
step "s1a27" { SELECT bcdb_tx_submit('{"hash": "2_9", "iso": "SE", "sql": "SELECT simple_pay(28, 5, 0);"}'); }
step "s1a28" { SELECT bcdb_tx_submit('{"hash": "2_10", "iso": "SE", "sql": "SELECT simple_pay(24, 20, 0);"}'); }
step "s1a29" { SELECT bcdb_tx_submit('{"hash": "2_11", "iso": "SE", "sql": "SELECT simple_pay(18, 11, 0);"}'); }
step "s1a30" { SELECT bcdb_tx_submit('{"hash": "2_12", "iso": "SE", "sql": "SELECT joint_pay(11, 2, 39, 0, 0);"}'); }
step "s1a31" { SELECT bcdb_tx_submit('{"hash": "2_13", "iso": "SE", "sql": "SELECT simple_pay(16, 30, 0);"}'); }
step "s1a32" { SELECT bcdb_tx_submit('{"hash": "2_14", "iso": "SE", "sql": "SELECT joint_pay(43, 48, 8, 0, 0);"}'); }
step "s1a33" { SELECT bcdb_tx_submit('{"hash": "2_15", "iso": "SE", "sql": "SELECT simple_pay(2, 5, 0);"}'); }
step "s1a34" { SELECT bcdb_block_submit('{"bid": 2, "txs": ["2_0", "2_1", "2_2", "2_3", "2_4", "2_5", "2_6", "2_7", "2_8", "2_9", "2_10", "2_11", "2_12", "2_13", "2_14", "2_15"]}'); }
step "s1a35" { SELECT bcdb_tx_submit('{"hash": "3_0", "iso": "SE", "sql": "SELECT simple_pay(34, 43, 0);"}'); }
step "s1a36" { SELECT bcdb_tx_submit('{"hash": "3_1", "iso": "SE", "sql": "SELECT simple_pay(45, 33, 0);"}'); }
step "s1a37" { SELECT bcdb_tx_submit('{"hash": "3_2", "iso": "SE", "sql": "SELECT simple_pay(15, 13, 0);"}'); }
step "s1a38" { SELECT bcdb_tx_submit('{"hash": "3_3", "iso": "SE", "sql": "SELECT simple_pay(37, 26, 0);"}'); }
step "s1a39" { SELECT bcdb_tx_submit('{"hash": "3_4", "iso": "SE", "sql": "SELECT simple_pay(28, 31, 0);"}'); }
step "s1a40" { SELECT bcdb_tx_submit('{"hash": "3_5", "iso": "SE", "sql": "SELECT simple_pay(44, 22, 0);"}'); }
step "s1a41" { SELECT bcdb_tx_submit('{"hash": "3_6", "iso": "SE", "sql": "SELECT joint_pay(39, 7, 31, 0, 0);"}'); }
step "s1a42" { SELECT bcdb_tx_submit('{"hash": "3_7", "iso": "SE", "sql": "SELECT simple_pay(21, 12, 0);"}'); }
step "s1a43" { SELECT bcdb_tx_submit('{"hash": "3_8", "iso": "SE", "sql": "SELECT simple_pay(46, 17, 0);"}'); }
step "s1a44" { SELECT bcdb_tx_submit('{"hash": "3_9", "iso": "SE", "sql": "SELECT joint_pay(14, 23, 10, 0, 0);"}'); }
step "s1a45" { SELECT bcdb_tx_submit('{"hash": "3_10", "iso": "SE", "sql": "SELECT simple_pay(3, 6, 0);"}'); }
step "s1a46" { SELECT bcdb_tx_submit('{"hash": "3_11", "iso": "SE", "sql": "SELECT simple_pay(44, 14, 0);"}'); }
step "s1a47" { SELECT bcdb_tx_submit('{"hash": "3_12", "iso": "SE", "sql": "SELECT joint_pay(36, 40, 34, 0, 0);"}'); }
step "s1a48" { SELECT bcdb_tx_submit('{"hash": "3_13", "iso": "SE", "sql": "SELECT simple_pay(4, 1, 0);"}'); }
step "s1a49" { SELECT bcdb_tx_submit('{"hash": "3_14", "iso": "SE", "sql": "SELECT joint_pay(12, 38, 36, 0, 0);"}'); }
step "s1a50" { SELECT bcdb_tx_submit('{"hash": "3_15", "iso": "SE", "sql": "SELECT joint_pay(5, 23, 7, 0, 0);"}'); }
step "s1a51" { SELECT bcdb_block_submit('{"bid": 3, "txs": ["3_0", "3_1", "3_2", "3_3", "3_4", "3_5", "3_6", "3_7", "3_8", "3_9", "3_10", "3_11", "3_12", "3_13", "3_14", "3_15"]}'); }
step "s1a52" { SELECT bcdb_tx_submit('{"hash": "4_0", "iso": "SE", "sql": "SELECT joint_pay(1, 12, 11, 0, 0);"}'); }
step "s1a53" { SELECT bcdb_tx_submit('{"hash": "4_1", "iso": "SE", "sql": "SELECT simple_pay(30, 13, 0);"}'); }
step "s1a54" { SELECT bcdb_tx_submit('{"hash": "4_2", "iso": "SE", "sql": "SELECT simple_pay(3, 43, 0);"}'); }
step "s1a55" { SELECT bcdb_tx_submit('{"hash": "4_3", "iso": "SE", "sql": "SELECT joint_pay(27, 39, 6, 0, 0);"}'); }
step "s1a56" { SELECT bcdb_tx_submit('{"hash": "4_4", "iso": "SE", "sql": "SELECT simple_pay(4, 14, 0);"}'); }
step "s1a57" { SELECT bcdb_tx_submit('{"hash": "4_5", "iso": "SE", "sql": "SELECT joint_pay(19, 22, 27, 0, 0);"}'); }
step "s1a58" { SELECT bcdb_tx_submit('{"hash": "4_6", "iso": "SE", "sql": "SELECT joint_pay(32, 29, 2, 0, 0);"}'); }
step "s1a59" { SELECT bcdb_tx_submit('{"hash": "4_7", "iso": "SE", "sql": "SELECT simple_pay(44, 25, 0);"}'); }
step "s1a60" { SELECT bcdb_tx_submit('{"hash": "4_8", "iso": "SE", "sql": "SELECT joint_pay(22, 46, 30, 0, 0);"}'); }
step "s1a61" { SELECT bcdb_tx_submit('{"hash": "4_9", "iso": "SE", "sql": "SELECT simple_pay(36, 10, 0);"}'); }
step "s1a62" { SELECT bcdb_tx_submit('{"hash": "4_10", "iso": "SE", "sql": "SELECT simple_pay(13, 49, 0);"}'); }
step "s1a63" { SELECT bcdb_tx_submit('{"hash": "4_11", "iso": "SE", "sql": "SELECT joint_pay(43, 10, 21, 0, 0);"}'); }
step "s1a64" { SELECT bcdb_tx_submit('{"hash": "4_12", "iso": "SE", "sql": "SELECT simple_pay(7, 38, 0);"}'); }
step "s1a65" { SELECT bcdb_tx_submit('{"hash": "4_13", "iso": "SE", "sql": "SELECT simple_pay(42, 11, 0);"}'); }
step "s1a66" { SELECT bcdb_tx_submit('{"hash": "4_14", "iso": "SE", "sql": "SELECT joint_pay(43, 26, 36, 0, 0);"}'); }
step "s1a67" { SELECT bcdb_tx_submit('{"hash": "4_15", "iso": "SE", "sql": "SELECT simple_pay(19, 41, 0);"}'); }
step "s1a68" { SELECT bcdb_block_submit('{"bid": 4, "txs": ["4_0", "4_1", "4_2", "4_3", "4_4", "4_5", "4_6", "4_7", "4_8", "4_9", "4_10", "4_11", "4_12", "4_13", "4_14", "4_15"]}'); }
step "s1a69" { SELECT bcdb_tx_submit('{"hash": "5_0", "iso": "SE", "sql": "SELECT simple_pay(42, 16, 0);"}'); }
step "s1a70" { SELECT bcdb_tx_submit('{"hash": "5_1", "iso": "SE", "sql": "SELECT joint_pay(44, 0, 29, 0, 0);"}'); }
step "s1a71" { SELECT bcdb_tx_submit('{"hash": "5_2", "iso": "SE", "sql": "SELECT simple_pay(21, 47, 0);"}'); }
step "s1a72" { SELECT bcdb_tx_submit('{"hash": "5_3", "iso": "SE", "sql": "SELECT joint_pay(17, 8, 15, 0, 0);"}'); }
step "s1a73" { SELECT bcdb_tx_submit('{"hash": "5_4", "iso": "SE", "sql": "SELECT simple_pay(30, 22, 0);"}'); }
step "s1a74" { SELECT bcdb_tx_submit('{"hash": "5_5", "iso": "SE", "sql": "SELECT simple_pay(43, 22, 0);"}'); }
step "s1a75" { SELECT bcdb_tx_submit('{"hash": "5_6", "iso": "SE", "sql": "SELECT simple_pay(40, 39, 0);"}'); }
step "s1a76" { SELECT bcdb_tx_submit('{"hash": "5_7", "iso": "SE", "sql": "SELECT joint_pay(19, 24, 47, 0, 0);"}'); }
step "s1a77" { SELECT bcdb_tx_submit('{"hash": "5_8", "iso": "SE", "sql": "SELECT simple_pay(41, 5, 0);"}'); }
step "s1a78" { SELECT bcdb_tx_submit('{"hash": "5_9", "iso": "SE", "sql": "SELECT joint_pay(12, 44, 21, 0, 0);"}'); }
step "s1a79" { SELECT bcdb_tx_submit('{"hash": "5_10", "iso": "SE", "sql": "SELECT joint_pay(14, 40, 28, 0, 0);"}'); }
step "s1a80" { SELECT bcdb_tx_submit('{"hash": "5_11", "iso": "SE", "sql": "SELECT simple_pay(43, 36, 0);"}'); }
step "s1a81" { SELECT bcdb_tx_submit('{"hash": "5_12", "iso": "SE", "sql": "SELECT simple_pay(2, 25, 0);"}'); }
step "s1a82" { SELECT bcdb_tx_submit('{"hash": "5_13", "iso": "SE", "sql": "SELECT simple_pay(36, 26, 0);"}'); }
step "s1a83" { SELECT bcdb_tx_submit('{"hash": "5_14", "iso": "SE", "sql": "SELECT simple_pay(45, 2, 0);"}'); }
step "s1a84" { SELECT bcdb_tx_submit('{"hash": "5_15", "iso": "SE", "sql": "SELECT joint_pay(4, 16, 44, 0, 0);"}'); }
step "s1a85" { SELECT bcdb_block_submit('{"bid": 5, "txs": ["5_0", "5_1", "5_2", "5_3", "5_4", "5_5", "5_6", "5_7", "5_8", "5_9", "5_10", "5_11", "5_12", "5_13", "5_14", "5_15"]}'); }
step "s1a86" { SELECT bcdb_tx_submit('{"hash": "6_0", "iso": "SE", "sql": "SELECT joint_pay(33, 31, 35, 0, 0);"}'); }
step "s1a87" { SELECT bcdb_tx_submit('{"hash": "6_1", "iso": "SE", "sql": "SELECT simple_pay(0, 2, 0);"}'); }
step "s1a88" { SELECT bcdb_tx_submit('{"hash": "6_2", "iso": "SE", "sql": "SELECT simple_pay(19, 29, 0);"}'); }
step "s1a89" { SELECT bcdb_tx_submit('{"hash": "6_3", "iso": "SE", "sql": "SELECT joint_pay(26, 12, 35, 0, 0);"}'); }
step "s1a90" { SELECT bcdb_tx_submit('{"hash": "6_4", "iso": "SE", "sql": "SELECT simple_pay(40, 5, 0);"}'); }
step "s1a91" { SELECT bcdb_tx_submit('{"hash": "6_5", "iso": "SE", "sql": "SELECT simple_pay(8, 0, 0);"}'); }
step "s1a92" { SELECT bcdb_tx_submit('{"hash": "6_6", "iso": "SE", "sql": "SELECT simple_pay(43, 26, 0);"}'); }
step "s1a93" { SELECT bcdb_tx_submit('{"hash": "6_7", "iso": "SE", "sql": "SELECT simple_pay(13, 0, 0);"}'); }
step "s1a94" { SELECT bcdb_tx_submit('{"hash": "6_8", "iso": "SE", "sql": "SELECT simple_pay(0, 43, 0);"}'); }
step "s1a95" { SELECT bcdb_tx_submit('{"hash": "6_9", "iso": "SE", "sql": "SELECT simple_pay(6, 12, 0);"}'); }
step "s1a96" { SELECT bcdb_tx_submit('{"hash": "6_10", "iso": "SE", "sql": "SELECT joint_pay(41, 12, 19, 0, 0);"}'); }
step "s1a97" { SELECT bcdb_tx_submit('{"hash": "6_11", "iso": "SE", "sql": "SELECT simple_pay(11, 6, 0);"}'); }
step "s1a98" { SELECT bcdb_tx_submit('{"hash": "6_12", "iso": "SE", "sql": "SELECT simple_pay(25, 40, 0);"}'); }
step "s1a99" { SELECT bcdb_tx_submit('{"hash": "6_13", "iso": "SE", "sql": "SELECT joint_pay(17, 28, 7, 0, 0);"}'); }
step "s1a100" { SELECT bcdb_tx_submit('{"hash": "6_14", "iso": "SE", "sql": "SELECT simple_pay(8, 41, 0);"}'); }
step "s1a101" { SELECT bcdb_tx_submit('{"hash": "6_15", "iso": "SE", "sql": "SELECT simple_pay(41, 22, 0);"}'); }
step "s1a102" { SELECT bcdb_block_submit('{"bid": 6, "txs": ["6_0", "6_1", "6_2", "6_3", "6_4", "6_5", "6_6", "6_7", "6_8", "6_9", "6_10", "6_11", "6_12", "6_13", "6_14", "6_15"]}'); }
step "s1a103" { SELECT bcdb_tx_submit('{"hash": "7_0", "iso": "SE", "sql": "SELECT joint_pay(9, 17, 1, 0, 0);"}'); }
step "s1a104" { SELECT bcdb_tx_submit('{"hash": "7_1", "iso": "SE", "sql": "SELECT joint_pay(13, 43, 16, 0, 0);"}'); }
step "s1a105" { SELECT bcdb_tx_submit('{"hash": "7_2", "iso": "SE", "sql": "SELECT simple_pay(23, 36, 0);"}'); }
step "s1a106" { SELECT bcdb_tx_submit('{"hash": "7_3", "iso": "SE", "sql": "SELECT simple_pay(2, 47, 0);"}'); }
step "s1a107" { SELECT bcdb_tx_submit('{"hash": "7_4", "iso": "SE", "sql": "SELECT simple_pay(38, 41, 0);"}'); }
step "s1a108" { SELECT bcdb_tx_submit('{"hash": "7_5", "iso": "SE", "sql": "SELECT simple_pay(41, 29, 0);"}'); }
step "s1a109" { SELECT bcdb_tx_submit('{"hash": "7_6", "iso": "SE", "sql": "SELECT simple_pay(23, 34, 0);"}'); }
step "s1a110" { SELECT bcdb_tx_submit('{"hash": "7_7", "iso": "SE", "sql": "SELECT joint_pay(24, 37, 18, 0, 0);"}'); }
step "s1a111" { SELECT bcdb_tx_submit('{"hash": "7_8", "iso": "SE", "sql": "SELECT joint_pay(9, 17, 21, 0, 0);"}'); }
step "s1a112" { SELECT bcdb_tx_submit('{"hash": "7_9", "iso": "SE", "sql": "SELECT simple_pay(23, 45, 0);"}'); }
step "s1a113" { SELECT bcdb_tx_submit('{"hash": "7_10", "iso": "SE", "sql": "SELECT joint_pay(49, 39, 2, 0, 0);"}'); }
step "s1a114" { SELECT bcdb_tx_submit('{"hash": "7_11", "iso": "SE", "sql": "SELECT joint_pay(10, 9, 37, 0, 0);"}'); }
step "s1a115" { SELECT bcdb_tx_submit('{"hash": "7_12", "iso": "SE", "sql": "SELECT simple_pay(25, 35, 0);"}'); }
step "s1a116" { SELECT bcdb_tx_submit('{"hash": "7_13", "iso": "SE", "sql": "SELECT joint_pay(7, 30, 46, 0, 0);"}'); }
step "s1a117" { SELECT bcdb_tx_submit('{"hash": "7_14", "iso": "SE", "sql": "SELECT simple_pay(3, 19, 0);"}'); }
step "s1a118" { SELECT bcdb_tx_submit('{"hash": "7_15", "iso": "SE", "sql": "SELECT joint_pay(33, 46, 4, 0, 0);"}'); }
step "s1a119" { SELECT bcdb_block_submit('{"bid": 7, "txs": ["7_0", "7_1", "7_2", "7_3", "7_4", "7_5", "7_6", "7_7", "7_8", "7_9", "7_10", "7_11", "7_12", "7_13", "7_14", "7_15"]}'); }
step "s1a120" { SELECT bcdb_tx_submit('{"hash": "8_0", "iso": "SE", "sql": "SELECT simple_pay(21, 19, 0);"}'); }
step "s1a121" { SELECT bcdb_tx_submit('{"hash": "8_1", "iso": "SE", "sql": "SELECT simple_pay(6, 35, 0);"}'); }
step "s1a122" { SELECT bcdb_tx_submit('{"hash": "8_2", "iso": "SE", "sql": "SELECT simple_pay(30, 21, 0);"}'); }
step "s1a123" { SELECT bcdb_tx_submit('{"hash": "8_3", "iso": "SE", "sql": "SELECT simple_pay(21, 7, 0);"}'); }
step "s1a124" { SELECT bcdb_tx_submit('{"hash": "8_4", "iso": "SE", "sql": "SELECT simple_pay(44, 31, 0);"}'); }
step "s1a125" { SELECT bcdb_tx_submit('{"hash": "8_5", "iso": "SE", "sql": "SELECT simple_pay(19, 21, 0);"}'); }
step "s1a126" { SELECT bcdb_tx_submit('{"hash": "8_6", "iso": "SE", "sql": "SELECT simple_pay(9, 10, 0);"}'); }
step "s1a127" { SELECT bcdb_tx_submit('{"hash": "8_7", "iso": "SE", "sql": "SELECT simple_pay(24, 40, 0);"}'); }
step "s1a128" { SELECT bcdb_tx_submit('{"hash": "8_8", "iso": "SE", "sql": "SELECT joint_pay(5, 12, 47, 0, 0);"}'); }
step "s1a129" { SELECT bcdb_tx_submit('{"hash": "8_9", "iso": "SE", "sql": "SELECT simple_pay(24, 0, 0);"}'); }
step "s1a130" { SELECT bcdb_tx_submit('{"hash": "8_10", "iso": "SE", "sql": "SELECT joint_pay(35, 33, 18, 0, 0);"}'); }
step "s1a131" { SELECT bcdb_tx_submit('{"hash": "8_11", "iso": "SE", "sql": "SELECT simple_pay(31, 37, 0);"}'); }
step "s1a132" { SELECT bcdb_tx_submit('{"hash": "8_12", "iso": "SE", "sql": "SELECT simple_pay(13, 27, 0);"}'); }
step "s1a133" { SELECT bcdb_tx_submit('{"hash": "8_13", "iso": "SE", "sql": "SELECT joint_pay(14, 16, 37, 0, 0);"}'); }
step "s1a134" { SELECT bcdb_tx_submit('{"hash": "8_14", "iso": "SE", "sql": "SELECT simple_pay(27, 12, 0);"}'); }
step "s1a135" { SELECT bcdb_tx_submit('{"hash": "8_15", "iso": "SE", "sql": "SELECT simple_pay(4, 44, 0);"}'); }
step "s1a136" { SELECT bcdb_block_submit('{"bid": 8, "txs": ["8_0", "8_1", "8_2", "8_3", "8_4", "8_5", "8_6", "8_7", "8_8", "8_9", "8_10", "8_11", "8_12", "8_13", "8_14", "8_15"]}'); }
step "s1a137" { SELECT bcdb_tx_submit('{"hash": "9_0", "iso": "SE", "sql": "SELECT joint_pay(33, 28, 48, 0, 0);"}'); }
step "s1a138" { SELECT bcdb_tx_submit('{"hash": "9_1", "iso": "SE", "sql": "SELECT simple_pay(7, 31, 0);"}'); }
step "s1a139" { SELECT bcdb_tx_submit('{"hash": "9_2", "iso": "SE", "sql": "SELECT simple_pay(13, 41, 0);"}'); }
step "s1a140" { SELECT bcdb_tx_submit('{"hash": "9_3", "iso": "SE", "sql": "SELECT joint_pay(13, 39, 9, 0, 0);"}'); }
step "s1a141" { SELECT bcdb_tx_submit('{"hash": "9_4", "iso": "SE", "sql": "SELECT joint_pay(29, 24, 23, 0, 0);"}'); }
step "s1a142" { SELECT bcdb_tx_submit('{"hash": "9_5", "iso": "SE", "sql": "SELECT simple_pay(9, 6, 0);"}'); }
step "s1a143" { SELECT bcdb_tx_submit('{"hash": "9_6", "iso": "SE", "sql": "SELECT simple_pay(31, 9, 0);"}'); }
step "s1a144" { SELECT bcdb_tx_submit('{"hash": "9_7", "iso": "SE", "sql": "SELECT simple_pay(40, 43, 0);"}'); }
step "s1a145" { SELECT bcdb_tx_submit('{"hash": "9_8", "iso": "SE", "sql": "SELECT simple_pay(33, 31, 0);"}'); }
step "s1a146" { SELECT bcdb_tx_submit('{"hash": "9_9", "iso": "SE", "sql": "SELECT simple_pay(20, 31, 0);"}'); }
step "s1a147" { SELECT bcdb_tx_submit('{"hash": "9_10", "iso": "SE", "sql": "SELECT simple_pay(40, 42, 0);"}'); }
step "s1a148" { SELECT bcdb_tx_submit('{"hash": "9_11", "iso": "SE", "sql": "SELECT simple_pay(34, 39, 0);"}'); }
step "s1a149" { SELECT bcdb_tx_submit('{"hash": "9_12", "iso": "SE", "sql": "SELECT simple_pay(0, 21, 0);"}'); }
step "s1a150" { SELECT bcdb_tx_submit('{"hash": "9_13", "iso": "SE", "sql": "SELECT simple_pay(47, 20, 0);"}'); }
step "s1a151" { SELECT bcdb_tx_submit('{"hash": "9_14", "iso": "SE", "sql": "SELECT simple_pay(2, 33, 0);"}'); }
step "s1a152" { SELECT bcdb_tx_submit('{"hash": "9_15", "iso": "SE", "sql": "SELECT joint_pay(16, 38, 9, 0, 0);"}'); }
step "s1a153" { SELECT bcdb_block_submit('{"bid": 9, "txs": ["9_0", "9_1", "9_2", "9_3", "9_4", "9_5", "9_6", "9_7", "9_8", "9_9", "9_10", "9_11", "9_12", "9_13", "9_14", "9_15"]}'); }
step "s1a154" { SELECT bcdb_tx_submit('{"hash": "10_0", "iso": "SE", "sql": "SELECT simple_pay(37, 18, 0);"}'); }
step "s1a155" { SELECT bcdb_tx_submit('{"hash": "10_1", "iso": "SE", "sql": "SELECT simple_pay(30, 4, 0);"}'); }
step "s1a156" { SELECT bcdb_tx_submit('{"hash": "10_2", "iso": "SE", "sql": "SELECT simple_pay(33, 2, 0);"}'); }
step "s1a157" { SELECT bcdb_tx_submit('{"hash": "10_3", "iso": "SE", "sql": "SELECT joint_pay(8, 2, 19, 0, 0);"}'); }
step "s1a158" { SELECT bcdb_tx_submit('{"hash": "10_4", "iso": "SE", "sql": "SELECT joint_pay(28, 21, 10, 0, 0);"}'); }
step "s1a159" { SELECT bcdb_tx_submit('{"hash": "10_5", "iso": "SE", "sql": "SELECT simple_pay(41, 29, 0);"}'); }
step "s1a160" { SELECT bcdb_tx_submit('{"hash": "10_6", "iso": "SE", "sql": "SELECT simple_pay(32, 24, 0);"}'); }
step "s1a161" { SELECT bcdb_tx_submit('{"hash": "10_7", "iso": "SE", "sql": "SELECT simple_pay(32, 2, 0);"}'); }
step "s1a162" { SELECT bcdb_tx_submit('{"hash": "10_8", "iso": "SE", "sql": "SELECT simple_pay(43, 33, 0);"}'); }
step "s1a163" { SELECT bcdb_tx_submit('{"hash": "10_9", "iso": "SE", "sql": "SELECT simple_pay(4, 47, 0);"}'); }
step "s1a164" { SELECT bcdb_tx_submit('{"hash": "10_10", "iso": "SE", "sql": "SELECT simple_pay(48, 13, 0);"}'); }
step "s1a165" { SELECT bcdb_tx_submit('{"hash": "10_11", "iso": "SE", "sql": "SELECT simple_pay(38, 26, 0);"}'); }
step "s1a166" { SELECT bcdb_tx_submit('{"hash": "10_12", "iso": "SE", "sql": "SELECT simple_pay(30, 24, 0);"}'); }
step "s1a167" { SELECT bcdb_tx_submit('{"hash": "10_13", "iso": "SE", "sql": "SELECT simple_pay(14, 1, 0);"}'); }
step "s1a168" { SELECT bcdb_tx_submit('{"hash": "10_14", "iso": "SE", "sql": "SELECT simple_pay(0, 47, 0);"}'); }
step "s1a169" { SELECT bcdb_tx_submit('{"hash": "10_15", "iso": "SE", "sql": "SELECT joint_pay(32, 36, 16, 0, 0);"}'); }
step "s1a170" { SELECT bcdb_block_submit('{"bid": 10, "txs": ["10_0", "10_1", "10_2", "10_3", "10_4", "10_5", "10_6", "10_7", "10_8", "10_9", "10_10", "10_11", "10_12", "10_13", "10_14", "10_15"]}'); }
step "s1a171" { SELECT bcdb_tx_submit('{"hash": "11_0", "iso": "SE", "sql": "SELECT simple_pay(31, 16, 0);"}'); }
step "s1a172" { SELECT bcdb_tx_submit('{"hash": "11_1", "iso": "SE", "sql": "SELECT simple_pay(19, 49, 0);"}'); }
step "s1a173" { SELECT bcdb_tx_submit('{"hash": "11_2", "iso": "SE", "sql": "SELECT simple_pay(24, 3, 0);"}'); }
step "s1a174" { SELECT bcdb_tx_submit('{"hash": "11_3", "iso": "SE", "sql": "SELECT joint_pay(8, 15, 18, 0, 0);"}'); }
step "s1a175" { SELECT bcdb_tx_submit('{"hash": "11_4", "iso": "SE", "sql": "SELECT simple_pay(21, 3, 0);"}'); }
step "s1a176" { SELECT bcdb_tx_submit('{"hash": "11_5", "iso": "SE", "sql": "SELECT simple_pay(30, 26, 0);"}'); }
step "s1a177" { SELECT bcdb_tx_submit('{"hash": "11_6", "iso": "SE", "sql": "SELECT joint_pay(38, 45, 5, 0, 0);"}'); }
step "s1a178" { SELECT bcdb_tx_submit('{"hash": "11_7", "iso": "SE", "sql": "SELECT simple_pay(9, 22, 0);"}'); }
step "s1a179" { SELECT bcdb_tx_submit('{"hash": "11_8", "iso": "SE", "sql": "SELECT simple_pay(39, 29, 0);"}'); }
step "s1a180" { SELECT bcdb_tx_submit('{"hash": "11_9", "iso": "SE", "sql": "SELECT simple_pay(3, 6, 0);"}'); }
step "s1a181" { SELECT bcdb_tx_submit('{"hash": "11_10", "iso": "SE", "sql": "SELECT simple_pay(9, 1, 0);"}'); }
step "s1a182" { SELECT bcdb_tx_submit('{"hash": "11_11", "iso": "SE", "sql": "SELECT joint_pay(39, 8, 40, 0, 0);"}'); }
step "s1a183" { SELECT bcdb_tx_submit('{"hash": "11_12", "iso": "SE", "sql": "SELECT simple_pay(44, 35, 0);"}'); }
step "s1a184" { SELECT bcdb_tx_submit('{"hash": "11_13", "iso": "SE", "sql": "SELECT simple_pay(12, 24, 0);"}'); }
step "s1a185" { SELECT bcdb_tx_submit('{"hash": "11_14", "iso": "SE", "sql": "SELECT simple_pay(49, 31, 0);"}'); }
step "s1a186" { SELECT bcdb_tx_submit('{"hash": "11_15", "iso": "SE", "sql": "SELECT joint_pay(3, 39, 44, 0, 0);"}'); }
step "s1a187" { SELECT bcdb_block_submit('{"bid": 11, "txs": ["11_0", "11_1", "11_2", "11_3", "11_4", "11_5", "11_6", "11_7", "11_8", "11_9", "11_10", "11_11", "11_12", "11_13", "11_14", "11_15"]}'); }
step "s1a188" { SELECT bcdb_tx_submit('{"hash": "12_0", "iso": "SE", "sql": "SELECT simple_pay(40, 21, 0);"}'); }
step "s1a189" { SELECT bcdb_tx_submit('{"hash": "12_1", "iso": "SE", "sql": "SELECT simple_pay(43, 45, 0);"}'); }
step "s1a190" { SELECT bcdb_tx_submit('{"hash": "12_2", "iso": "SE", "sql": "SELECT simple_pay(8, 24, 0);"}'); }
step "s1a191" { SELECT bcdb_tx_submit('{"hash": "12_3", "iso": "SE", "sql": "SELECT simple_pay(47, 43, 0);"}'); }
step "s1a192" { SELECT bcdb_tx_submit('{"hash": "12_4", "iso": "SE", "sql": "SELECT simple_pay(7, 33, 0);"}'); }
step "s1a193" { SELECT bcdb_tx_submit('{"hash": "12_5", "iso": "SE", "sql": "SELECT simple_pay(12, 2, 0);"}'); }
step "s1a194" { SELECT bcdb_tx_submit('{"hash": "12_6", "iso": "SE", "sql": "SELECT simple_pay(28, 23, 0);"}'); }
step "s1a195" { SELECT bcdb_tx_submit('{"hash": "12_7", "iso": "SE", "sql": "SELECT simple_pay(29, 22, 0);"}'); }
step "s1a196" { SELECT bcdb_tx_submit('{"hash": "12_8", "iso": "SE", "sql": "SELECT simple_pay(4, 2, 0);"}'); }
step "s1a197" { SELECT bcdb_tx_submit('{"hash": "12_9", "iso": "SE", "sql": "SELECT simple_pay(2, 31, 0);"}'); }
step "s1a198" { SELECT bcdb_tx_submit('{"hash": "12_10", "iso": "SE", "sql": "SELECT simple_pay(1, 33, 0);"}'); }
step "s1a199" { SELECT bcdb_tx_submit('{"hash": "12_11", "iso": "SE", "sql": "SELECT simple_pay(36, 13, 0);"}'); }
step "s1a200" { SELECT bcdb_tx_submit('{"hash": "12_12", "iso": "SE", "sql": "SELECT simple_pay(49, 40, 0);"}'); }
step "s1a201" { SELECT bcdb_tx_submit('{"hash": "12_13", "iso": "SE", "sql": "SELECT simple_pay(44, 33, 0);"}'); }
step "s1a202" { SELECT bcdb_tx_submit('{"hash": "12_14", "iso": "SE", "sql": "SELECT simple_pay(19, 7, 0);"}'); }
step "s1a203" { SELECT bcdb_tx_submit('{"hash": "12_15", "iso": "SE", "sql": "SELECT joint_pay(36, 27, 5, 0, 0);"}'); }
step "s1a204" { SELECT bcdb_block_submit('{"bid": 12, "txs": ["12_0", "12_1", "12_2", "12_3", "12_4", "12_5", "12_6", "12_7", "12_8", "12_9", "12_10", "12_11", "12_12", "12_13", "12_14", "12_15"]}'); }
step "s1a205" { SELECT bcdb_tx_submit('{"hash": "13_0", "iso": "SE", "sql": "SELECT simple_pay(26, 4, 0);"}'); }
step "s1a206" { SELECT bcdb_tx_submit('{"hash": "13_1", "iso": "SE", "sql": "SELECT joint_pay(49, 9, 46, 0, 0);"}'); }
step "s1a207" { SELECT bcdb_tx_submit('{"hash": "13_2", "iso": "SE", "sql": "SELECT simple_pay(28, 27, 0);"}'); }
step "s1a208" { SELECT bcdb_tx_submit('{"hash": "13_3", "iso": "SE", "sql": "SELECT simple_pay(1, 31, 0);"}'); }
step "s1a209" { SELECT bcdb_tx_submit('{"hash": "13_4", "iso": "SE", "sql": "SELECT simple_pay(20, 46, 0);"}'); }
step "s1a210" { SELECT bcdb_tx_submit('{"hash": "13_5", "iso": "SE", "sql": "SELECT simple_pay(22, 4, 0);"}'); }
step "s1a211" { SELECT bcdb_tx_submit('{"hash": "13_6", "iso": "SE", "sql": "SELECT joint_pay(44, 1, 22, 0, 0);"}'); }
step "s1a212" { SELECT bcdb_tx_submit('{"hash": "13_7", "iso": "SE", "sql": "SELECT simple_pay(0, 14, 0);"}'); }
step "s1a213" { SELECT bcdb_tx_submit('{"hash": "13_8", "iso": "SE", "sql": "SELECT simple_pay(4, 38, 0);"}'); }
step "s1a214" { SELECT bcdb_tx_submit('{"hash": "13_9", "iso": "SE", "sql": "SELECT simple_pay(13, 0, 0);"}'); }
step "s1a215" { SELECT bcdb_tx_submit('{"hash": "13_10", "iso": "SE", "sql": "SELECT simple_pay(43, 46, 0);"}'); }
step "s1a216" { SELECT bcdb_tx_submit('{"hash": "13_11", "iso": "SE", "sql": "SELECT simple_pay(7, 47, 0);"}'); }
step "s1a217" { SELECT bcdb_tx_submit('{"hash": "13_12", "iso": "SE", "sql": "SELECT joint_pay(23, 44, 1, 0, 0);"}'); }
step "s1a218" { SELECT bcdb_tx_submit('{"hash": "13_13", "iso": "SE", "sql": "SELECT simple_pay(14, 9, 0);"}'); }
step "s1a219" { SELECT bcdb_tx_submit('{"hash": "13_14", "iso": "SE", "sql": "SELECT joint_pay(7, 30, 22, 0, 0);"}'); }
step "s1a220" { SELECT bcdb_tx_submit('{"hash": "13_15", "iso": "SE", "sql": "SELECT simple_pay(16, 8, 0);"}'); }
step "s1a221" { SELECT bcdb_block_submit('{"bid": 13, "txs": ["13_0", "13_1", "13_2", "13_3", "13_4", "13_5", "13_6", "13_7", "13_8", "13_9", "13_10", "13_11", "13_12", "13_13", "13_14", "13_15"]}'); }
step "s1a222" { SELECT bcdb_tx_submit('{"hash": "14_0", "iso": "SE", "sql": "SELECT joint_pay(13, 23, 21, 0, 0);"}'); }
step "s1a223" { SELECT bcdb_tx_submit('{"hash": "14_1", "iso": "SE", "sql": "SELECT simple_pay(18, 35, 0);"}'); }
step "s1a224" { SELECT bcdb_tx_submit('{"hash": "14_2", "iso": "SE", "sql": "SELECT simple_pay(11, 37, 0);"}'); }
step "s1a225" { SELECT bcdb_tx_submit('{"hash": "14_3", "iso": "SE", "sql": "SELECT simple_pay(6, 34, 0);"}'); }
step "s1a226" { SELECT bcdb_tx_submit('{"hash": "14_4", "iso": "SE", "sql": "SELECT simple_pay(10, 24, 0);"}'); }
step "s1a227" { SELECT bcdb_tx_submit('{"hash": "14_5", "iso": "SE", "sql": "SELECT simple_pay(8, 14, 0);"}'); }
step "s1a228" { SELECT bcdb_tx_submit('{"hash": "14_6", "iso": "SE", "sql": "SELECT simple_pay(15, 48, 0);"}'); }
step "s1a229" { SELECT bcdb_tx_submit('{"hash": "14_7", "iso": "SE", "sql": "SELECT joint_pay(23, 26, 42, 0, 0);"}'); }
step "s1a230" { SELECT bcdb_tx_submit('{"hash": "14_8", "iso": "SE", "sql": "SELECT joint_pay(8, 38, 1, 0, 0);"}'); }
step "s1a231" { SELECT bcdb_tx_submit('{"hash": "14_9", "iso": "SE", "sql": "SELECT simple_pay(44, 4, 0);"}'); }
step "s1a232" { SELECT bcdb_tx_submit('{"hash": "14_10", "iso": "SE", "sql": "SELECT joint_pay(19, 35, 26, 0, 0);"}'); }
step "s1a233" { SELECT bcdb_tx_submit('{"hash": "14_11", "iso": "SE", "sql": "SELECT simple_pay(9, 37, 0);"}'); }
step "s1a234" { SELECT bcdb_tx_submit('{"hash": "14_12", "iso": "SE", "sql": "SELECT simple_pay(40, 22, 0);"}'); }
step "s1a235" { SELECT bcdb_tx_submit('{"hash": "14_13", "iso": "SE", "sql": "SELECT joint_pay(28, 40, 23, 0, 0);"}'); }
step "s1a236" { SELECT bcdb_tx_submit('{"hash": "14_14", "iso": "SE", "sql": "SELECT simple_pay(33, 3, 0);"}'); }
step "s1a237" { SELECT bcdb_tx_submit('{"hash": "14_15", "iso": "SE", "sql": "SELECT simple_pay(0, 26, 0);"}'); }
step "s1a238" { SELECT bcdb_block_submit('{"bid": 14, "txs": ["14_0", "14_1", "14_2", "14_3", "14_4", "14_5", "14_6", "14_7", "14_8", "14_9", "14_10", "14_11", "14_12", "14_13", "14_14", "14_15"]}'); }
step "s1a239" { SELECT bcdb_tx_submit('{"hash": "15_0", "iso": "SE", "sql": "SELECT simple_pay(20, 28, 0);"}'); }
step "s1a240" { SELECT bcdb_tx_submit('{"hash": "15_1", "iso": "SE", "sql": "SELECT simple_pay(18, 30, 0);"}'); }
step "s1a241" { SELECT bcdb_tx_submit('{"hash": "15_2", "iso": "SE", "sql": "SELECT joint_pay(11, 6, 17, 0, 0);"}'); }
step "s1a242" { SELECT bcdb_tx_submit('{"hash": "15_3", "iso": "SE", "sql": "SELECT joint_pay(38, 44, 9, 0, 0);"}'); }
step "s1a243" { SELECT bcdb_tx_submit('{"hash": "15_4", "iso": "SE", "sql": "SELECT simple_pay(28, 25, 0);"}'); }
step "s1a244" { SELECT bcdb_tx_submit('{"hash": "15_5", "iso": "SE", "sql": "SELECT joint_pay(26, 27, 11, 0, 0);"}'); }
step "s1a245" { SELECT bcdb_tx_submit('{"hash": "15_6", "iso": "SE", "sql": "SELECT simple_pay(29, 21, 0);"}'); }
step "s1a246" { SELECT bcdb_tx_submit('{"hash": "15_7", "iso": "SE", "sql": "SELECT simple_pay(9, 22, 0);"}'); }
step "s1a247" { SELECT bcdb_tx_submit('{"hash": "15_8", "iso": "SE", "sql": "SELECT simple_pay(40, 5, 0);"}'); }
step "s1a248" { SELECT bcdb_tx_submit('{"hash": "15_9", "iso": "SE", "sql": "SELECT simple_pay(13, 18, 0);"}'); }
step "s1a249" { SELECT bcdb_tx_submit('{"hash": "15_10", "iso": "SE", "sql": "SELECT joint_pay(44, 28, 39, 0, 0);"}'); }
step "s1a250" { SELECT bcdb_tx_submit('{"hash": "15_11", "iso": "SE", "sql": "SELECT simple_pay(13, 19, 0);"}'); }
step "s1a251" { SELECT bcdb_tx_submit('{"hash": "15_12", "iso": "SE", "sql": "SELECT joint_pay(40, 19, 34, 0, 0);"}'); }
step "s1a252" { SELECT bcdb_tx_submit('{"hash": "15_13", "iso": "SE", "sql": "SELECT simple_pay(27, 45, 0);"}'); }
step "s1a253" { SELECT bcdb_tx_submit('{"hash": "15_14", "iso": "SE", "sql": "SELECT simple_pay(5, 43, 0);"}'); }
step "s1a254" { SELECT bcdb_tx_submit('{"hash": "15_15", "iso": "SE", "sql": "SELECT simple_pay(14, 34, 0);"}'); }
step "s1a255" { SELECT bcdb_block_submit('{"bid": 15, "txs": ["15_0", "15_1", "15_2", "15_3", "15_4", "15_5", "15_6", "15_7", "15_8", "15_9", "15_10", "15_11", "15_12", "15_13", "15_14", "15_15"]}'); }
step "s1a256" { SELECT bcdb_tx_submit('{"hash": "16_0", "iso": "SE", "sql": "SELECT simple_pay(17, 40, 0);"}'); }
step "s1a257" { SELECT bcdb_tx_submit('{"hash": "16_1", "iso": "SE", "sql": "SELECT simple_pay(7, 17, 0);"}'); }
step "s1a258" { SELECT bcdb_tx_submit('{"hash": "16_2", "iso": "SE", "sql": "SELECT simple_pay(2, 0, 0);"}'); }
step "s1a259" { SELECT bcdb_tx_submit('{"hash": "16_3", "iso": "SE", "sql": "SELECT simple_pay(33, 37, 0);"}'); }
step "s1a260" { SELECT bcdb_tx_submit('{"hash": "16_4", "iso": "SE", "sql": "SELECT simple_pay(28, 6, 0);"}'); }
step "s1a261" { SELECT bcdb_tx_submit('{"hash": "16_5", "iso": "SE", "sql": "SELECT simple_pay(22, 18, 0);"}'); }
step "s1a262" { SELECT bcdb_tx_submit('{"hash": "16_6", "iso": "SE", "sql": "SELECT simple_pay(43, 12, 0);"}'); }
step "s1a263" { SELECT bcdb_tx_submit('{"hash": "16_7", "iso": "SE", "sql": "SELECT simple_pay(2, 4, 0);"}'); }
step "s1a264" { SELECT bcdb_tx_submit('{"hash": "16_8", "iso": "SE", "sql": "SELECT simple_pay(19, 34, 0);"}'); }
step "s1a265" { SELECT bcdb_tx_submit('{"hash": "16_9", "iso": "SE", "sql": "SELECT simple_pay(33, 15, 0);"}'); }
step "s1a266" { SELECT bcdb_tx_submit('{"hash": "16_10", "iso": "SE", "sql": "SELECT simple_pay(48, 10, 0);"}'); }
step "s1a267" { SELECT bcdb_tx_submit('{"hash": "16_11", "iso": "SE", "sql": "SELECT joint_pay(18, 33, 8, 0, 0);"}'); }
step "s1a268" { SELECT bcdb_tx_submit('{"hash": "16_12", "iso": "SE", "sql": "SELECT simple_pay(40, 13, 0);"}'); }
step "s1a269" { SELECT bcdb_tx_submit('{"hash": "16_13", "iso": "SE", "sql": "SELECT simple_pay(26, 40, 0);"}'); }
step "s1a270" { SELECT bcdb_tx_submit('{"hash": "16_14", "iso": "SE", "sql": "SELECT simple_pay(47, 49, 0);"}'); }
step "s1a271" { SELECT bcdb_tx_submit('{"hash": "16_15", "iso": "SE", "sql": "SELECT simple_pay(17, 18, 0);"}'); }
step "s1a272" { SELECT bcdb_block_submit('{"bid": 16, "txs": ["16_0", "16_1", "16_2", "16_3", "16_4", "16_5", "16_6", "16_7", "16_8", "16_9", "16_10", "16_11", "16_12", "16_13", "16_14", "16_15"]}'); }
step "s1a273" { SELECT bcdb_tx_submit('{"hash": "17_0", "iso": "SE", "sql": "SELECT simple_pay(36, 40, 0);"}'); }
step "s1a274" { SELECT bcdb_tx_submit('{"hash": "17_1", "iso": "SE", "sql": "SELECT joint_pay(7, 44, 24, 0, 0);"}'); }
step "s1a275" { SELECT bcdb_tx_submit('{"hash": "17_2", "iso": "SE", "sql": "SELECT simple_pay(29, 8, 0);"}'); }
step "s1a276" { SELECT bcdb_tx_submit('{"hash": "17_3", "iso": "SE", "sql": "SELECT simple_pay(19, 22, 0);"}'); }
step "s1a277" { SELECT bcdb_tx_submit('{"hash": "17_4", "iso": "SE", "sql": "SELECT simple_pay(47, 26, 0);"}'); }
step "s1a278" { SELECT bcdb_tx_submit('{"hash": "17_5", "iso": "SE", "sql": "SELECT simple_pay(31, 44, 0);"}'); }
step "s1a279" { SELECT bcdb_tx_submit('{"hash": "17_6", "iso": "SE", "sql": "SELECT simple_pay(31, 41, 0);"}'); }
step "s1a280" { SELECT bcdb_tx_submit('{"hash": "17_7", "iso": "SE", "sql": "SELECT simple_pay(28, 19, 0);"}'); }
step "s1a281" { SELECT bcdb_tx_submit('{"hash": "17_8", "iso": "SE", "sql": "SELECT joint_pay(31, 3, 39, 0, 0);"}'); }
step "s1a282" { SELECT bcdb_tx_submit('{"hash": "17_9", "iso": "SE", "sql": "SELECT simple_pay(22, 30, 0);"}'); }
step "s1a283" { SELECT bcdb_tx_submit('{"hash": "17_10", "iso": "SE", "sql": "SELECT simple_pay(0, 33, 0);"}'); }
step "s1a284" { SELECT bcdb_tx_submit('{"hash": "17_11", "iso": "SE", "sql": "SELECT simple_pay(43, 5, 0);"}'); }
step "s1a285" { SELECT bcdb_tx_submit('{"hash": "17_12", "iso": "SE", "sql": "SELECT simple_pay(47, 42, 0);"}'); }
step "s1a286" { SELECT bcdb_tx_submit('{"hash": "17_13", "iso": "SE", "sql": "SELECT simple_pay(23, 2, 0);"}'); }
step "s1a287" { SELECT bcdb_tx_submit('{"hash": "17_14", "iso": "SE", "sql": "SELECT joint_pay(0, 17, 40, 0, 0);"}'); }
step "s1a288" { SELECT bcdb_tx_submit('{"hash": "17_15", "iso": "SE", "sql": "SELECT simple_pay(46, 14, 0);"}'); }
step "s1a289" { SELECT bcdb_block_submit('{"bid": 17, "txs": ["17_0", "17_1", "17_2", "17_3", "17_4", "17_5", "17_6", "17_7", "17_8", "17_9", "17_10", "17_11", "17_12", "17_13", "17_14", "17_15"]}'); }
step "s1a290" { SELECT bcdb_tx_submit('{"hash": "18_0", "iso": "SE", "sql": "SELECT joint_pay(36, 18, 12, 0, 0);"}'); }
step "s1a291" { SELECT bcdb_tx_submit('{"hash": "18_1", "iso": "SE", "sql": "SELECT joint_pay(29, 45, 21, 0, 0);"}'); }
step "s1a292" { SELECT bcdb_tx_submit('{"hash": "18_2", "iso": "SE", "sql": "SELECT simple_pay(21, 26, 0);"}'); }
step "s1a293" { SELECT bcdb_tx_submit('{"hash": "18_3", "iso": "SE", "sql": "SELECT simple_pay(43, 27, 0);"}'); }
step "s1a294" { SELECT bcdb_tx_submit('{"hash": "18_4", "iso": "SE", "sql": "SELECT joint_pay(45, 9, 33, 0, 0);"}'); }
step "s1a295" { SELECT bcdb_tx_submit('{"hash": "18_5", "iso": "SE", "sql": "SELECT simple_pay(13, 11, 0);"}'); }
step "s1a296" { SELECT bcdb_tx_submit('{"hash": "18_6", "iso": "SE", "sql": "SELECT simple_pay(24, 27, 0);"}'); }
step "s1a297" { SELECT bcdb_tx_submit('{"hash": "18_7", "iso": "SE", "sql": "SELECT simple_pay(24, 46, 0);"}'); }
step "s1a298" { SELECT bcdb_tx_submit('{"hash": "18_8", "iso": "SE", "sql": "SELECT simple_pay(12, 28, 0);"}'); }
step "s1a299" { SELECT bcdb_tx_submit('{"hash": "18_9", "iso": "SE", "sql": "SELECT simple_pay(37, 45, 0);"}'); }
step "s1a300" { SELECT bcdb_tx_submit('{"hash": "18_10", "iso": "SE", "sql": "SELECT joint_pay(24, 2, 14, 0, 0);"}'); }
step "s1a301" { SELECT bcdb_tx_submit('{"hash": "18_11", "iso": "SE", "sql": "SELECT simple_pay(11, 23, 0);"}'); }
step "s1a302" { SELECT bcdb_tx_submit('{"hash": "18_12", "iso": "SE", "sql": "SELECT joint_pay(40, 43, 11, 0, 0);"}'); }
step "s1a303" { SELECT bcdb_tx_submit('{"hash": "18_13", "iso": "SE", "sql": "SELECT simple_pay(19, 39, 0);"}'); }
step "s1a304" { SELECT bcdb_tx_submit('{"hash": "18_14", "iso": "SE", "sql": "SELECT joint_pay(32, 48, 18, 0, 0);"}'); }
step "s1a305" { SELECT bcdb_tx_submit('{"hash": "18_15", "iso": "SE", "sql": "SELECT simple_pay(22, 26, 0);"}'); }
step "s1a306" { SELECT bcdb_block_submit('{"bid": 18, "txs": ["18_0", "18_1", "18_2", "18_3", "18_4", "18_5", "18_6", "18_7", "18_8", "18_9", "18_10", "18_11", "18_12", "18_13", "18_14", "18_15"]}'); }
step "s1a307" { SELECT bcdb_tx_submit('{"hash": "19_0", "iso": "SE", "sql": "SELECT simple_pay(40, 44, 0);"}'); }
step "s1a308" { SELECT bcdb_tx_submit('{"hash": "19_1", "iso": "SE", "sql": "SELECT simple_pay(41, 35, 0);"}'); }
step "s1a309" { SELECT bcdb_tx_submit('{"hash": "19_2", "iso": "SE", "sql": "SELECT simple_pay(27, 37, 0);"}'); }
step "s1a310" { SELECT bcdb_tx_submit('{"hash": "19_3", "iso": "SE", "sql": "SELECT simple_pay(16, 45, 0);"}'); }
step "s1a311" { SELECT bcdb_tx_submit('{"hash": "19_4", "iso": "SE", "sql": "SELECT simple_pay(21, 17, 0);"}'); }
step "s1a312" { SELECT bcdb_tx_submit('{"hash": "19_5", "iso": "SE", "sql": "SELECT joint_pay(3, 10, 22, 0, 0);"}'); }
step "s1a313" { SELECT bcdb_tx_submit('{"hash": "19_6", "iso": "SE", "sql": "SELECT joint_pay(41, 0, 8, 0, 0);"}'); }
step "s1a314" { SELECT bcdb_tx_submit('{"hash": "19_7", "iso": "SE", "sql": "SELECT joint_pay(27, 43, 14, 0, 0);"}'); }
step "s1a315" { SELECT bcdb_tx_submit('{"hash": "19_8", "iso": "SE", "sql": "SELECT simple_pay(25, 35, 0);"}'); }
step "s1a316" { SELECT bcdb_tx_submit('{"hash": "19_9", "iso": "SE", "sql": "SELECT simple_pay(29, 12, 0);"}'); }
step "s1a317" { SELECT bcdb_tx_submit('{"hash": "19_10", "iso": "SE", "sql": "SELECT simple_pay(6, 38, 0);"}'); }
step "s1a318" { SELECT bcdb_tx_submit('{"hash": "19_11", "iso": "SE", "sql": "SELECT simple_pay(20, 34, 0);"}'); }
step "s1a319" { SELECT bcdb_tx_submit('{"hash": "19_12", "iso": "SE", "sql": "SELECT simple_pay(20, 16, 0);"}'); }
step "s1a320" { SELECT bcdb_tx_submit('{"hash": "19_13", "iso": "SE", "sql": "SELECT joint_pay(2, 12, 23, 0, 0);"}'); }
step "s1a321" { SELECT bcdb_tx_submit('{"hash": "19_14", "iso": "SE", "sql": "SELECT joint_pay(33, 22, 12, 0, 0);"}'); }
step "s1a322" { SELECT bcdb_tx_submit('{"hash": "19_15", "iso": "SE", "sql": "SELECT simple_pay(16, 43, 0);"}'); }
step "s1a323" { SELECT bcdb_block_submit('{"bid": 19, "txs": ["19_0", "19_1", "19_2", "19_3", "19_4", "19_5", "19_6", "19_7", "19_8", "19_9", "19_10", "19_11", "19_12", "19_13", "19_14", "19_15"]}'); }
step "s1a324" { SELECT bcdb_tx_submit('{"hash": "20_0", "iso": "SE", "sql": "SELECT simple_pay(19, 33, 0);"}'); }
step "s1a325" { SELECT bcdb_tx_submit('{"hash": "20_1", "iso": "SE", "sql": "SELECT simple_pay(16, 30, 0);"}'); }
step "s1a326" { SELECT bcdb_tx_submit('{"hash": "20_2", "iso": "SE", "sql": "SELECT simple_pay(45, 15, 0);"}'); }
step "s1a327" { SELECT bcdb_tx_submit('{"hash": "20_3", "iso": "SE", "sql": "SELECT joint_pay(35, 4, 0, 0, 0);"}'); }
step "s1a328" { SELECT bcdb_tx_submit('{"hash": "20_4", "iso": "SE", "sql": "SELECT simple_pay(46, 28, 0);"}'); }
step "s1a329" { SELECT bcdb_tx_submit('{"hash": "20_5", "iso": "SE", "sql": "SELECT joint_pay(26, 31, 29, 0, 0);"}'); }
step "s1a330" { SELECT bcdb_tx_submit('{"hash": "20_6", "iso": "SE", "sql": "SELECT simple_pay(5, 15, 0);"}'); }
step "s1a331" { SELECT bcdb_tx_submit('{"hash": "20_7", "iso": "SE", "sql": "SELECT joint_pay(48, 9, 26, 0, 0);"}'); }
step "s1a332" { SELECT bcdb_tx_submit('{"hash": "20_8", "iso": "SE", "sql": "SELECT simple_pay(13, 28, 0);"}'); }
step "s1a333" { SELECT bcdb_tx_submit('{"hash": "20_9", "iso": "SE", "sql": "SELECT simple_pay(27, 35, 0);"}'); }
step "s1a334" { SELECT bcdb_tx_submit('{"hash": "20_10", "iso": "SE", "sql": "SELECT simple_pay(25, 2, 0);"}'); }
step "s1a335" { SELECT bcdb_tx_submit('{"hash": "20_11", "iso": "SE", "sql": "SELECT simple_pay(15, 31, 0);"}'); }
step "s1a336" { SELECT bcdb_tx_submit('{"hash": "20_12", "iso": "SE", "sql": "SELECT simple_pay(17, 22, 0);"}'); }
step "s1a337" { SELECT bcdb_tx_submit('{"hash": "20_13", "iso": "SE", "sql": "SELECT simple_pay(27, 6, 0);"}'); }
step "s1a338" { SELECT bcdb_tx_submit('{"hash": "20_14", "iso": "SE", "sql": "SELECT simple_pay(18, 39, 0);"}'); }
step "s1a339" { SELECT bcdb_tx_submit('{"hash": "20_15", "iso": "SE", "sql": "SELECT simple_pay(12, 45, 0);"}'); }
step "s1a340" { SELECT bcdb_block_submit('{"bid": 20, "txs": ["20_0", "20_1", "20_2", "20_3", "20_4", "20_5", "20_6", "20_7", "20_8", "20_9", "20_10", "20_11", "20_12", "20_13", "20_14", "20_15"]}'); }
step "s1a341" { SELECT bcdb_tx_submit('{"hash": "21_0", "iso": "SE", "sql": "SELECT simple_pay(28, 32, 0);"}'); }
step "s1a342" { SELECT bcdb_tx_submit('{"hash": "21_1", "iso": "SE", "sql": "SELECT simple_pay(34, 40, 0);"}'); }
step "s1a343" { SELECT bcdb_tx_submit('{"hash": "21_2", "iso": "SE", "sql": "SELECT simple_pay(14, 1, 0);"}'); }
step "s1a344" { SELECT bcdb_tx_submit('{"hash": "21_3", "iso": "SE", "sql": "SELECT joint_pay(45, 6, 11, 0, 0);"}'); }
step "s1a345" { SELECT bcdb_tx_submit('{"hash": "21_4", "iso": "SE", "sql": "SELECT simple_pay(15, 13, 0);"}'); }
step "s1a346" { SELECT bcdb_tx_submit('{"hash": "21_5", "iso": "SE", "sql": "SELECT simple_pay(47, 42, 0);"}'); }
step "s1a347" { SELECT bcdb_tx_submit('{"hash": "21_6", "iso": "SE", "sql": "SELECT joint_pay(34, 32, 27, 0, 0);"}'); }
step "s1a348" { SELECT bcdb_tx_submit('{"hash": "21_7", "iso": "SE", "sql": "SELECT simple_pay(7, 24, 0);"}'); }
step "s1a349" { SELECT bcdb_tx_submit('{"hash": "21_8", "iso": "SE", "sql": "SELECT simple_pay(7, 47, 0);"}'); }
step "s1a350" { SELECT bcdb_tx_submit('{"hash": "21_9", "iso": "SE", "sql": "SELECT simple_pay(14, 43, 0);"}'); }
step "s1a351" { SELECT bcdb_tx_submit('{"hash": "21_10", "iso": "SE", "sql": "SELECT simple_pay(34, 42, 0);"}'); }
step "s1a352" { SELECT bcdb_tx_submit('{"hash": "21_11", "iso": "SE", "sql": "SELECT simple_pay(47, 15, 0);"}'); }
step "s1a353" { SELECT bcdb_tx_submit('{"hash": "21_12", "iso": "SE", "sql": "SELECT joint_pay(19, 43, 20, 0, 0);"}'); }
step "s1a354" { SELECT bcdb_tx_submit('{"hash": "21_13", "iso": "SE", "sql": "SELECT simple_pay(40, 30, 0);"}'); }
step "s1a355" { SELECT bcdb_tx_submit('{"hash": "21_14", "iso": "SE", "sql": "SELECT simple_pay(10, 8, 0);"}'); }
step "s1a356" { SELECT bcdb_tx_submit('{"hash": "21_15", "iso": "SE", "sql": "SELECT simple_pay(35, 32, 0);"}'); }
step "s1a357" { SELECT bcdb_block_submit('{"bid": 21, "txs": ["21_0", "21_1", "21_2", "21_3", "21_4", "21_5", "21_6", "21_7", "21_8", "21_9", "21_10", "21_11", "21_12", "21_13", "21_14", "21_15"]}'); }
step "s1a358" { SELECT bcdb_tx_submit('{"hash": "22_0", "iso": "SE", "sql": "SELECT simple_pay(37, 40, 0);"}'); }
step "s1a359" { SELECT bcdb_tx_submit('{"hash": "22_1", "iso": "SE", "sql": "SELECT joint_pay(8, 25, 9, 0, 0);"}'); }
step "s1a360" { SELECT bcdb_tx_submit('{"hash": "22_2", "iso": "SE", "sql": "SELECT simple_pay(32, 4, 0);"}'); }
step "s1a361" { SELECT bcdb_tx_submit('{"hash": "22_3", "iso": "SE", "sql": "SELECT joint_pay(13, 49, 31, 0, 0);"}'); }
step "s1a362" { SELECT bcdb_tx_submit('{"hash": "22_4", "iso": "SE", "sql": "SELECT simple_pay(44, 13, 0);"}'); }
step "s1a363" { SELECT bcdb_tx_submit('{"hash": "22_5", "iso": "SE", "sql": "SELECT simple_pay(8, 14, 0);"}'); }
step "s1a364" { SELECT bcdb_tx_submit('{"hash": "22_6", "iso": "SE", "sql": "SELECT simple_pay(22, 38, 0);"}'); }
step "s1a365" { SELECT bcdb_tx_submit('{"hash": "22_7", "iso": "SE", "sql": "SELECT simple_pay(40, 31, 0);"}'); }
step "s1a366" { SELECT bcdb_tx_submit('{"hash": "22_8", "iso": "SE", "sql": "SELECT simple_pay(6, 39, 0);"}'); }
step "s1a367" { SELECT bcdb_tx_submit('{"hash": "22_9", "iso": "SE", "sql": "SELECT simple_pay(33, 38, 0);"}'); }
step "s1a368" { SELECT bcdb_tx_submit('{"hash": "22_10", "iso": "SE", "sql": "SELECT simple_pay(29, 19, 0);"}'); }
step "s1a369" { SELECT bcdb_tx_submit('{"hash": "22_11", "iso": "SE", "sql": "SELECT joint_pay(14, 35, 41, 0, 0);"}'); }
step "s1a370" { SELECT bcdb_tx_submit('{"hash": "22_12", "iso": "SE", "sql": "SELECT joint_pay(31, 47, 30, 0, 0);"}'); }
step "s1a371" { SELECT bcdb_tx_submit('{"hash": "22_13", "iso": "SE", "sql": "SELECT simple_pay(45, 5, 0);"}'); }
step "s1a372" { SELECT bcdb_tx_submit('{"hash": "22_14", "iso": "SE", "sql": "SELECT simple_pay(38, 25, 0);"}'); }
step "s1a373" { SELECT bcdb_tx_submit('{"hash": "22_15", "iso": "SE", "sql": "SELECT simple_pay(20, 18, 0);"}'); }
step "s1a374" { SELECT bcdb_block_submit('{"bid": 22, "txs": ["22_0", "22_1", "22_2", "22_3", "22_4", "22_5", "22_6", "22_7", "22_8", "22_9", "22_10", "22_11", "22_12", "22_13", "22_14", "22_15"]}'); }
step "s1a375" { SELECT bcdb_tx_submit('{"hash": "23_0", "iso": "SE", "sql": "SELECT simple_pay(3, 13, 0);"}'); }
step "s1a376" { SELECT bcdb_tx_submit('{"hash": "23_1", "iso": "SE", "sql": "SELECT joint_pay(46, 47, 15, 0, 0);"}'); }
step "s1a377" { SELECT bcdb_tx_submit('{"hash": "23_2", "iso": "SE", "sql": "SELECT simple_pay(28, 42, 0);"}'); }
step "s1a378" { SELECT bcdb_tx_submit('{"hash": "23_3", "iso": "SE", "sql": "SELECT simple_pay(42, 14, 0);"}'); }
step "s1a379" { SELECT bcdb_tx_submit('{"hash": "23_4", "iso": "SE", "sql": "SELECT simple_pay(42, 10, 0);"}'); }
step "s1a380" { SELECT bcdb_tx_submit('{"hash": "23_5", "iso": "SE", "sql": "SELECT simple_pay(22, 36, 0);"}'); }
step "s1a381" { SELECT bcdb_tx_submit('{"hash": "23_6", "iso": "SE", "sql": "SELECT simple_pay(46, 40, 0);"}'); }
step "s1a382" { SELECT bcdb_tx_submit('{"hash": "23_7", "iso": "SE", "sql": "SELECT joint_pay(1, 31, 40, 0, 0);"}'); }
step "s1a383" { SELECT bcdb_tx_submit('{"hash": "23_8", "iso": "SE", "sql": "SELECT joint_pay(15, 2, 0, 0, 0);"}'); }
step "s1a384" { SELECT bcdb_tx_submit('{"hash": "23_9", "iso": "SE", "sql": "SELECT simple_pay(41, 20, 0);"}'); }
step "s1a385" { SELECT bcdb_tx_submit('{"hash": "23_10", "iso": "SE", "sql": "SELECT joint_pay(3, 22, 42, 0, 0);"}'); }
step "s1a386" { SELECT bcdb_tx_submit('{"hash": "23_11", "iso": "SE", "sql": "SELECT simple_pay(13, 28, 0);"}'); }
step "s1a387" { SELECT bcdb_tx_submit('{"hash": "23_12", "iso": "SE", "sql": "SELECT simple_pay(22, 19, 0);"}'); }
step "s1a388" { SELECT bcdb_tx_submit('{"hash": "23_13", "iso": "SE", "sql": "SELECT joint_pay(21, 46, 47, 0, 0);"}'); }
step "s1a389" { SELECT bcdb_tx_submit('{"hash": "23_14", "iso": "SE", "sql": "SELECT simple_pay(0, 26, 0);"}'); }
step "s1a390" { SELECT bcdb_tx_submit('{"hash": "23_15", "iso": "SE", "sql": "SELECT simple_pay(34, 47, 0);"}'); }
step "s1a391" { SELECT bcdb_block_submit('{"bid": 23, "txs": ["23_0", "23_1", "23_2", "23_3", "23_4", "23_5", "23_6", "23_7", "23_8", "23_9", "23_10", "23_11", "23_12", "23_13", "23_14", "23_15"]}'); }
step "s1a392" { SELECT bcdb_tx_submit('{"hash": "24_0", "iso": "SE", "sql": "SELECT simple_pay(45, 29, 0);"}'); }
step "s1a393" { SELECT bcdb_tx_submit('{"hash": "24_1", "iso": "SE", "sql": "SELECT simple_pay(36, 7, 0);"}'); }
step "s1a394" { SELECT bcdb_tx_submit('{"hash": "24_2", "iso": "SE", "sql": "SELECT simple_pay(24, 10, 0);"}'); }
step "s1a395" { SELECT bcdb_tx_submit('{"hash": "24_3", "iso": "SE", "sql": "SELECT joint_pay(8, 39, 42, 0, 0);"}'); }
step "s1a396" { SELECT bcdb_tx_submit('{"hash": "24_4", "iso": "SE", "sql": "SELECT simple_pay(46, 44, 0);"}'); }
step "s1a397" { SELECT bcdb_tx_submit('{"hash": "24_5", "iso": "SE", "sql": "SELECT joint_pay(21, 15, 11, 0, 0);"}'); }
step "s1a398" { SELECT bcdb_tx_submit('{"hash": "24_6", "iso": "SE", "sql": "SELECT simple_pay(1, 10, 0);"}'); }
step "s1a399" { SELECT bcdb_tx_submit('{"hash": "24_7", "iso": "SE", "sql": "SELECT simple_pay(43, 35, 0);"}'); }
step "s1a400" { SELECT bcdb_tx_submit('{"hash": "24_8", "iso": "SE", "sql": "SELECT joint_pay(5, 27, 38, 0, 0);"}'); }
step "s1a401" { SELECT bcdb_tx_submit('{"hash": "24_9", "iso": "SE", "sql": "SELECT joint_pay(40, 29, 45, 0, 0);"}'); }
step "s1a402" { SELECT bcdb_tx_submit('{"hash": "24_10", "iso": "SE", "sql": "SELECT joint_pay(38, 2, 16, 0, 0);"}'); }
step "s1a403" { SELECT bcdb_tx_submit('{"hash": "24_11", "iso": "SE", "sql": "SELECT simple_pay(47, 46, 0);"}'); }
step "s1a404" { SELECT bcdb_tx_submit('{"hash": "24_12", "iso": "SE", "sql": "SELECT simple_pay(40, 2, 0);"}'); }
step "s1a405" { SELECT bcdb_tx_submit('{"hash": "24_13", "iso": "SE", "sql": "SELECT simple_pay(22, 18, 0);"}'); }
step "s1a406" { SELECT bcdb_tx_submit('{"hash": "24_14", "iso": "SE", "sql": "SELECT simple_pay(29, 15, 0);"}'); }
step "s1a407" { SELECT bcdb_tx_submit('{"hash": "24_15", "iso": "SE", "sql": "SELECT simple_pay(10, 47, 0);"}'); }
step "s1a408" { SELECT bcdb_block_submit('{"bid": 24, "txs": ["24_0", "24_1", "24_2", "24_3", "24_4", "24_5", "24_6", "24_7", "24_8", "24_9", "24_10", "24_11", "24_12", "24_13", "24_14", "24_15"]}'); }
step "s1a409" { SELECT bcdb_tx_submit('{"hash": "25_0", "iso": "SE", "sql": "SELECT simple_pay(21, 17, 0);"}'); }
step "s1a410" { SELECT bcdb_tx_submit('{"hash": "25_1", "iso": "SE", "sql": "SELECT simple_pay(25, 0, 0);"}'); }
step "s1a411" { SELECT bcdb_tx_submit('{"hash": "25_2", "iso": "SE", "sql": "SELECT simple_pay(18, 35, 0);"}'); }
step "s1a412" { SELECT bcdb_tx_submit('{"hash": "25_3", "iso": "SE", "sql": "SELECT simple_pay(2, 49, 0);"}'); }
step "s1a413" { SELECT bcdb_tx_submit('{"hash": "25_4", "iso": "SE", "sql": "SELECT simple_pay(35, 16, 0);"}'); }
step "s1a414" { SELECT bcdb_tx_submit('{"hash": "25_5", "iso": "SE", "sql": "SELECT simple_pay(2, 29, 0);"}'); }
step "s1a415" { SELECT bcdb_tx_submit('{"hash": "25_6", "iso": "SE", "sql": "SELECT simple_pay(7, 25, 0);"}'); }
step "s1a416" { SELECT bcdb_tx_submit('{"hash": "25_7", "iso": "SE", "sql": "SELECT simple_pay(3, 1, 0);"}'); }
step "s1a417" { SELECT bcdb_tx_submit('{"hash": "25_8", "iso": "SE", "sql": "SELECT simple_pay(2, 16, 0);"}'); }
step "s1a418" { SELECT bcdb_tx_submit('{"hash": "25_9", "iso": "SE", "sql": "SELECT simple_pay(37, 44, 0);"}'); }
step "s1a419" { SELECT bcdb_tx_submit('{"hash": "25_10", "iso": "SE", "sql": "SELECT simple_pay(18, 43, 0);"}'); }
step "s1a420" { SELECT bcdb_tx_submit('{"hash": "25_11", "iso": "SE", "sql": "SELECT simple_pay(48, 33, 0);"}'); }
step "s1a421" { SELECT bcdb_tx_submit('{"hash": "25_12", "iso": "SE", "sql": "SELECT simple_pay(24, 16, 0);"}'); }
step "s1a422" { SELECT bcdb_tx_submit('{"hash": "25_13", "iso": "SE", "sql": "SELECT simple_pay(36, 21, 0);"}'); }
step "s1a423" { SELECT bcdb_tx_submit('{"hash": "25_14", "iso": "SE", "sql": "SELECT simple_pay(15, 37, 0);"}'); }
step "s1a424" { SELECT bcdb_tx_submit('{"hash": "25_15", "iso": "SE", "sql": "SELECT simple_pay(34, 43, 0);"}'); }
step "s1a425" { SELECT bcdb_block_submit('{"bid": 25, "txs": ["25_0", "25_1", "25_2", "25_3", "25_4", "25_5", "25_6", "25_7", "25_8", "25_9", "25_10", "25_11", "25_12", "25_13", "25_14", "25_15"]}'); }
step "s1a426" { SELECT bcdb_tx_submit('{"hash": "26_0", "iso": "SE", "sql": "SELECT simple_pay(10, 9, 0);"}'); }
step "s1a427" { SELECT bcdb_tx_submit('{"hash": "26_1", "iso": "SE", "sql": "SELECT simple_pay(47, 0, 0);"}'); }
step "s1a428" { SELECT bcdb_tx_submit('{"hash": "26_2", "iso": "SE", "sql": "SELECT simple_pay(3, 36, 0);"}'); }
step "s1a429" { SELECT bcdb_tx_submit('{"hash": "26_3", "iso": "SE", "sql": "SELECT joint_pay(22, 23, 18, 0, 0);"}'); }
step "s1a430" { SELECT bcdb_tx_submit('{"hash": "26_4", "iso": "SE", "sql": "SELECT simple_pay(20, 31, 0);"}'); }
step "s1a431" { SELECT bcdb_tx_submit('{"hash": "26_5", "iso": "SE", "sql": "SELECT simple_pay(38, 27, 0);"}'); }
step "s1a432" { SELECT bcdb_tx_submit('{"hash": "26_6", "iso": "SE", "sql": "SELECT simple_pay(0, 9, 0);"}'); }
step "s1a433" { SELECT bcdb_tx_submit('{"hash": "26_7", "iso": "SE", "sql": "SELECT simple_pay(28, 8, 0);"}'); }
step "s1a434" { SELECT bcdb_tx_submit('{"hash": "26_8", "iso": "SE", "sql": "SELECT simple_pay(0, 46, 0);"}'); }
step "s1a435" { SELECT bcdb_tx_submit('{"hash": "26_9", "iso": "SE", "sql": "SELECT simple_pay(42, 49, 0);"}'); }
step "s1a436" { SELECT bcdb_tx_submit('{"hash": "26_10", "iso": "SE", "sql": "SELECT simple_pay(39, 12, 0);"}'); }
step "s1a437" { SELECT bcdb_tx_submit('{"hash": "26_11", "iso": "SE", "sql": "SELECT joint_pay(27, 17, 11, 0, 0);"}'); }
step "s1a438" { SELECT bcdb_tx_submit('{"hash": "26_12", "iso": "SE", "sql": "SELECT simple_pay(4, 42, 0);"}'); }
step "s1a439" { SELECT bcdb_tx_submit('{"hash": "26_13", "iso": "SE", "sql": "SELECT simple_pay(37, 7, 0);"}'); }
step "s1a440" { SELECT bcdb_tx_submit('{"hash": "26_14", "iso": "SE", "sql": "SELECT simple_pay(40, 34, 0);"}'); }
step "s1a441" { SELECT bcdb_tx_submit('{"hash": "26_15", "iso": "SE", "sql": "SELECT simple_pay(48, 27, 0);"}'); }
step "s1a442" { SELECT bcdb_block_submit('{"bid": 26, "txs": ["26_0", "26_1", "26_2", "26_3", "26_4", "26_5", "26_6", "26_7", "26_8", "26_9", "26_10", "26_11", "26_12", "26_13", "26_14", "26_15"]}'); }
step "s1a443" { SELECT bcdb_tx_submit('{"hash": "27_0", "iso": "SE", "sql": "SELECT simple_pay(18, 0, 0);"}'); }
step "s1a444" { SELECT bcdb_tx_submit('{"hash": "27_1", "iso": "SE", "sql": "SELECT simple_pay(45, 17, 0);"}'); }
step "s1a445" { SELECT bcdb_tx_submit('{"hash": "27_2", "iso": "SE", "sql": "SELECT simple_pay(34, 33, 0);"}'); }
step "s1a446" { SELECT bcdb_tx_submit('{"hash": "27_3", "iso": "SE", "sql": "SELECT simple_pay(21, 12, 0);"}'); }
step "s1a447" { SELECT bcdb_tx_submit('{"hash": "27_4", "iso": "SE", "sql": "SELECT simple_pay(27, 9, 0);"}'); }
step "s1a448" { SELECT bcdb_tx_submit('{"hash": "27_5", "iso": "SE", "sql": "SELECT simple_pay(48, 32, 0);"}'); }
step "s1a449" { SELECT bcdb_tx_submit('{"hash": "27_6", "iso": "SE", "sql": "SELECT joint_pay(42, 44, 36, 0, 0);"}'); }
step "s1a450" { SELECT bcdb_tx_submit('{"hash": "27_7", "iso": "SE", "sql": "SELECT simple_pay(29, 2, 0);"}'); }
step "s1a451" { SELECT bcdb_tx_submit('{"hash": "27_8", "iso": "SE", "sql": "SELECT simple_pay(26, 40, 0);"}'); }
step "s1a452" { SELECT bcdb_tx_submit('{"hash": "27_9", "iso": "SE", "sql": "SELECT simple_pay(48, 14, 0);"}'); }
step "s1a453" { SELECT bcdb_tx_submit('{"hash": "27_10", "iso": "SE", "sql": "SELECT simple_pay(23, 33, 0);"}'); }
step "s1a454" { SELECT bcdb_tx_submit('{"hash": "27_11", "iso": "SE", "sql": "SELECT simple_pay(10, 43, 0);"}'); }
step "s1a455" { SELECT bcdb_tx_submit('{"hash": "27_12", "iso": "SE", "sql": "SELECT joint_pay(22, 40, 44, 0, 0);"}'); }
step "s1a456" { SELECT bcdb_tx_submit('{"hash": "27_13", "iso": "SE", "sql": "SELECT simple_pay(46, 47, 0);"}'); }
step "s1a457" { SELECT bcdb_tx_submit('{"hash": "27_14", "iso": "SE", "sql": "SELECT simple_pay(15, 17, 0);"}'); }
step "s1a458" { SELECT bcdb_tx_submit('{"hash": "27_15", "iso": "SE", "sql": "SELECT joint_pay(48, 26, 4, 0, 0);"}'); }
step "s1a459" { SELECT bcdb_block_submit('{"bid": 27, "txs": ["27_0", "27_1", "27_2", "27_3", "27_4", "27_5", "27_6", "27_7", "27_8", "27_9", "27_10", "27_11", "27_12", "27_13", "27_14", "27_15"]}'); }
step "s1a460" { SELECT bcdb_tx_submit('{"hash": "28_0", "iso": "SE", "sql": "SELECT simple_pay(15, 47, 0);"}'); }
step "s1a461" { SELECT bcdb_tx_submit('{"hash": "28_1", "iso": "SE", "sql": "SELECT simple_pay(32, 45, 0);"}'); }
step "s1a462" { SELECT bcdb_tx_submit('{"hash": "28_2", "iso": "SE", "sql": "SELECT joint_pay(12, 10, 28, 0, 0);"}'); }
step "s1a463" { SELECT bcdb_tx_submit('{"hash": "28_3", "iso": "SE", "sql": "SELECT simple_pay(27, 40, 0);"}'); }
step "s1a464" { SELECT bcdb_tx_submit('{"hash": "28_4", "iso": "SE", "sql": "SELECT simple_pay(17, 16, 0);"}'); }
step "s1a465" { SELECT bcdb_tx_submit('{"hash": "28_5", "iso": "SE", "sql": "SELECT simple_pay(48, 49, 0);"}'); }
step "s1a466" { SELECT bcdb_tx_submit('{"hash": "28_6", "iso": "SE", "sql": "SELECT simple_pay(20, 5, 0);"}'); }
step "s1a467" { SELECT bcdb_tx_submit('{"hash": "28_7", "iso": "SE", "sql": "SELECT simple_pay(31, 0, 0);"}'); }
step "s1a468" { SELECT bcdb_tx_submit('{"hash": "28_8", "iso": "SE", "sql": "SELECT simple_pay(12, 48, 0);"}'); }
step "s1a469" { SELECT bcdb_tx_submit('{"hash": "28_9", "iso": "SE", "sql": "SELECT simple_pay(27, 49, 0);"}'); }
step "s1a470" { SELECT bcdb_tx_submit('{"hash": "28_10", "iso": "SE", "sql": "SELECT simple_pay(43, 24, 0);"}'); }
step "s1a471" { SELECT bcdb_tx_submit('{"hash": "28_11", "iso": "SE", "sql": "SELECT simple_pay(2, 37, 0);"}'); }
step "s1a472" { SELECT bcdb_tx_submit('{"hash": "28_12", "iso": "SE", "sql": "SELECT simple_pay(36, 8, 0);"}'); }
step "s1a473" { SELECT bcdb_tx_submit('{"hash": "28_13", "iso": "SE", "sql": "SELECT simple_pay(17, 20, 0);"}'); }
step "s1a474" { SELECT bcdb_tx_submit('{"hash": "28_14", "iso": "SE", "sql": "SELECT simple_pay(25, 30, 0);"}'); }
step "s1a475" { SELECT bcdb_tx_submit('{"hash": "28_15", "iso": "SE", "sql": "SELECT simple_pay(8, 2, 0);"}'); }
step "s1a476" { SELECT bcdb_block_submit('{"bid": 28, "txs": ["28_0", "28_1", "28_2", "28_3", "28_4", "28_5", "28_6", "28_7", "28_8", "28_9", "28_10", "28_11", "28_12", "28_13", "28_14", "28_15"]}'); }
step "s1a477" { SELECT bcdb_tx_submit('{"hash": "29_0", "iso": "SE", "sql": "SELECT joint_pay(22, 23, 0, 0, 0);"}'); }
step "s1a478" { SELECT bcdb_tx_submit('{"hash": "29_1", "iso": "SE", "sql": "SELECT joint_pay(45, 7, 42, 0, 0);"}'); }
step "s1a479" { SELECT bcdb_tx_submit('{"hash": "29_2", "iso": "SE", "sql": "SELECT simple_pay(2, 20, 0);"}'); }
step "s1a480" { SELECT bcdb_tx_submit('{"hash": "29_3", "iso": "SE", "sql": "SELECT simple_pay(1, 20, 0);"}'); }
step "s1a481" { SELECT bcdb_tx_submit('{"hash": "29_4", "iso": "SE", "sql": "SELECT simple_pay(8, 48, 0);"}'); }
step "s1a482" { SELECT bcdb_tx_submit('{"hash": "29_5", "iso": "SE", "sql": "SELECT simple_pay(26, 42, 0);"}'); }
step "s1a483" { SELECT bcdb_tx_submit('{"hash": "29_6", "iso": "SE", "sql": "SELECT joint_pay(9, 25, 19, 0, 0);"}'); }
step "s1a484" { SELECT bcdb_tx_submit('{"hash": "29_7", "iso": "SE", "sql": "SELECT simple_pay(10, 8, 0);"}'); }
step "s1a485" { SELECT bcdb_tx_submit('{"hash": "29_8", "iso": "SE", "sql": "SELECT simple_pay(30, 45, 0);"}'); }
step "s1a486" { SELECT bcdb_tx_submit('{"hash": "29_9", "iso": "SE", "sql": "SELECT simple_pay(48, 46, 0);"}'); }
step "s1a487" { SELECT bcdb_tx_submit('{"hash": "29_10", "iso": "SE", "sql": "SELECT joint_pay(33, 2, 35, 0, 0);"}'); }
step "s1a488" { SELECT bcdb_tx_submit('{"hash": "29_11", "iso": "SE", "sql": "SELECT simple_pay(44, 40, 0);"}'); }
step "s1a489" { SELECT bcdb_tx_submit('{"hash": "29_12", "iso": "SE", "sql": "SELECT simple_pay(11, 22, 0);"}'); }
step "s1a490" { SELECT bcdb_tx_submit('{"hash": "29_13", "iso": "SE", "sql": "SELECT simple_pay(5, 35, 0);"}'); }
step "s1a491" { SELECT bcdb_tx_submit('{"hash": "29_14", "iso": "SE", "sql": "SELECT joint_pay(16, 12, 20, 0, 0);"}'); }
step "s1a492" { SELECT bcdb_tx_submit('{"hash": "29_15", "iso": "SE", "sql": "SELECT simple_pay(16, 33, 0);"}'); }
step "s1a493" { SELECT bcdb_block_submit('{"bid": 29, "txs": ["29_0", "29_1", "29_2", "29_3", "29_4", "29_5", "29_6", "29_7", "29_8", "29_9", "29_10", "29_11", "29_12", "29_13", "29_14", "29_15"]}'); }
step "s1a494" { SELECT bcdb_tx_submit('{"hash": "30_0", "iso": "SE", "sql": "SELECT simple_pay(9, 48, 0);"}'); }
step "s1a495" { SELECT bcdb_tx_submit('{"hash": "30_1", "iso": "SE", "sql": "SELECT simple_pay(35, 9, 0);"}'); }
step "s1a496" { SELECT bcdb_tx_submit('{"hash": "30_2", "iso": "SE", "sql": "SELECT joint_pay(37, 11, 41, 0, 0);"}'); }
step "s1a497" { SELECT bcdb_tx_submit('{"hash": "30_3", "iso": "SE", "sql": "SELECT simple_pay(48, 20, 0);"}'); }
step "s1a498" { SELECT bcdb_tx_submit('{"hash": "30_4", "iso": "SE", "sql": "SELECT simple_pay(4, 12, 0);"}'); }
step "s1a499" { SELECT bcdb_tx_submit('{"hash": "30_5", "iso": "SE", "sql": "SELECT simple_pay(29, 39, 0);"}'); }
step "s1a500" { SELECT bcdb_tx_submit('{"hash": "30_6", "iso": "SE", "sql": "SELECT simple_pay(29, 33, 0);"}'); }
step "s1a501" { SELECT bcdb_tx_submit('{"hash": "30_7", "iso": "SE", "sql": "SELECT joint_pay(21, 41, 8, 0, 0);"}'); }
step "s1a502" { SELECT bcdb_tx_submit('{"hash": "30_8", "iso": "SE", "sql": "SELECT simple_pay(35, 3, 0);"}'); }
step "s1a503" { SELECT bcdb_tx_submit('{"hash": "30_9", "iso": "SE", "sql": "SELECT simple_pay(33, 21, 0);"}'); }
step "s1a504" { SELECT bcdb_tx_submit('{"hash": "30_10", "iso": "SE", "sql": "SELECT joint_pay(49, 5, 6, 0, 0);"}'); }
step "s1a505" { SELECT bcdb_tx_submit('{"hash": "30_11", "iso": "SE", "sql": "SELECT simple_pay(22, 36, 0);"}'); }
step "s1a506" { SELECT bcdb_tx_submit('{"hash": "30_12", "iso": "SE", "sql": "SELECT simple_pay(24, 32, 0);"}'); }
step "s1a507" { SELECT bcdb_tx_submit('{"hash": "30_13", "iso": "SE", "sql": "SELECT simple_pay(40, 7, 0);"}'); }
step "s1a508" { SELECT bcdb_tx_submit('{"hash": "30_14", "iso": "SE", "sql": "SELECT joint_pay(1, 11, 46, 0, 0);"}'); }
step "s1a509" { SELECT bcdb_tx_submit('{"hash": "30_15", "iso": "SE", "sql": "SELECT joint_pay(21, 38, 12, 0, 0);"}'); }
step "s1a510" { SELECT bcdb_block_submit('{"bid": 30, "txs": ["30_0", "30_1", "30_2", "30_3", "30_4", "30_5", "30_6", "30_7", "30_8", "30_9", "30_10", "30_11", "30_12", "30_13", "30_14", "30_15"]}'); }
step "s1a511" { SELECT bcdb_tx_submit('{"hash": "31_0", "iso": "SE", "sql": "SELECT joint_pay(41, 3, 44, 0, 0);"}'); }
step "s1a512" { SELECT bcdb_tx_submit('{"hash": "31_1", "iso": "SE", "sql": "SELECT simple_pay(24, 3, 0);"}'); }
step "s1a513" { SELECT bcdb_tx_submit('{"hash": "31_2", "iso": "SE", "sql": "SELECT simple_pay(45, 10, 0);"}'); }
step "s1a514" { SELECT bcdb_tx_submit('{"hash": "31_3", "iso": "SE", "sql": "SELECT simple_pay(4, 26, 0);"}'); }
step "s1a515" { SELECT bcdb_tx_submit('{"hash": "31_4", "iso": "SE", "sql": "SELECT joint_pay(22, 38, 39, 0, 0);"}'); }
step "s1a516" { SELECT bcdb_tx_submit('{"hash": "31_5", "iso": "SE", "sql": "SELECT simple_pay(43, 19, 0);"}'); }
step "s1a517" { SELECT bcdb_tx_submit('{"hash": "31_6", "iso": "SE", "sql": "SELECT simple_pay(29, 26, 0);"}'); }
step "s1a518" { SELECT bcdb_tx_submit('{"hash": "31_7", "iso": "SE", "sql": "SELECT joint_pay(29, 16, 12, 0, 0);"}'); }
step "s1a519" { SELECT bcdb_tx_submit('{"hash": "31_8", "iso": "SE", "sql": "SELECT simple_pay(4, 22, 0);"}'); }
step "s1a520" { SELECT bcdb_tx_submit('{"hash": "31_9", "iso": "SE", "sql": "SELECT joint_pay(1, 22, 11, 0, 0);"}'); }
step "s1a521" { SELECT bcdb_tx_submit('{"hash": "31_10", "iso": "SE", "sql": "SELECT simple_pay(44, 41, 0);"}'); }
step "s1a522" { SELECT bcdb_tx_submit('{"hash": "31_11", "iso": "SE", "sql": "SELECT simple_pay(20, 29, 0);"}'); }
step "s1a523" { SELECT bcdb_tx_submit('{"hash": "31_12", "iso": "SE", "sql": "SELECT simple_pay(47, 44, 0);"}'); }
step "s1a524" { SELECT bcdb_tx_submit('{"hash": "31_13", "iso": "SE", "sql": "SELECT simple_pay(5, 3, 0);"}'); }
step "s1a525" { SELECT bcdb_tx_submit('{"hash": "31_14", "iso": "SE", "sql": "SELECT simple_pay(25, 16, 0);"}'); }
step "s1a526" { SELECT bcdb_tx_submit('{"hash": "31_15", "iso": "SE", "sql": "SELECT joint_pay(33, 6, 5, 0, 0);"}'); }
step "s1a527" { SELECT bcdb_block_submit('{"bid": 31, "txs": ["31_0", "31_1", "31_2", "31_3", "31_4", "31_5", "31_6", "31_7", "31_8", "31_9", "31_10", "31_11", "31_12", "31_13", "31_14", "31_15"]}'); }
step "s1a528" { SELECT bcdb_tx_submit('{"hash": "32_0", "iso": "SE", "sql": "SELECT simple_pay(6, 30, 0);"}'); }
step "s1a529" { SELECT bcdb_tx_submit('{"hash": "32_1", "iso": "SE", "sql": "SELECT simple_pay(9, 33, 0);"}'); }
step "s1a530" { SELECT bcdb_tx_submit('{"hash": "32_2", "iso": "SE", "sql": "SELECT simple_pay(18, 2, 0);"}'); }
step "s1a531" { SELECT bcdb_tx_submit('{"hash": "32_3", "iso": "SE", "sql": "SELECT joint_pay(21, 10, 35, 0, 0);"}'); }
step "s1a532" { SELECT bcdb_tx_submit('{"hash": "32_4", "iso": "SE", "sql": "SELECT simple_pay(10, 11, 0);"}'); }
step "s1a533" { SELECT bcdb_tx_submit('{"hash": "32_5", "iso": "SE", "sql": "SELECT simple_pay(10, 40, 0);"}'); }
step "s1a534" { SELECT bcdb_tx_submit('{"hash": "32_6", "iso": "SE", "sql": "SELECT simple_pay(39, 21, 0);"}'); }
step "s1a535" { SELECT bcdb_tx_submit('{"hash": "32_7", "iso": "SE", "sql": "SELECT simple_pay(30, 40, 0);"}'); }
step "s1a536" { SELECT bcdb_tx_submit('{"hash": "32_8", "iso": "SE", "sql": "SELECT simple_pay(2, 14, 0);"}'); }
step "s1a537" { SELECT bcdb_tx_submit('{"hash": "32_9", "iso": "SE", "sql": "SELECT simple_pay(18, 21, 0);"}'); }
step "s1a538" { SELECT bcdb_tx_submit('{"hash": "32_10", "iso": "SE", "sql": "SELECT joint_pay(15, 22, 14, 0, 0);"}'); }
step "s1a539" { SELECT bcdb_tx_submit('{"hash": "32_11", "iso": "SE", "sql": "SELECT joint_pay(26, 29, 23, 0, 0);"}'); }
step "s1a540" { SELECT bcdb_tx_submit('{"hash": "32_12", "iso": "SE", "sql": "SELECT simple_pay(8, 24, 0);"}'); }
step "s1a541" { SELECT bcdb_tx_submit('{"hash": "32_13", "iso": "SE", "sql": "SELECT simple_pay(0, 10, 0);"}'); }
step "s1a542" { SELECT bcdb_tx_submit('{"hash": "32_14", "iso": "SE", "sql": "SELECT simple_pay(0, 43, 0);"}'); }
step "s1a543" { SELECT bcdb_tx_submit('{"hash": "32_15", "iso": "SE", "sql": "SELECT simple_pay(11, 9, 0);"}'); }
step "s1a544" { SELECT bcdb_block_submit('{"bid": 32, "txs": ["32_0", "32_1", "32_2", "32_3", "32_4", "32_5", "32_6", "32_7", "32_8", "32_9", "32_10", "32_11", "32_12", "32_13", "32_14", "32_15"]}'); }
step "s1a545" { SELECT bcdb_tx_submit('{"hash": "33_0", "iso": "SE", "sql": "SELECT joint_pay(20, 32, 0, 0, 0);"}'); }
step "s1a546" { SELECT bcdb_tx_submit('{"hash": "33_1", "iso": "SE", "sql": "SELECT joint_pay(49, 7, 36, 0, 0);"}'); }
step "s1a547" { SELECT bcdb_tx_submit('{"hash": "33_2", "iso": "SE", "sql": "SELECT simple_pay(49, 9, 0);"}'); }
step "s1a548" { SELECT bcdb_tx_submit('{"hash": "33_3", "iso": "SE", "sql": "SELECT simple_pay(24, 1, 0);"}'); }
step "s1a549" { SELECT bcdb_tx_submit('{"hash": "33_4", "iso": "SE", "sql": "SELECT simple_pay(36, 43, 0);"}'); }
step "s1a550" { SELECT bcdb_tx_submit('{"hash": "33_5", "iso": "SE", "sql": "SELECT simple_pay(15, 8, 0);"}'); }
step "s1a551" { SELECT bcdb_tx_submit('{"hash": "33_6", "iso": "SE", "sql": "SELECT simple_pay(13, 34, 0);"}'); }
step "s1a552" { SELECT bcdb_tx_submit('{"hash": "33_7", "iso": "SE", "sql": "SELECT simple_pay(8, 26, 0);"}'); }
step "s1a553" { SELECT bcdb_tx_submit('{"hash": "33_8", "iso": "SE", "sql": "SELECT simple_pay(22, 6, 0);"}'); }
step "s1a554" { SELECT bcdb_tx_submit('{"hash": "33_9", "iso": "SE", "sql": "SELECT simple_pay(27, 15, 0);"}'); }
step "s1a555" { SELECT bcdb_tx_submit('{"hash": "33_10", "iso": "SE", "sql": "SELECT simple_pay(14, 25, 0);"}'); }
step "s1a556" { SELECT bcdb_tx_submit('{"hash": "33_11", "iso": "SE", "sql": "SELECT simple_pay(30, 25, 0);"}'); }
step "s1a557" { SELECT bcdb_tx_submit('{"hash": "33_12", "iso": "SE", "sql": "SELECT simple_pay(4, 16, 0);"}'); }
step "s1a558" { SELECT bcdb_tx_submit('{"hash": "33_13", "iso": "SE", "sql": "SELECT simple_pay(33, 23, 0);"}'); }
step "s1a559" { SELECT bcdb_tx_submit('{"hash": "33_14", "iso": "SE", "sql": "SELECT simple_pay(38, 39, 0);"}'); }
step "s1a560" { SELECT bcdb_tx_submit('{"hash": "33_15", "iso": "SE", "sql": "SELECT simple_pay(15, 17, 0);"}'); }
step "s1a561" { SELECT bcdb_block_submit('{"bid": 33, "txs": ["33_0", "33_1", "33_2", "33_3", "33_4", "33_5", "33_6", "33_7", "33_8", "33_9", "33_10", "33_11", "33_12", "33_13", "33_14", "33_15"]}'); }
step "s1a562" { SELECT bcdb_tx_submit('{"hash": "34_0", "iso": "SE", "sql": "SELECT joint_pay(20, 25, 40, 0, 0);"}'); }
step "s1a563" { SELECT bcdb_tx_submit('{"hash": "34_1", "iso": "SE", "sql": "SELECT joint_pay(3, 9, 45, 0, 0);"}'); }
step "s1a564" { SELECT bcdb_tx_submit('{"hash": "34_2", "iso": "SE", "sql": "SELECT simple_pay(49, 26, 0);"}'); }
step "s1a565" { SELECT bcdb_tx_submit('{"hash": "34_3", "iso": "SE", "sql": "SELECT simple_pay(25, 27, 0);"}'); }
step "s1a566" { SELECT bcdb_tx_submit('{"hash": "34_4", "iso": "SE", "sql": "SELECT simple_pay(45, 29, 0);"}'); }
step "s1a567" { SELECT bcdb_tx_submit('{"hash": "34_5", "iso": "SE", "sql": "SELECT simple_pay(10, 21, 0);"}'); }
step "s1a568" { SELECT bcdb_tx_submit('{"hash": "34_6", "iso": "SE", "sql": "SELECT simple_pay(10, 37, 0);"}'); }
step "s1a569" { SELECT bcdb_tx_submit('{"hash": "34_7", "iso": "SE", "sql": "SELECT simple_pay(18, 48, 0);"}'); }
step "s1a570" { SELECT bcdb_tx_submit('{"hash": "34_8", "iso": "SE", "sql": "SELECT simple_pay(23, 22, 0);"}'); }
step "s1a571" { SELECT bcdb_tx_submit('{"hash": "34_9", "iso": "SE", "sql": "SELECT joint_pay(22, 49, 30, 0, 0);"}'); }
step "s1a572" { SELECT bcdb_tx_submit('{"hash": "34_10", "iso": "SE", "sql": "SELECT simple_pay(48, 3, 0);"}'); }
step "s1a573" { SELECT bcdb_tx_submit('{"hash": "34_11", "iso": "SE", "sql": "SELECT joint_pay(16, 11, 46, 0, 0);"}'); }
step "s1a574" { SELECT bcdb_tx_submit('{"hash": "34_12", "iso": "SE", "sql": "SELECT simple_pay(18, 24, 0);"}'); }
step "s1a575" { SELECT bcdb_tx_submit('{"hash": "34_13", "iso": "SE", "sql": "SELECT simple_pay(18, 35, 0);"}'); }
step "s1a576" { SELECT bcdb_tx_submit('{"hash": "34_14", "iso": "SE", "sql": "SELECT simple_pay(43, 26, 0);"}'); }
step "s1a577" { SELECT bcdb_tx_submit('{"hash": "34_15", "iso": "SE", "sql": "SELECT simple_pay(46, 13, 0);"}'); }
step "s1a578" { SELECT bcdb_block_submit('{"bid": 34, "txs": ["34_0", "34_1", "34_2", "34_3", "34_4", "34_5", "34_6", "34_7", "34_8", "34_9", "34_10", "34_11", "34_12", "34_13", "34_14", "34_15"]}'); }
step "s1a579" { SELECT bcdb_tx_submit('{"hash": "35_0", "iso": "SE", "sql": "SELECT simple_pay(8, 7, 0);"}'); }
step "s1a580" { SELECT bcdb_tx_submit('{"hash": "35_1", "iso": "SE", "sql": "SELECT simple_pay(10, 1, 0);"}'); }
step "s1a581" { SELECT bcdb_tx_submit('{"hash": "35_2", "iso": "SE", "sql": "SELECT simple_pay(25, 29, 0);"}'); }
step "s1a582" { SELECT bcdb_tx_submit('{"hash": "35_3", "iso": "SE", "sql": "SELECT joint_pay(45, 43, 4, 0, 0);"}'); }
step "s1a583" { SELECT bcdb_tx_submit('{"hash": "35_4", "iso": "SE", "sql": "SELECT simple_pay(34, 46, 0);"}'); }
step "s1a584" { SELECT bcdb_tx_submit('{"hash": "35_5", "iso": "SE", "sql": "SELECT simple_pay(10, 9, 0);"}'); }
step "s1a585" { SELECT bcdb_tx_submit('{"hash": "35_6", "iso": "SE", "sql": "SELECT simple_pay(14, 1, 0);"}'); }
step "s1a586" { SELECT bcdb_tx_submit('{"hash": "35_7", "iso": "SE", "sql": "SELECT simple_pay(31, 22, 0);"}'); }
step "s1a587" { SELECT bcdb_tx_submit('{"hash": "35_8", "iso": "SE", "sql": "SELECT simple_pay(39, 47, 0);"}'); }
step "s1a588" { SELECT bcdb_tx_submit('{"hash": "35_9", "iso": "SE", "sql": "SELECT simple_pay(21, 43, 0);"}'); }
step "s1a589" { SELECT bcdb_tx_submit('{"hash": "35_10", "iso": "SE", "sql": "SELECT joint_pay(26, 49, 16, 0, 0);"}'); }
step "s1a590" { SELECT bcdb_tx_submit('{"hash": "35_11", "iso": "SE", "sql": "SELECT simple_pay(21, 40, 0);"}'); }
step "s1a591" { SELECT bcdb_tx_submit('{"hash": "35_12", "iso": "SE", "sql": "SELECT simple_pay(21, 34, 0);"}'); }
step "s1a592" { SELECT bcdb_tx_submit('{"hash": "35_13", "iso": "SE", "sql": "SELECT simple_pay(24, 47, 0);"}'); }
step "s1a593" { SELECT bcdb_tx_submit('{"hash": "35_14", "iso": "SE", "sql": "SELECT simple_pay(19, 15, 0);"}'); }
step "s1a594" { SELECT bcdb_tx_submit('{"hash": "35_15", "iso": "SE", "sql": "SELECT simple_pay(24, 22, 0);"}'); }
step "s1a595" { SELECT bcdb_block_submit('{"bid": 35, "txs": ["35_0", "35_1", "35_2", "35_3", "35_4", "35_5", "35_6", "35_7", "35_8", "35_9", "35_10", "35_11", "35_12", "35_13", "35_14", "35_15"]}'); }
step "s1a596" { SELECT bcdb_tx_submit('{"hash": "36_0", "iso": "SE", "sql": "SELECT simple_pay(30, 32, 0);"}'); }
step "s1a597" { SELECT bcdb_tx_submit('{"hash": "36_1", "iso": "SE", "sql": "SELECT simple_pay(26, 6, 0);"}'); }
step "s1a598" { SELECT bcdb_tx_submit('{"hash": "36_2", "iso": "SE", "sql": "SELECT simple_pay(9, 0, 0);"}'); }
step "s1a599" { SELECT bcdb_tx_submit('{"hash": "36_3", "iso": "SE", "sql": "SELECT simple_pay(40, 45, 0);"}'); }
step "s1a600" { SELECT bcdb_tx_submit('{"hash": "36_4", "iso": "SE", "sql": "SELECT simple_pay(33, 6, 0);"}'); }
step "s1a601" { SELECT bcdb_tx_submit('{"hash": "36_5", "iso": "SE", "sql": "SELECT simple_pay(41, 44, 0);"}'); }
step "s1a602" { SELECT bcdb_tx_submit('{"hash": "36_6", "iso": "SE", "sql": "SELECT simple_pay(41, 38, 0);"}'); }
step "s1a603" { SELECT bcdb_tx_submit('{"hash": "36_7", "iso": "SE", "sql": "SELECT simple_pay(7, 17, 0);"}'); }
step "s1a604" { SELECT bcdb_tx_submit('{"hash": "36_8", "iso": "SE", "sql": "SELECT simple_pay(39, 10, 0);"}'); }
step "s1a605" { SELECT bcdb_tx_submit('{"hash": "36_9", "iso": "SE", "sql": "SELECT simple_pay(2, 0, 0);"}'); }
step "s1a606" { SELECT bcdb_tx_submit('{"hash": "36_10", "iso": "SE", "sql": "SELECT joint_pay(23, 46, 30, 0, 0);"}'); }
step "s1a607" { SELECT bcdb_tx_submit('{"hash": "36_11", "iso": "SE", "sql": "SELECT simple_pay(43, 28, 0);"}'); }
step "s1a608" { SELECT bcdb_tx_submit('{"hash": "36_12", "iso": "SE", "sql": "SELECT simple_pay(44, 16, 0);"}'); }
step "s1a609" { SELECT bcdb_tx_submit('{"hash": "36_13", "iso": "SE", "sql": "SELECT simple_pay(49, 14, 0);"}'); }
step "s1a610" { SELECT bcdb_tx_submit('{"hash": "36_14", "iso": "SE", "sql": "SELECT simple_pay(35, 4, 0);"}'); }
step "s1a611" { SELECT bcdb_tx_submit('{"hash": "36_15", "iso": "SE", "sql": "SELECT simple_pay(32, 10, 0);"}'); }
step "s1a612" { SELECT bcdb_block_submit('{"bid": 36, "txs": ["36_0", "36_1", "36_2", "36_3", "36_4", "36_5", "36_6", "36_7", "36_8", "36_9", "36_10", "36_11", "36_12", "36_13", "36_14", "36_15"]}'); }
step "s1a613" { SELECT bcdb_tx_submit('{"hash": "37_0", "iso": "SE", "sql": "SELECT joint_pay(41, 10, 33, 0, 0);"}'); }
step "s1a614" { SELECT bcdb_tx_submit('{"hash": "37_1", "iso": "SE", "sql": "SELECT simple_pay(42, 13, 0);"}'); }
step "s1a615" { SELECT bcdb_tx_submit('{"hash": "37_2", "iso": "SE", "sql": "SELECT simple_pay(43, 25, 0);"}'); }
step "s1a616" { SELECT bcdb_tx_submit('{"hash": "37_3", "iso": "SE", "sql": "SELECT simple_pay(37, 8, 0);"}'); }
step "s1a617" { SELECT bcdb_tx_submit('{"hash": "37_4", "iso": "SE", "sql": "SELECT simple_pay(10, 28, 0);"}'); }
step "s1a618" { SELECT bcdb_tx_submit('{"hash": "37_5", "iso": "SE", "sql": "SELECT simple_pay(24, 5, 0);"}'); }
step "s1a619" { SELECT bcdb_tx_submit('{"hash": "37_6", "iso": "SE", "sql": "SELECT simple_pay(25, 21, 0);"}'); }
step "s1a620" { SELECT bcdb_tx_submit('{"hash": "37_7", "iso": "SE", "sql": "SELECT simple_pay(29, 2, 0);"}'); }
step "s1a621" { SELECT bcdb_tx_submit('{"hash": "37_8", "iso": "SE", "sql": "SELECT simple_pay(6, 17, 0);"}'); }
step "s1a622" { SELECT bcdb_tx_submit('{"hash": "37_9", "iso": "SE", "sql": "SELECT simple_pay(31, 35, 0);"}'); }
step "s1a623" { SELECT bcdb_tx_submit('{"hash": "37_10", "iso": "SE", "sql": "SELECT simple_pay(30, 16, 0);"}'); }
step "s1a624" { SELECT bcdb_tx_submit('{"hash": "37_11", "iso": "SE", "sql": "SELECT joint_pay(34, 23, 10, 0, 0);"}'); }
step "s1a625" { SELECT bcdb_tx_submit('{"hash": "37_12", "iso": "SE", "sql": "SELECT simple_pay(38, 9, 0);"}'); }
step "s1a626" { SELECT bcdb_tx_submit('{"hash": "37_13", "iso": "SE", "sql": "SELECT simple_pay(4, 30, 0);"}'); }
step "s1a627" { SELECT bcdb_tx_submit('{"hash": "37_14", "iso": "SE", "sql": "SELECT simple_pay(26, 35, 0);"}'); }
step "s1a628" { SELECT bcdb_tx_submit('{"hash": "37_15", "iso": "SE", "sql": "SELECT joint_pay(30, 14, 7, 0, 0);"}'); }
step "s1a629" { SELECT bcdb_block_submit('{"bid": 37, "txs": ["37_0", "37_1", "37_2", "37_3", "37_4", "37_5", "37_6", "37_7", "37_8", "37_9", "37_10", "37_11", "37_12", "37_13", "37_14", "37_15"]}'); }
step "s1a630" { SELECT bcdb_tx_submit('{"hash": "38_0", "iso": "SE", "sql": "SELECT simple_pay(23, 6, 0);"}'); }
step "s1a631" { SELECT bcdb_tx_submit('{"hash": "38_1", "iso": "SE", "sql": "SELECT joint_pay(3, 42, 8, 0, 0);"}'); }
step "s1a632" { SELECT bcdb_tx_submit('{"hash": "38_2", "iso": "SE", "sql": "SELECT simple_pay(12, 0, 0);"}'); }
step "s1a633" { SELECT bcdb_tx_submit('{"hash": "38_3", "iso": "SE", "sql": "SELECT joint_pay(25, 35, 44, 0, 0);"}'); }
step "s1a634" { SELECT bcdb_tx_submit('{"hash": "38_4", "iso": "SE", "sql": "SELECT simple_pay(31, 45, 0);"}'); }
step "s1a635" { SELECT bcdb_tx_submit('{"hash": "38_5", "iso": "SE", "sql": "SELECT simple_pay(30, 35, 0);"}'); }
step "s1a636" { SELECT bcdb_tx_submit('{"hash": "38_6", "iso": "SE", "sql": "SELECT simple_pay(49, 21, 0);"}'); }
step "s1a637" { SELECT bcdb_tx_submit('{"hash": "38_7", "iso": "SE", "sql": "SELECT simple_pay(43, 0, 0);"}'); }
step "s1a638" { SELECT bcdb_tx_submit('{"hash": "38_8", "iso": "SE", "sql": "SELECT simple_pay(31, 19, 0);"}'); }
step "s1a639" { SELECT bcdb_tx_submit('{"hash": "38_9", "iso": "SE", "sql": "SELECT simple_pay(0, 31, 0);"}'); }
step "s1a640" { SELECT bcdb_tx_submit('{"hash": "38_10", "iso": "SE", "sql": "SELECT simple_pay(32, 21, 0);"}'); }
step "s1a641" { SELECT bcdb_tx_submit('{"hash": "38_11", "iso": "SE", "sql": "SELECT joint_pay(19, 36, 27, 0, 0);"}'); }
step "s1a642" { SELECT bcdb_tx_submit('{"hash": "38_12", "iso": "SE", "sql": "SELECT simple_pay(23, 24, 0);"}'); }
step "s1a643" { SELECT bcdb_tx_submit('{"hash": "38_13", "iso": "SE", "sql": "SELECT simple_pay(9, 14, 0);"}'); }
step "s1a644" { SELECT bcdb_tx_submit('{"hash": "38_14", "iso": "SE", "sql": "SELECT simple_pay(12, 47, 0);"}'); }
step "s1a645" { SELECT bcdb_tx_submit('{"hash": "38_15", "iso": "SE", "sql": "SELECT simple_pay(42, 22, 0);"}'); }
step "s1a646" { SELECT bcdb_block_submit('{"bid": 38, "txs": ["38_0", "38_1", "38_2", "38_3", "38_4", "38_5", "38_6", "38_7", "38_8", "38_9", "38_10", "38_11", "38_12", "38_13", "38_14", "38_15"]}'); }
step "s1a647" { SELECT bcdb_tx_submit('{"hash": "39_0", "iso": "SE", "sql": "SELECT simple_pay(39, 8, 0);"}'); }
step "s1a648" { SELECT bcdb_tx_submit('{"hash": "39_1", "iso": "SE", "sql": "SELECT simple_pay(7, 25, 0);"}'); }
step "s1a649" { SELECT bcdb_tx_submit('{"hash": "39_2", "iso": "SE", "sql": "SELECT simple_pay(30, 14, 0);"}'); }
step "s1a650" { SELECT bcdb_tx_submit('{"hash": "39_3", "iso": "SE", "sql": "SELECT simple_pay(23, 40, 0);"}'); }
step "s1a651" { SELECT bcdb_tx_submit('{"hash": "39_4", "iso": "SE", "sql": "SELECT simple_pay(27, 17, 0);"}'); }
step "s1a652" { SELECT bcdb_tx_submit('{"hash": "39_5", "iso": "SE", "sql": "SELECT simple_pay(25, 49, 0);"}'); }
step "s1a653" { SELECT bcdb_tx_submit('{"hash": "39_6", "iso": "SE", "sql": "SELECT simple_pay(18, 6, 0);"}'); }
step "s1a654" { SELECT bcdb_tx_submit('{"hash": "39_7", "iso": "SE", "sql": "SELECT simple_pay(18, 7, 0);"}'); }
step "s1a655" { SELECT bcdb_tx_submit('{"hash": "39_8", "iso": "SE", "sql": "SELECT simple_pay(22, 15, 0);"}'); }
step "s1a656" { SELECT bcdb_tx_submit('{"hash": "39_9", "iso": "SE", "sql": "SELECT simple_pay(21, 31, 0);"}'); }
step "s1a657" { SELECT bcdb_tx_submit('{"hash": "39_10", "iso": "SE", "sql": "SELECT simple_pay(43, 24, 0);"}'); }
step "s1a658" { SELECT bcdb_tx_submit('{"hash": "39_11", "iso": "SE", "sql": "SELECT simple_pay(29, 32, 0);"}'); }
step "s1a659" { SELECT bcdb_tx_submit('{"hash": "39_12", "iso": "SE", "sql": "SELECT simple_pay(36, 39, 0);"}'); }
step "s1a660" { SELECT bcdb_tx_submit('{"hash": "39_13", "iso": "SE", "sql": "SELECT simple_pay(25, 32, 0);"}'); }
step "s1a661" { SELECT bcdb_tx_submit('{"hash": "39_14", "iso": "SE", "sql": "SELECT simple_pay(14, 20, 0);"}'); }
step "s1a662" { SELECT bcdb_tx_submit('{"hash": "39_15", "iso": "SE", "sql": "SELECT simple_pay(0, 5, 0);"}'); }
step "s1a663" { SELECT bcdb_block_submit('{"bid": 39, "txs": ["39_0", "39_1", "39_2", "39_3", "39_4", "39_5", "39_6", "39_7", "39_8", "39_9", "39_10", "39_11", "39_12", "39_13", "39_14", "39_15"]}'); }
step "s1a664" { SELECT bcdb_tx_submit('{"hash": "40_0", "iso": "SE", "sql": "SELECT simple_pay(25, 14, 0);"}'); }
step "s1a665" { SELECT bcdb_tx_submit('{"hash": "40_1", "iso": "SE", "sql": "SELECT simple_pay(27, 3, 0);"}'); }
step "s1a666" { SELECT bcdb_tx_submit('{"hash": "40_2", "iso": "SE", "sql": "SELECT simple_pay(2, 26, 0);"}'); }
step "s1a667" { SELECT bcdb_tx_submit('{"hash": "40_3", "iso": "SE", "sql": "SELECT joint_pay(12, 46, 20, 0, 0);"}'); }
step "s1a668" { SELECT bcdb_tx_submit('{"hash": "40_4", "iso": "SE", "sql": "SELECT joint_pay(11, 44, 23, 0, 0);"}'); }
step "s1a669" { SELECT bcdb_tx_submit('{"hash": "40_5", "iso": "SE", "sql": "SELECT joint_pay(2, 0, 24, 0, 0);"}'); }
step "s1a670" { SELECT bcdb_tx_submit('{"hash": "40_6", "iso": "SE", "sql": "SELECT simple_pay(8, 7, 0);"}'); }
step "s1a671" { SELECT bcdb_tx_submit('{"hash": "40_7", "iso": "SE", "sql": "SELECT simple_pay(38, 12, 0);"}'); }
step "s1a672" { SELECT bcdb_tx_submit('{"hash": "40_8", "iso": "SE", "sql": "SELECT joint_pay(29, 12, 0, 0, 0);"}'); }
step "s1a673" { SELECT bcdb_tx_submit('{"hash": "40_9", "iso": "SE", "sql": "SELECT simple_pay(39, 26, 0);"}'); }
step "s1a674" { SELECT bcdb_tx_submit('{"hash": "40_10", "iso": "SE", "sql": "SELECT joint_pay(11, 14, 26, 0, 0);"}'); }
step "s1a675" { SELECT bcdb_tx_submit('{"hash": "40_11", "iso": "SE", "sql": "SELECT simple_pay(0, 27, 0);"}'); }
step "s1a676" { SELECT bcdb_tx_submit('{"hash": "40_12", "iso": "SE", "sql": "SELECT simple_pay(48, 2, 0);"}'); }
step "s1a677" { SELECT bcdb_tx_submit('{"hash": "40_13", "iso": "SE", "sql": "SELECT simple_pay(17, 1, 0);"}'); }
step "s1a678" { SELECT bcdb_tx_submit('{"hash": "40_14", "iso": "SE", "sql": "SELECT simple_pay(45, 23, 0);"}'); }
step "s1a679" { SELECT bcdb_tx_submit('{"hash": "40_15", "iso": "SE", "sql": "SELECT simple_pay(43, 29, 0);"}'); }
step "s1a680" { SELECT bcdb_block_submit('{"bid": 40, "txs": ["40_0", "40_1", "40_2", "40_3", "40_4", "40_5", "40_6", "40_7", "40_8", "40_9", "40_10", "40_11", "40_12", "40_13", "40_14", "40_15"]}'); }
step "s1a681" { SELECT bcdb_tx_submit('{"hash": "41_0", "iso": "SE", "sql": "SELECT simple_pay(38, 33, 0);"}'); }
step "s1a682" { SELECT bcdb_tx_submit('{"hash": "41_1", "iso": "SE", "sql": "SELECT joint_pay(6, 45, 17, 0, 0);"}'); }
step "s1a683" { SELECT bcdb_tx_submit('{"hash": "41_2", "iso": "SE", "sql": "SELECT joint_pay(9, 39, 49, 0, 0);"}'); }
step "s1a684" { SELECT bcdb_tx_submit('{"hash": "41_3", "iso": "SE", "sql": "SELECT simple_pay(24, 13, 0);"}'); }
step "s1a685" { SELECT bcdb_tx_submit('{"hash": "41_4", "iso": "SE", "sql": "SELECT simple_pay(42, 20, 0);"}'); }
step "s1a686" { SELECT bcdb_tx_submit('{"hash": "41_5", "iso": "SE", "sql": "SELECT simple_pay(32, 7, 0);"}'); }
step "s1a687" { SELECT bcdb_tx_submit('{"hash": "41_6", "iso": "SE", "sql": "SELECT simple_pay(44, 30, 0);"}'); }
step "s1a688" { SELECT bcdb_tx_submit('{"hash": "41_7", "iso": "SE", "sql": "SELECT joint_pay(28, 30, 11, 0, 0);"}'); }
step "s1a689" { SELECT bcdb_tx_submit('{"hash": "41_8", "iso": "SE", "sql": "SELECT simple_pay(21, 8, 0);"}'); }
step "s1a690" { SELECT bcdb_tx_submit('{"hash": "41_9", "iso": "SE", "sql": "SELECT simple_pay(24, 5, 0);"}'); }
step "s1a691" { SELECT bcdb_tx_submit('{"hash": "41_10", "iso": "SE", "sql": "SELECT simple_pay(21, 14, 0);"}'); }
step "s1a692" { SELECT bcdb_tx_submit('{"hash": "41_11", "iso": "SE", "sql": "SELECT simple_pay(22, 30, 0);"}'); }
step "s1a693" { SELECT bcdb_tx_submit('{"hash": "41_12", "iso": "SE", "sql": "SELECT simple_pay(26, 1, 0);"}'); }
step "s1a694" { SELECT bcdb_tx_submit('{"hash": "41_13", "iso": "SE", "sql": "SELECT simple_pay(0, 35, 0);"}'); }
step "s1a695" { SELECT bcdb_tx_submit('{"hash": "41_14", "iso": "SE", "sql": "SELECT simple_pay(48, 49, 0);"}'); }
step "s1a696" { SELECT bcdb_tx_submit('{"hash": "41_15", "iso": "SE", "sql": "SELECT simple_pay(27, 15, 0);"}'); }
step "s1a697" { SELECT bcdb_block_submit('{"bid": 41, "txs": ["41_0", "41_1", "41_2", "41_3", "41_4", "41_5", "41_6", "41_7", "41_8", "41_9", "41_10", "41_11", "41_12", "41_13", "41_14", "41_15"]}'); }
step "s1a698" { SELECT bcdb_tx_submit('{"hash": "42_0", "iso": "SE", "sql": "SELECT simple_pay(30, 9, 0);"}'); }
step "s1a699" { SELECT bcdb_tx_submit('{"hash": "42_1", "iso": "SE", "sql": "SELECT simple_pay(18, 23, 0);"}'); }
step "s1a700" { SELECT bcdb_tx_submit('{"hash": "42_2", "iso": "SE", "sql": "SELECT simple_pay(38, 9, 0);"}'); }
step "s1a701" { SELECT bcdb_tx_submit('{"hash": "42_3", "iso": "SE", "sql": "SELECT simple_pay(33, 43, 0);"}'); }
step "s1a702" { SELECT bcdb_tx_submit('{"hash": "42_4", "iso": "SE", "sql": "SELECT joint_pay(19, 33, 40, 0, 0);"}'); }
step "s1a703" { SELECT bcdb_tx_submit('{"hash": "42_5", "iso": "SE", "sql": "SELECT simple_pay(3, 9, 0);"}'); }
step "s1a704" { SELECT bcdb_tx_submit('{"hash": "42_6", "iso": "SE", "sql": "SELECT simple_pay(21, 39, 0);"}'); }
step "s1a705" { SELECT bcdb_tx_submit('{"hash": "42_7", "iso": "SE", "sql": "SELECT simple_pay(49, 29, 0);"}'); }
step "s1a706" { SELECT bcdb_tx_submit('{"hash": "42_8", "iso": "SE", "sql": "SELECT simple_pay(12, 26, 0);"}'); }
step "s1a707" { SELECT bcdb_tx_submit('{"hash": "42_9", "iso": "SE", "sql": "SELECT simple_pay(10, 25, 0);"}'); }
step "s1a708" { SELECT bcdb_tx_submit('{"hash": "42_10", "iso": "SE", "sql": "SELECT joint_pay(49, 21, 48, 0, 0);"}'); }
step "s1a709" { SELECT bcdb_tx_submit('{"hash": "42_11", "iso": "SE", "sql": "SELECT simple_pay(33, 12, 0);"}'); }
step "s1a710" { SELECT bcdb_tx_submit('{"hash": "42_12", "iso": "SE", "sql": "SELECT simple_pay(11, 33, 0);"}'); }
step "s1a711" { SELECT bcdb_tx_submit('{"hash": "42_13", "iso": "SE", "sql": "SELECT simple_pay(45, 38, 0);"}'); }
step "s1a712" { SELECT bcdb_tx_submit('{"hash": "42_14", "iso": "SE", "sql": "SELECT simple_pay(9, 40, 0);"}'); }
step "s1a713" { SELECT bcdb_tx_submit('{"hash": "42_15", "iso": "SE", "sql": "SELECT simple_pay(31, 42, 0);"}'); }
step "s1a714" { SELECT bcdb_block_submit('{"bid": 42, "txs": ["42_0", "42_1", "42_2", "42_3", "42_4", "42_5", "42_6", "42_7", "42_8", "42_9", "42_10", "42_11", "42_12", "42_13", "42_14", "42_15"]}'); }
step "s1a715" { SELECT bcdb_tx_submit('{"hash": "43_0", "iso": "SE", "sql": "SELECT simple_pay(13, 38, 0);"}'); }
step "s1a716" { SELECT bcdb_tx_submit('{"hash": "43_1", "iso": "SE", "sql": "SELECT simple_pay(15, 31, 0);"}'); }
step "s1a717" { SELECT bcdb_tx_submit('{"hash": "43_2", "iso": "SE", "sql": "SELECT simple_pay(20, 35, 0);"}'); }
step "s1a718" { SELECT bcdb_tx_submit('{"hash": "43_3", "iso": "SE", "sql": "SELECT simple_pay(0, 2, 0);"}'); }
step "s1a719" { SELECT bcdb_tx_submit('{"hash": "43_4", "iso": "SE", "sql": "SELECT joint_pay(15, 28, 43, 0, 0);"}'); }
step "s1a720" { SELECT bcdb_tx_submit('{"hash": "43_5", "iso": "SE", "sql": "SELECT simple_pay(42, 43, 0);"}'); }
step "s1a721" { SELECT bcdb_tx_submit('{"hash": "43_6", "iso": "SE", "sql": "SELECT joint_pay(48, 33, 27, 0, 0);"}'); }
step "s1a722" { SELECT bcdb_tx_submit('{"hash": "43_7", "iso": "SE", "sql": "SELECT simple_pay(40, 18, 0);"}'); }
step "s1a723" { SELECT bcdb_tx_submit('{"hash": "43_8", "iso": "SE", "sql": "SELECT simple_pay(21, 31, 0);"}'); }
step "s1a724" { SELECT bcdb_tx_submit('{"hash": "43_9", "iso": "SE", "sql": "SELECT simple_pay(10, 23, 0);"}'); }
step "s1a725" { SELECT bcdb_tx_submit('{"hash": "43_10", "iso": "SE", "sql": "SELECT simple_pay(22, 45, 0);"}'); }
step "s1a726" { SELECT bcdb_tx_submit('{"hash": "43_11", "iso": "SE", "sql": "SELECT simple_pay(28, 42, 0);"}'); }
step "s1a727" { SELECT bcdb_tx_submit('{"hash": "43_12", "iso": "SE", "sql": "SELECT simple_pay(29, 4, 0);"}'); }
step "s1a728" { SELECT bcdb_tx_submit('{"hash": "43_13", "iso": "SE", "sql": "SELECT joint_pay(48, 7, 9, 0, 0);"}'); }
step "s1a729" { SELECT bcdb_tx_submit('{"hash": "43_14", "iso": "SE", "sql": "SELECT simple_pay(25, 29, 0);"}'); }
step "s1a730" { SELECT bcdb_tx_submit('{"hash": "43_15", "iso": "SE", "sql": "SELECT simple_pay(13, 23, 0);"}'); }
step "s1a731" { SELECT bcdb_block_submit('{"bid": 43, "txs": ["43_0", "43_1", "43_2", "43_3", "43_4", "43_5", "43_6", "43_7", "43_8", "43_9", "43_10", "43_11", "43_12", "43_13", "43_14", "43_15"]}'); }
step "s1a732" { SELECT bcdb_tx_submit('{"hash": "44_0", "iso": "SE", "sql": "SELECT simple_pay(1, 25, 0);"}'); }
step "s1a733" { SELECT bcdb_tx_submit('{"hash": "44_1", "iso": "SE", "sql": "SELECT simple_pay(26, 37, 0);"}'); }
step "s1a734" { SELECT bcdb_tx_submit('{"hash": "44_2", "iso": "SE", "sql": "SELECT simple_pay(26, 34, 0);"}'); }
step "s1a735" { SELECT bcdb_tx_submit('{"hash": "44_3", "iso": "SE", "sql": "SELECT simple_pay(0, 42, 0);"}'); }
step "s1a736" { SELECT bcdb_tx_submit('{"hash": "44_4", "iso": "SE", "sql": "SELECT joint_pay(41, 31, 19, 0, 0);"}'); }
step "s1a737" { SELECT bcdb_tx_submit('{"hash": "44_5", "iso": "SE", "sql": "SELECT simple_pay(34, 4, 0);"}'); }
step "s1a738" { SELECT bcdb_tx_submit('{"hash": "44_6", "iso": "SE", "sql": "SELECT joint_pay(46, 31, 48, 0, 0);"}'); }
step "s1a739" { SELECT bcdb_tx_submit('{"hash": "44_7", "iso": "SE", "sql": "SELECT joint_pay(26, 39, 48, 0, 0);"}'); }
step "s1a740" { SELECT bcdb_tx_submit('{"hash": "44_8", "iso": "SE", "sql": "SELECT simple_pay(5, 47, 0);"}'); }
step "s1a741" { SELECT bcdb_tx_submit('{"hash": "44_9", "iso": "SE", "sql": "SELECT joint_pay(15, 39, 1, 0, 0);"}'); }
step "s1a742" { SELECT bcdb_tx_submit('{"hash": "44_10", "iso": "SE", "sql": "SELECT simple_pay(32, 23, 0);"}'); }
step "s1a743" { SELECT bcdb_tx_submit('{"hash": "44_11", "iso": "SE", "sql": "SELECT joint_pay(16, 7, 37, 0, 0);"}'); }
step "s1a744" { SELECT bcdb_tx_submit('{"hash": "44_12", "iso": "SE", "sql": "SELECT simple_pay(14, 24, 0);"}'); }
step "s1a745" { SELECT bcdb_tx_submit('{"hash": "44_13", "iso": "SE", "sql": "SELECT simple_pay(32, 21, 0);"}'); }
step "s1a746" { SELECT bcdb_tx_submit('{"hash": "44_14", "iso": "SE", "sql": "SELECT simple_pay(37, 16, 0);"}'); }
step "s1a747" { SELECT bcdb_tx_submit('{"hash": "44_15", "iso": "SE", "sql": "SELECT simple_pay(2, 9, 0);"}'); }
step "s1a748" { SELECT bcdb_block_submit('{"bid": 44, "txs": ["44_0", "44_1", "44_2", "44_3", "44_4", "44_5", "44_6", "44_7", "44_8", "44_9", "44_10", "44_11", "44_12", "44_13", "44_14", "44_15"]}'); }
step "s1a749" { SELECT bcdb_tx_submit('{"hash": "45_0", "iso": "SE", "sql": "SELECT simple_pay(37, 36, 0);"}'); }
step "s1a750" { SELECT bcdb_tx_submit('{"hash": "45_1", "iso": "SE", "sql": "SELECT simple_pay(33, 30, 0);"}'); }
step "s1a751" { SELECT bcdb_tx_submit('{"hash": "45_2", "iso": "SE", "sql": "SELECT simple_pay(24, 46, 0);"}'); }
step "s1a752" { SELECT bcdb_tx_submit('{"hash": "45_3", "iso": "SE", "sql": "SELECT simple_pay(7, 27, 0);"}'); }
step "s1a753" { SELECT bcdb_tx_submit('{"hash": "45_4", "iso": "SE", "sql": "SELECT simple_pay(8, 48, 0);"}'); }
step "s1a754" { SELECT bcdb_tx_submit('{"hash": "45_5", "iso": "SE", "sql": "SELECT joint_pay(1, 7, 45, 0, 0);"}'); }
step "s1a755" { SELECT bcdb_tx_submit('{"hash": "45_6", "iso": "SE", "sql": "SELECT simple_pay(2, 40, 0);"}'); }
step "s1a756" { SELECT bcdb_tx_submit('{"hash": "45_7", "iso": "SE", "sql": "SELECT simple_pay(24, 7, 0);"}'); }
step "s1a757" { SELECT bcdb_tx_submit('{"hash": "45_8", "iso": "SE", "sql": "SELECT simple_pay(23, 39, 0);"}'); }
step "s1a758" { SELECT bcdb_tx_submit('{"hash": "45_9", "iso": "SE", "sql": "SELECT simple_pay(12, 47, 0);"}'); }
step "s1a759" { SELECT bcdb_tx_submit('{"hash": "45_10", "iso": "SE", "sql": "SELECT simple_pay(34, 3, 0);"}'); }
step "s1a760" { SELECT bcdb_tx_submit('{"hash": "45_11", "iso": "SE", "sql": "SELECT simple_pay(35, 0, 0);"}'); }
step "s1a761" { SELECT bcdb_tx_submit('{"hash": "45_12", "iso": "SE", "sql": "SELECT joint_pay(31, 1, 40, 0, 0);"}'); }
step "s1a762" { SELECT bcdb_tx_submit('{"hash": "45_13", "iso": "SE", "sql": "SELECT simple_pay(21, 8, 0);"}'); }
step "s1a763" { SELECT bcdb_tx_submit('{"hash": "45_14", "iso": "SE", "sql": "SELECT simple_pay(6, 39, 0);"}'); }
step "s1a764" { SELECT bcdb_tx_submit('{"hash": "45_15", "iso": "SE", "sql": "SELECT simple_pay(48, 4, 0);"}'); }
step "s1a765" { SELECT bcdb_block_submit('{"bid": 45, "txs": ["45_0", "45_1", "45_2", "45_3", "45_4", "45_5", "45_6", "45_7", "45_8", "45_9", "45_10", "45_11", "45_12", "45_13", "45_14", "45_15"]}'); }
step "s1a766" { SELECT bcdb_tx_submit('{"hash": "46_0", "iso": "SE", "sql": "SELECT simple_pay(6, 33, 0);"}'); }
step "s1a767" { SELECT bcdb_tx_submit('{"hash": "46_1", "iso": "SE", "sql": "SELECT joint_pay(37, 8, 31, 0, 0);"}'); }
step "s1a768" { SELECT bcdb_tx_submit('{"hash": "46_2", "iso": "SE", "sql": "SELECT joint_pay(14, 22, 6, 0, 0);"}'); }
step "s1a769" { SELECT bcdb_tx_submit('{"hash": "46_3", "iso": "SE", "sql": "SELECT simple_pay(45, 13, 0);"}'); }
step "s1a770" { SELECT bcdb_tx_submit('{"hash": "46_4", "iso": "SE", "sql": "SELECT simple_pay(44, 42, 0);"}'); }
step "s1a771" { SELECT bcdb_tx_submit('{"hash": "46_5", "iso": "SE", "sql": "SELECT simple_pay(25, 12, 0);"}'); }
step "s1a772" { SELECT bcdb_tx_submit('{"hash": "46_6", "iso": "SE", "sql": "SELECT simple_pay(47, 28, 0);"}'); }
step "s1a773" { SELECT bcdb_tx_submit('{"hash": "46_7", "iso": "SE", "sql": "SELECT simple_pay(17, 46, 0);"}'); }
step "s1a774" { SELECT bcdb_tx_submit('{"hash": "46_8", "iso": "SE", "sql": "SELECT simple_pay(22, 35, 0);"}'); }
step "s1a775" { SELECT bcdb_tx_submit('{"hash": "46_9", "iso": "SE", "sql": "SELECT simple_pay(13, 29, 0);"}'); }
step "s1a776" { SELECT bcdb_tx_submit('{"hash": "46_10", "iso": "SE", "sql": "SELECT simple_pay(8, 17, 0);"}'); }
step "s1a777" { SELECT bcdb_tx_submit('{"hash": "46_11", "iso": "SE", "sql": "SELECT simple_pay(49, 0, 0);"}'); }
step "s1a778" { SELECT bcdb_tx_submit('{"hash": "46_12", "iso": "SE", "sql": "SELECT joint_pay(20, 19, 45, 0, 0);"}'); }
step "s1a779" { SELECT bcdb_tx_submit('{"hash": "46_13", "iso": "SE", "sql": "SELECT simple_pay(20, 2, 0);"}'); }
step "s1a780" { SELECT bcdb_tx_submit('{"hash": "46_14", "iso": "SE", "sql": "SELECT joint_pay(0, 18, 7, 0, 0);"}'); }
step "s1a781" { SELECT bcdb_tx_submit('{"hash": "46_15", "iso": "SE", "sql": "SELECT joint_pay(17, 12, 32, 0, 0);"}'); }
step "s1a782" { SELECT bcdb_block_submit('{"bid": 46, "txs": ["46_0", "46_1", "46_2", "46_3", "46_4", "46_5", "46_6", "46_7", "46_8", "46_9", "46_10", "46_11", "46_12", "46_13", "46_14", "46_15"]}'); }
step "s1a783" { SELECT bcdb_tx_submit('{"hash": "47_0", "iso": "SE", "sql": "SELECT simple_pay(28, 5, 0);"}'); }
step "s1a784" { SELECT bcdb_tx_submit('{"hash": "47_1", "iso": "SE", "sql": "SELECT simple_pay(34, 26, 0);"}'); }
step "s1a785" { SELECT bcdb_tx_submit('{"hash": "47_2", "iso": "SE", "sql": "SELECT joint_pay(37, 29, 20, 0, 0);"}'); }
step "s1a786" { SELECT bcdb_tx_submit('{"hash": "47_3", "iso": "SE", "sql": "SELECT joint_pay(15, 40, 27, 0, 0);"}'); }
step "s1a787" { SELECT bcdb_tx_submit('{"hash": "47_4", "iso": "SE", "sql": "SELECT simple_pay(18, 2, 0);"}'); }
step "s1a788" { SELECT bcdb_tx_submit('{"hash": "47_5", "iso": "SE", "sql": "SELECT joint_pay(0, 40, 17, 0, 0);"}'); }
step "s1a789" { SELECT bcdb_tx_submit('{"hash": "47_6", "iso": "SE", "sql": "SELECT joint_pay(42, 20, 35, 0, 0);"}'); }
step "s1a790" { SELECT bcdb_tx_submit('{"hash": "47_7", "iso": "SE", "sql": "SELECT simple_pay(18, 3, 0);"}'); }
step "s1a791" { SELECT bcdb_tx_submit('{"hash": "47_8", "iso": "SE", "sql": "SELECT simple_pay(15, 44, 0);"}'); }
step "s1a792" { SELECT bcdb_tx_submit('{"hash": "47_9", "iso": "SE", "sql": "SELECT simple_pay(16, 38, 0);"}'); }
step "s1a793" { SELECT bcdb_tx_submit('{"hash": "47_10", "iso": "SE", "sql": "SELECT joint_pay(24, 26, 17, 0, 0);"}'); }
step "s1a794" { SELECT bcdb_tx_submit('{"hash": "47_11", "iso": "SE", "sql": "SELECT simple_pay(16, 20, 0);"}'); }
step "s1a795" { SELECT bcdb_tx_submit('{"hash": "47_12", "iso": "SE", "sql": "SELECT simple_pay(34, 31, 0);"}'); }
step "s1a796" { SELECT bcdb_tx_submit('{"hash": "47_13", "iso": "SE", "sql": "SELECT simple_pay(45, 7, 0);"}'); }
step "s1a797" { SELECT bcdb_tx_submit('{"hash": "47_14", "iso": "SE", "sql": "SELECT simple_pay(10, 33, 0);"}'); }
step "s1a798" { SELECT bcdb_tx_submit('{"hash": "47_15", "iso": "SE", "sql": "SELECT joint_pay(45, 30, 24, 0, 0);"}'); }
step "s1a799" { SELECT bcdb_block_submit('{"bid": 47, "txs": ["47_0", "47_1", "47_2", "47_3", "47_4", "47_5", "47_6", "47_7", "47_8", "47_9", "47_10", "47_11", "47_12", "47_13", "47_14", "47_15"]}'); }
step "s1a800" { SELECT bcdb_tx_submit('{"hash": "48_0", "iso": "SE", "sql": "SELECT joint_pay(5, 19, 6, 0, 0);"}'); }
step "s1a801" { SELECT bcdb_tx_submit('{"hash": "48_1", "iso": "SE", "sql": "SELECT simple_pay(8, 28, 0);"}'); }
step "s1a802" { SELECT bcdb_tx_submit('{"hash": "48_2", "iso": "SE", "sql": "SELECT joint_pay(48, 23, 33, 0, 0);"}'); }
step "s1a803" { SELECT bcdb_tx_submit('{"hash": "48_3", "iso": "SE", "sql": "SELECT simple_pay(33, 15, 0);"}'); }
step "s1a804" { SELECT bcdb_tx_submit('{"hash": "48_4", "iso": "SE", "sql": "SELECT simple_pay(17, 25, 0);"}'); }
step "s1a805" { SELECT bcdb_tx_submit('{"hash": "48_5", "iso": "SE", "sql": "SELECT simple_pay(44, 3, 0);"}'); }
step "s1a806" { SELECT bcdb_tx_submit('{"hash": "48_6", "iso": "SE", "sql": "SELECT joint_pay(33, 22, 12, 0, 0);"}'); }
step "s1a807" { SELECT bcdb_tx_submit('{"hash": "48_7", "iso": "SE", "sql": "SELECT simple_pay(14, 19, 0);"}'); }
step "s1a808" { SELECT bcdb_tx_submit('{"hash": "48_8", "iso": "SE", "sql": "SELECT simple_pay(11, 35, 0);"}'); }
step "s1a809" { SELECT bcdb_tx_submit('{"hash": "48_9", "iso": "SE", "sql": "SELECT simple_pay(34, 1, 0);"}'); }
step "s1a810" { SELECT bcdb_tx_submit('{"hash": "48_10", "iso": "SE", "sql": "SELECT joint_pay(46, 26, 45, 0, 0);"}'); }
step "s1a811" { SELECT bcdb_tx_submit('{"hash": "48_11", "iso": "SE", "sql": "SELECT simple_pay(15, 48, 0);"}'); }
step "s1a812" { SELECT bcdb_tx_submit('{"hash": "48_12", "iso": "SE", "sql": "SELECT simple_pay(37, 43, 0);"}'); }
step "s1a813" { SELECT bcdb_tx_submit('{"hash": "48_13", "iso": "SE", "sql": "SELECT joint_pay(15, 33, 49, 0, 0);"}'); }
step "s1a814" { SELECT bcdb_tx_submit('{"hash": "48_14", "iso": "SE", "sql": "SELECT simple_pay(45, 47, 0);"}'); }
step "s1a815" { SELECT bcdb_tx_submit('{"hash": "48_15", "iso": "SE", "sql": "SELECT joint_pay(29, 12, 3, 0, 0);"}'); }
step "s1a816" { SELECT bcdb_block_submit('{"bid": 48, "txs": ["48_0", "48_1", "48_2", "48_3", "48_4", "48_5", "48_6", "48_7", "48_8", "48_9", "48_10", "48_11", "48_12", "48_13", "48_14", "48_15"]}'); }
step "s1a817" { SELECT bcdb_tx_submit('{"hash": "49_0", "iso": "SE", "sql": "SELECT simple_pay(24, 32, 0);"}'); }
step "s1a818" { SELECT bcdb_tx_submit('{"hash": "49_1", "iso": "SE", "sql": "SELECT simple_pay(24, 34, 0);"}'); }
step "s1a819" { SELECT bcdb_tx_submit('{"hash": "49_2", "iso": "SE", "sql": "SELECT simple_pay(6, 8, 0);"}'); }
step "s1a820" { SELECT bcdb_tx_submit('{"hash": "49_3", "iso": "SE", "sql": "SELECT simple_pay(34, 0, 0);"}'); }
step "s1a821" { SELECT bcdb_tx_submit('{"hash": "49_4", "iso": "SE", "sql": "SELECT simple_pay(5, 0, 0);"}'); }
step "s1a822" { SELECT bcdb_tx_submit('{"hash": "49_5", "iso": "SE", "sql": "SELECT simple_pay(15, 47, 0);"}'); }
step "s1a823" { SELECT bcdb_tx_submit('{"hash": "49_6", "iso": "SE", "sql": "SELECT simple_pay(43, 17, 0);"}'); }
step "s1a824" { SELECT bcdb_tx_submit('{"hash": "49_7", "iso": "SE", "sql": "SELECT simple_pay(22, 42, 0);"}'); }
step "s1a825" { SELECT bcdb_tx_submit('{"hash": "49_8", "iso": "SE", "sql": "SELECT simple_pay(46, 4, 0);"}'); }
step "s1a826" { SELECT bcdb_tx_submit('{"hash": "49_9", "iso": "SE", "sql": "SELECT simple_pay(10, 37, 0);"}'); }
step "s1a827" { SELECT bcdb_tx_submit('{"hash": "49_10", "iso": "SE", "sql": "SELECT simple_pay(13, 2, 0);"}'); }
step "s1a828" { SELECT bcdb_tx_submit('{"hash": "49_11", "iso": "SE", "sql": "SELECT simple_pay(3, 32, 0);"}'); }
step "s1a829" { SELECT bcdb_tx_submit('{"hash": "49_12", "iso": "SE", "sql": "SELECT simple_pay(44, 28, 0);"}'); }
step "s1a830" { SELECT bcdb_tx_submit('{"hash": "49_13", "iso": "SE", "sql": "SELECT simple_pay(45, 49, 0);"}'); }
step "s1a831" { SELECT bcdb_tx_submit('{"hash": "49_14", "iso": "SE", "sql": "SELECT simple_pay(42, 8, 0);"}'); }
step "s1a832" { SELECT bcdb_tx_submit('{"hash": "49_15", "iso": "SE", "sql": "SELECT simple_pay(32, 18, 0);"}'); }
step "s1a833" { SELECT bcdb_block_submit('{"bid": 49, "txs": ["49_0", "49_1", "49_2", "49_3", "49_4", "49_5", "49_6", "49_7", "49_8", "49_9", "49_10", "49_11", "49_12", "49_13", "49_14", "49_15"]}'); }
step "s1a834" { SELECT bcdb_tx_submit('{"hash": "50_0", "iso": "SE", "sql": "SELECT joint_pay(9, 22, 42, 0, 0);"}'); }
step "s1a835" { SELECT bcdb_tx_submit('{"hash": "50_1", "iso": "SE", "sql": "SELECT simple_pay(19, 32, 0);"}'); }
step "s1a836" { SELECT bcdb_tx_submit('{"hash": "50_2", "iso": "SE", "sql": "SELECT simple_pay(16, 8, 0);"}'); }
step "s1a837" { SELECT bcdb_tx_submit('{"hash": "50_3", "iso": "SE", "sql": "SELECT joint_pay(46, 12, 38, 0, 0);"}'); }
step "s1a838" { SELECT bcdb_tx_submit('{"hash": "50_4", "iso": "SE", "sql": "SELECT simple_pay(30, 19, 0);"}'); }
step "s1a839" { SELECT bcdb_tx_submit('{"hash": "50_5", "iso": "SE", "sql": "SELECT simple_pay(30, 18, 0);"}'); }
step "s1a840" { SELECT bcdb_tx_submit('{"hash": "50_6", "iso": "SE", "sql": "SELECT simple_pay(44, 21, 0);"}'); }
step "s1a841" { SELECT bcdb_tx_submit('{"hash": "50_7", "iso": "SE", "sql": "SELECT simple_pay(40, 38, 0);"}'); }
step "s1a842" { SELECT bcdb_tx_submit('{"hash": "50_8", "iso": "SE", "sql": "SELECT simple_pay(37, 25, 0);"}'); }
step "s1a843" { SELECT bcdb_tx_submit('{"hash": "50_9", "iso": "SE", "sql": "SELECT simple_pay(32, 19, 0);"}'); }
step "s1a844" { SELECT bcdb_tx_submit('{"hash": "50_10", "iso": "SE", "sql": "SELECT simple_pay(48, 36, 0);"}'); }
step "s1a845" { SELECT bcdb_tx_submit('{"hash": "50_11", "iso": "SE", "sql": "SELECT simple_pay(12, 27, 0);"}'); }
step "s1a846" { SELECT bcdb_tx_submit('{"hash": "50_12", "iso": "SE", "sql": "SELECT simple_pay(32, 10, 0);"}'); }
step "s1a847" { SELECT bcdb_tx_submit('{"hash": "50_13", "iso": "SE", "sql": "SELECT simple_pay(38, 33, 0);"}'); }
step "s1a848" { SELECT bcdb_tx_submit('{"hash": "50_14", "iso": "SE", "sql": "SELECT simple_pay(34, 49, 0);"}'); }
step "s1a849" { SELECT bcdb_tx_submit('{"hash": "50_15", "iso": "SE", "sql": "SELECT simple_pay(41, 30, 0);"}'); }
step "s1a850" { SELECT bcdb_block_submit('{"bid": 50, "txs": ["50_0", "50_1", "50_2", "50_3", "50_4", "50_5", "50_6", "50_7", "50_8", "50_9", "50_10", "50_11", "50_12", "50_13", "50_14", "50_15"]}'); }
step "s1a851" { SELECT bcdb_tx_submit('{"hash": "51_0", "iso": "SE", "sql": "SELECT simple_pay(16, 27, 0);"}'); }
step "s1a852" { SELECT bcdb_tx_submit('{"hash": "51_1", "iso": "SE", "sql": "SELECT simple_pay(41, 33, 0);"}'); }
step "s1a853" { SELECT bcdb_tx_submit('{"hash": "51_2", "iso": "SE", "sql": "SELECT joint_pay(46, 12, 16, 0, 0);"}'); }
step "s1a854" { SELECT bcdb_tx_submit('{"hash": "51_3", "iso": "SE", "sql": "SELECT simple_pay(4, 1, 0);"}'); }
step "s1a855" { SELECT bcdb_tx_submit('{"hash": "51_4", "iso": "SE", "sql": "SELECT simple_pay(6, 16, 0);"}'); }
step "s1a856" { SELECT bcdb_tx_submit('{"hash": "51_5", "iso": "SE", "sql": "SELECT simple_pay(0, 13, 0);"}'); }
step "s1a857" { SELECT bcdb_tx_submit('{"hash": "51_6", "iso": "SE", "sql": "SELECT simple_pay(11, 39, 0);"}'); }
step "s1a858" { SELECT bcdb_tx_submit('{"hash": "51_7", "iso": "SE", "sql": "SELECT joint_pay(42, 23, 39, 0, 0);"}'); }
step "s1a859" { SELECT bcdb_tx_submit('{"hash": "51_8", "iso": "SE", "sql": "SELECT simple_pay(0, 43, 0);"}'); }
step "s1a860" { SELECT bcdb_tx_submit('{"hash": "51_9", "iso": "SE", "sql": "SELECT simple_pay(1, 38, 0);"}'); }
step "s1a861" { SELECT bcdb_tx_submit('{"hash": "51_10", "iso": "SE", "sql": "SELECT simple_pay(10, 19, 0);"}'); }
step "s1a862" { SELECT bcdb_tx_submit('{"hash": "51_11", "iso": "SE", "sql": "SELECT simple_pay(15, 25, 0);"}'); }
step "s1a863" { SELECT bcdb_tx_submit('{"hash": "51_12", "iso": "SE", "sql": "SELECT simple_pay(47, 23, 0);"}'); }
step "s1a864" { SELECT bcdb_tx_submit('{"hash": "51_13", "iso": "SE", "sql": "SELECT simple_pay(5, 37, 0);"}'); }
step "s1a865" { SELECT bcdb_tx_submit('{"hash": "51_14", "iso": "SE", "sql": "SELECT simple_pay(7, 44, 0);"}'); }
step "s1a866" { SELECT bcdb_tx_submit('{"hash": "51_15", "iso": "SE", "sql": "SELECT joint_pay(11, 0, 38, 0, 0);"}'); }
step "s1a867" { SELECT bcdb_block_submit('{"bid": 51, "txs": ["51_0", "51_1", "51_2", "51_3", "51_4", "51_5", "51_6", "51_7", "51_8", "51_9", "51_10", "51_11", "51_12", "51_13", "51_14", "51_15"]}'); }
step "s1a868" { SELECT bcdb_tx_submit('{"hash": "52_0", "iso": "SE", "sql": "SELECT simple_pay(22, 47, 0);"}'); }
step "s1a869" { SELECT bcdb_tx_submit('{"hash": "52_1", "iso": "SE", "sql": "SELECT simple_pay(24, 12, 0);"}'); }
step "s1a870" { SELECT bcdb_tx_submit('{"hash": "52_2", "iso": "SE", "sql": "SELECT simple_pay(11, 31, 0);"}'); }
step "s1a871" { SELECT bcdb_tx_submit('{"hash": "52_3", "iso": "SE", "sql": "SELECT simple_pay(39, 37, 0);"}'); }
step "s1a872" { SELECT bcdb_tx_submit('{"hash": "52_4", "iso": "SE", "sql": "SELECT simple_pay(37, 40, 0);"}'); }
step "s1a873" { SELECT bcdb_tx_submit('{"hash": "52_5", "iso": "SE", "sql": "SELECT simple_pay(14, 0, 0);"}'); }
step "s1a874" { SELECT bcdb_tx_submit('{"hash": "52_6", "iso": "SE", "sql": "SELECT joint_pay(38, 2, 41, 0, 0);"}'); }
step "s1a875" { SELECT bcdb_tx_submit('{"hash": "52_7", "iso": "SE", "sql": "SELECT simple_pay(8, 32, 0);"}'); }
step "s1a876" { SELECT bcdb_tx_submit('{"hash": "52_8", "iso": "SE", "sql": "SELECT joint_pay(19, 21, 40, 0, 0);"}'); }
step "s1a877" { SELECT bcdb_tx_submit('{"hash": "52_9", "iso": "SE", "sql": "SELECT simple_pay(39, 12, 0);"}'); }
step "s1a878" { SELECT bcdb_tx_submit('{"hash": "52_10", "iso": "SE", "sql": "SELECT simple_pay(21, 8, 0);"}'); }
step "s1a879" { SELECT bcdb_tx_submit('{"hash": "52_11", "iso": "SE", "sql": "SELECT simple_pay(42, 47, 0);"}'); }
step "s1a880" { SELECT bcdb_tx_submit('{"hash": "52_12", "iso": "SE", "sql": "SELECT simple_pay(30, 38, 0);"}'); }
step "s1a881" { SELECT bcdb_tx_submit('{"hash": "52_13", "iso": "SE", "sql": "SELECT simple_pay(17, 41, 0);"}'); }
step "s1a882" { SELECT bcdb_tx_submit('{"hash": "52_14", "iso": "SE", "sql": "SELECT joint_pay(48, 10, 6, 0, 0);"}'); }
step "s1a883" { SELECT bcdb_tx_submit('{"hash": "52_15", "iso": "SE", "sql": "SELECT simple_pay(35, 45, 0);"}'); }
step "s1a884" { SELECT bcdb_block_submit('{"bid": 52, "txs": ["52_0", "52_1", "52_2", "52_3", "52_4", "52_5", "52_6", "52_7", "52_8", "52_9", "52_10", "52_11", "52_12", "52_13", "52_14", "52_15"]}'); }
step "s1a885" { SELECT bcdb_tx_submit('{"hash": "53_0", "iso": "SE", "sql": "SELECT simple_pay(28, 26, 0);"}'); }
step "s1a886" { SELECT bcdb_tx_submit('{"hash": "53_1", "iso": "SE", "sql": "SELECT simple_pay(38, 26, 0);"}'); }
step "s1a887" { SELECT bcdb_tx_submit('{"hash": "53_2", "iso": "SE", "sql": "SELECT simple_pay(43, 42, 0);"}'); }
step "s1a888" { SELECT bcdb_tx_submit('{"hash": "53_3", "iso": "SE", "sql": "SELECT simple_pay(49, 7, 0);"}'); }
step "s1a889" { SELECT bcdb_tx_submit('{"hash": "53_4", "iso": "SE", "sql": "SELECT simple_pay(7, 11, 0);"}'); }
step "s1a890" { SELECT bcdb_tx_submit('{"hash": "53_5", "iso": "SE", "sql": "SELECT simple_pay(30, 18, 0);"}'); }
step "s1a891" { SELECT bcdb_tx_submit('{"hash": "53_6", "iso": "SE", "sql": "SELECT simple_pay(6, 43, 0);"}'); }
step "s1a892" { SELECT bcdb_tx_submit('{"hash": "53_7", "iso": "SE", "sql": "SELECT simple_pay(16, 17, 0);"}'); }
step "s1a893" { SELECT bcdb_tx_submit('{"hash": "53_8", "iso": "SE", "sql": "SELECT simple_pay(40, 22, 0);"}'); }
step "s1a894" { SELECT bcdb_tx_submit('{"hash": "53_9", "iso": "SE", "sql": "SELECT simple_pay(34, 4, 0);"}'); }
step "s1a895" { SELECT bcdb_tx_submit('{"hash": "53_10", "iso": "SE", "sql": "SELECT joint_pay(38, 0, 49, 0, 0);"}'); }
step "s1a896" { SELECT bcdb_tx_submit('{"hash": "53_11", "iso": "SE", "sql": "SELECT simple_pay(7, 26, 0);"}'); }
step "s1a897" { SELECT bcdb_tx_submit('{"hash": "53_12", "iso": "SE", "sql": "SELECT simple_pay(30, 1, 0);"}'); }
step "s1a898" { SELECT bcdb_tx_submit('{"hash": "53_13", "iso": "SE", "sql": "SELECT simple_pay(8, 5, 0);"}'); }
step "s1a899" { SELECT bcdb_tx_submit('{"hash": "53_14", "iso": "SE", "sql": "SELECT simple_pay(41, 37, 0);"}'); }
step "s1a900" { SELECT bcdb_tx_submit('{"hash": "53_15", "iso": "SE", "sql": "SELECT simple_pay(14, 3, 0);"}'); }
step "s1a901" { SELECT bcdb_block_submit('{"bid": 53, "txs": ["53_0", "53_1", "53_2", "53_3", "53_4", "53_5", "53_6", "53_7", "53_8", "53_9", "53_10", "53_11", "53_12", "53_13", "53_14", "53_15"]}'); }
step "s1a902" { SELECT bcdb_tx_submit('{"hash": "54_0", "iso": "SE", "sql": "SELECT simple_pay(1, 3, 0);"}'); }
step "s1a903" { SELECT bcdb_tx_submit('{"hash": "54_1", "iso": "SE", "sql": "SELECT simple_pay(25, 8, 0);"}'); }
step "s1a904" { SELECT bcdb_tx_submit('{"hash": "54_2", "iso": "SE", "sql": "SELECT simple_pay(45, 19, 0);"}'); }
step "s1a905" { SELECT bcdb_tx_submit('{"hash": "54_3", "iso": "SE", "sql": "SELECT simple_pay(34, 3, 0);"}'); }
step "s1a906" { SELECT bcdb_tx_submit('{"hash": "54_4", "iso": "SE", "sql": "SELECT simple_pay(28, 34, 0);"}'); }
step "s1a907" { SELECT bcdb_tx_submit('{"hash": "54_5", "iso": "SE", "sql": "SELECT joint_pay(8, 41, 13, 0, 0);"}'); }
step "s1a908" { SELECT bcdb_tx_submit('{"hash": "54_6", "iso": "SE", "sql": "SELECT simple_pay(10, 5, 0);"}'); }
step "s1a909" { SELECT bcdb_tx_submit('{"hash": "54_7", "iso": "SE", "sql": "SELECT simple_pay(18, 17, 0);"}'); }
step "s1a910" { SELECT bcdb_tx_submit('{"hash": "54_8", "iso": "SE", "sql": "SELECT simple_pay(25, 43, 0);"}'); }
step "s1a911" { SELECT bcdb_tx_submit('{"hash": "54_9", "iso": "SE", "sql": "SELECT joint_pay(40, 3, 33, 0, 0);"}'); }
step "s1a912" { SELECT bcdb_tx_submit('{"hash": "54_10", "iso": "SE", "sql": "SELECT simple_pay(4, 0, 0);"}'); }
step "s1a913" { SELECT bcdb_tx_submit('{"hash": "54_11", "iso": "SE", "sql": "SELECT simple_pay(9, 49, 0);"}'); }
step "s1a914" { SELECT bcdb_tx_submit('{"hash": "54_12", "iso": "SE", "sql": "SELECT joint_pay(48, 32, 8, 0, 0);"}'); }
step "s1a915" { SELECT bcdb_tx_submit('{"hash": "54_13", "iso": "SE", "sql": "SELECT simple_pay(7, 21, 0);"}'); }
step "s1a916" { SELECT bcdb_tx_submit('{"hash": "54_14", "iso": "SE", "sql": "SELECT joint_pay(20, 9, 21, 0, 0);"}'); }
step "s1a917" { SELECT bcdb_tx_submit('{"hash": "54_15", "iso": "SE", "sql": "SELECT simple_pay(4, 5, 0);"}'); }
step "s1a918" { SELECT bcdb_block_submit('{"bid": 54, "txs": ["54_0", "54_1", "54_2", "54_3", "54_4", "54_5", "54_6", "54_7", "54_8", "54_9", "54_10", "54_11", "54_12", "54_13", "54_14", "54_15"]}'); }
step "s1a919" { SELECT bcdb_tx_submit('{"hash": "55_0", "iso": "SE", "sql": "SELECT simple_pay(16, 28, 0);"}'); }
step "s1a920" { SELECT bcdb_tx_submit('{"hash": "55_1", "iso": "SE", "sql": "SELECT simple_pay(31, 30, 0);"}'); }
step "s1a921" { SELECT bcdb_tx_submit('{"hash": "55_2", "iso": "SE", "sql": "SELECT simple_pay(5, 20, 0);"}'); }
step "s1a922" { SELECT bcdb_tx_submit('{"hash": "55_3", "iso": "SE", "sql": "SELECT simple_pay(49, 25, 0);"}'); }
step "s1a923" { SELECT bcdb_tx_submit('{"hash": "55_4", "iso": "SE", "sql": "SELECT simple_pay(35, 27, 0);"}'); }
step "s1a924" { SELECT bcdb_tx_submit('{"hash": "55_5", "iso": "SE", "sql": "SELECT simple_pay(14, 9, 0);"}'); }
step "s1a925" { SELECT bcdb_tx_submit('{"hash": "55_6", "iso": "SE", "sql": "SELECT simple_pay(32, 20, 0);"}'); }
step "s1a926" { SELECT bcdb_tx_submit('{"hash": "55_7", "iso": "SE", "sql": "SELECT joint_pay(4, 9, 2, 0, 0);"}'); }
step "s1a927" { SELECT bcdb_tx_submit('{"hash": "55_8", "iso": "SE", "sql": "SELECT simple_pay(36, 7, 0);"}'); }
step "s1a928" { SELECT bcdb_tx_submit('{"hash": "55_9", "iso": "SE", "sql": "SELECT simple_pay(33, 17, 0);"}'); }
step "s1a929" { SELECT bcdb_tx_submit('{"hash": "55_10", "iso": "SE", "sql": "SELECT simple_pay(22, 42, 0);"}'); }
step "s1a930" { SELECT bcdb_tx_submit('{"hash": "55_11", "iso": "SE", "sql": "SELECT simple_pay(30, 25, 0);"}'); }
step "s1a931" { SELECT bcdb_tx_submit('{"hash": "55_12", "iso": "SE", "sql": "SELECT simple_pay(20, 47, 0);"}'); }
step "s1a932" { SELECT bcdb_tx_submit('{"hash": "55_13", "iso": "SE", "sql": "SELECT simple_pay(39, 29, 0);"}'); }
step "s1a933" { SELECT bcdb_tx_submit('{"hash": "55_14", "iso": "SE", "sql": "SELECT simple_pay(14, 49, 0);"}'); }
step "s1a934" { SELECT bcdb_tx_submit('{"hash": "55_15", "iso": "SE", "sql": "SELECT simple_pay(46, 24, 0);"}'); }
step "s1a935" { SELECT bcdb_block_submit('{"bid": 55, "txs": ["55_0", "55_1", "55_2", "55_3", "55_4", "55_5", "55_6", "55_7", "55_8", "55_9", "55_10", "55_11", "55_12", "55_13", "55_14", "55_15"]}'); }
step "s1a936" { SELECT bcdb_tx_submit('{"hash": "56_0", "iso": "SE", "sql": "SELECT simple_pay(23, 21, 0);"}'); }
step "s1a937" { SELECT bcdb_tx_submit('{"hash": "56_1", "iso": "SE", "sql": "SELECT simple_pay(0, 15, 0);"}'); }
step "s1a938" { SELECT bcdb_tx_submit('{"hash": "56_2", "iso": "SE", "sql": "SELECT simple_pay(30, 7, 0);"}'); }
step "s1a939" { SELECT bcdb_tx_submit('{"hash": "56_3", "iso": "SE", "sql": "SELECT simple_pay(49, 39, 0);"}'); }
step "s1a940" { SELECT bcdb_tx_submit('{"hash": "56_4", "iso": "SE", "sql": "SELECT simple_pay(1, 33, 0);"}'); }
step "s1a941" { SELECT bcdb_tx_submit('{"hash": "56_5", "iso": "SE", "sql": "SELECT simple_pay(2, 36, 0);"}'); }
step "s1a942" { SELECT bcdb_tx_submit('{"hash": "56_6", "iso": "SE", "sql": "SELECT simple_pay(23, 11, 0);"}'); }
step "s1a943" { SELECT bcdb_tx_submit('{"hash": "56_7", "iso": "SE", "sql": "SELECT simple_pay(31, 30, 0);"}'); }
step "s1a944" { SELECT bcdb_tx_submit('{"hash": "56_8", "iso": "SE", "sql": "SELECT simple_pay(26, 0, 0);"}'); }
step "s1a945" { SELECT bcdb_tx_submit('{"hash": "56_9", "iso": "SE", "sql": "SELECT simple_pay(49, 15, 0);"}'); }
step "s1a946" { SELECT bcdb_tx_submit('{"hash": "56_10", "iso": "SE", "sql": "SELECT simple_pay(30, 47, 0);"}'); }
step "s1a947" { SELECT bcdb_tx_submit('{"hash": "56_11", "iso": "SE", "sql": "SELECT simple_pay(22, 43, 0);"}'); }
step "s1a948" { SELECT bcdb_tx_submit('{"hash": "56_12", "iso": "SE", "sql": "SELECT simple_pay(46, 10, 0);"}'); }
step "s1a949" { SELECT bcdb_tx_submit('{"hash": "56_13", "iso": "SE", "sql": "SELECT simple_pay(48, 47, 0);"}'); }
step "s1a950" { SELECT bcdb_tx_submit('{"hash": "56_14", "iso": "SE", "sql": "SELECT simple_pay(42, 10, 0);"}'); }
step "s1a951" { SELECT bcdb_tx_submit('{"hash": "56_15", "iso": "SE", "sql": "SELECT simple_pay(44, 18, 0);"}'); }
step "s1a952" { SELECT bcdb_block_submit('{"bid": 56, "txs": ["56_0", "56_1", "56_2", "56_3", "56_4", "56_5", "56_6", "56_7", "56_8", "56_9", "56_10", "56_11", "56_12", "56_13", "56_14", "56_15"]}'); }
step "s1a953" { SELECT bcdb_tx_submit('{"hash": "57_0", "iso": "SE", "sql": "SELECT simple_pay(37, 30, 0);"}'); }
step "s1a954" { SELECT bcdb_tx_submit('{"hash": "57_1", "iso": "SE", "sql": "SELECT simple_pay(1, 45, 0);"}'); }
step "s1a955" { SELECT bcdb_tx_submit('{"hash": "57_2", "iso": "SE", "sql": "SELECT simple_pay(39, 38, 0);"}'); }
step "s1a956" { SELECT bcdb_tx_submit('{"hash": "57_3", "iso": "SE", "sql": "SELECT simple_pay(42, 11, 0);"}'); }
step "s1a957" { SELECT bcdb_tx_submit('{"hash": "57_4", "iso": "SE", "sql": "SELECT simple_pay(20, 37, 0);"}'); }
step "s1a958" { SELECT bcdb_tx_submit('{"hash": "57_5", "iso": "SE", "sql": "SELECT simple_pay(27, 36, 0);"}'); }
step "s1a959" { SELECT bcdb_tx_submit('{"hash": "57_6", "iso": "SE", "sql": "SELECT simple_pay(40, 9, 0);"}'); }
step "s1a960" { SELECT bcdb_tx_submit('{"hash": "57_7", "iso": "SE", "sql": "SELECT simple_pay(25, 15, 0);"}'); }
step "s1a961" { SELECT bcdb_tx_submit('{"hash": "57_8", "iso": "SE", "sql": "SELECT simple_pay(18, 15, 0);"}'); }
step "s1a962" { SELECT bcdb_tx_submit('{"hash": "57_9", "iso": "SE", "sql": "SELECT simple_pay(15, 34, 0);"}'); }
step "s1a963" { SELECT bcdb_tx_submit('{"hash": "57_10", "iso": "SE", "sql": "SELECT simple_pay(23, 29, 0);"}'); }
step "s1a964" { SELECT bcdb_tx_submit('{"hash": "57_11", "iso": "SE", "sql": "SELECT simple_pay(21, 39, 0);"}'); }
step "s1a965" { SELECT bcdb_tx_submit('{"hash": "57_12", "iso": "SE", "sql": "SELECT simple_pay(20, 15, 0);"}'); }
step "s1a966" { SELECT bcdb_tx_submit('{"hash": "57_13", "iso": "SE", "sql": "SELECT joint_pay(48, 16, 35, 0, 0);"}'); }
step "s1a967" { SELECT bcdb_tx_submit('{"hash": "57_14", "iso": "SE", "sql": "SELECT joint_pay(45, 38, 7, 0, 0);"}'); }
step "s1a968" { SELECT bcdb_tx_submit('{"hash": "57_15", "iso": "SE", "sql": "SELECT simple_pay(28, 30, 0);"}'); }
step "s1a969" { SELECT bcdb_block_submit('{"bid": 57, "txs": ["57_0", "57_1", "57_2", "57_3", "57_4", "57_5", "57_6", "57_7", "57_8", "57_9", "57_10", "57_11", "57_12", "57_13", "57_14", "57_15"]}'); }
step "s1a970" { SELECT bcdb_tx_submit('{"hash": "58_0", "iso": "SE", "sql": "SELECT simple_pay(11, 38, 0);"}'); }
step "s1a971" { SELECT bcdb_tx_submit('{"hash": "58_1", "iso": "SE", "sql": "SELECT simple_pay(15, 45, 0);"}'); }
step "s1a972" { SELECT bcdb_tx_submit('{"hash": "58_2", "iso": "SE", "sql": "SELECT simple_pay(34, 31, 0);"}'); }
step "s1a973" { SELECT bcdb_tx_submit('{"hash": "58_3", "iso": "SE", "sql": "SELECT simple_pay(18, 24, 0);"}'); }
step "s1a974" { SELECT bcdb_tx_submit('{"hash": "58_4", "iso": "SE", "sql": "SELECT simple_pay(12, 22, 0);"}'); }
step "s1a975" { SELECT bcdb_tx_submit('{"hash": "58_5", "iso": "SE", "sql": "SELECT simple_pay(20, 46, 0);"}'); }
step "s1a976" { SELECT bcdb_tx_submit('{"hash": "58_6", "iso": "SE", "sql": "SELECT joint_pay(12, 38, 10, 0, 0);"}'); }
step "s1a977" { SELECT bcdb_tx_submit('{"hash": "58_7", "iso": "SE", "sql": "SELECT simple_pay(29, 5, 0);"}'); }
step "s1a978" { SELECT bcdb_tx_submit('{"hash": "58_8", "iso": "SE", "sql": "SELECT simple_pay(18, 44, 0);"}'); }
step "s1a979" { SELECT bcdb_tx_submit('{"hash": "58_9", "iso": "SE", "sql": "SELECT simple_pay(20, 43, 0);"}'); }
step "s1a980" { SELECT bcdb_tx_submit('{"hash": "58_10", "iso": "SE", "sql": "SELECT simple_pay(44, 24, 0);"}'); }
step "s1a981" { SELECT bcdb_tx_submit('{"hash": "58_11", "iso": "SE", "sql": "SELECT joint_pay(7, 3, 21, 0, 0);"}'); }
step "s1a982" { SELECT bcdb_tx_submit('{"hash": "58_12", "iso": "SE", "sql": "SELECT simple_pay(48, 17, 0);"}'); }
step "s1a983" { SELECT bcdb_tx_submit('{"hash": "58_13", "iso": "SE", "sql": "SELECT simple_pay(35, 28, 0);"}'); }
step "s1a984" { SELECT bcdb_tx_submit('{"hash": "58_14", "iso": "SE", "sql": "SELECT simple_pay(26, 30, 0);"}'); }
step "s1a985" { SELECT bcdb_tx_submit('{"hash": "58_15", "iso": "SE", "sql": "SELECT simple_pay(43, 5, 0);"}'); }
step "s1a986" { SELECT bcdb_block_submit('{"bid": 58, "txs": ["58_0", "58_1", "58_2", "58_3", "58_4", "58_5", "58_6", "58_7", "58_8", "58_9", "58_10", "58_11", "58_12", "58_13", "58_14", "58_15"]}'); }
step "s1a987" { SELECT bcdb_tx_submit('{"hash": "59_0", "iso": "SE", "sql": "SELECT simple_pay(40, 5, 0);"}'); }
step "s1a988" { SELECT bcdb_tx_submit('{"hash": "59_1", "iso": "SE", "sql": "SELECT simple_pay(1, 42, 0);"}'); }
step "s1a989" { SELECT bcdb_tx_submit('{"hash": "59_2", "iso": "SE", "sql": "SELECT simple_pay(21, 46, 0);"}'); }
step "s1a990" { SELECT bcdb_tx_submit('{"hash": "59_3", "iso": "SE", "sql": "SELECT simple_pay(6, 36, 0);"}'); }
step "s1a991" { SELECT bcdb_tx_submit('{"hash": "59_4", "iso": "SE", "sql": "SELECT simple_pay(2, 6, 0);"}'); }
step "s1a992" { SELECT bcdb_tx_submit('{"hash": "59_5", "iso": "SE", "sql": "SELECT simple_pay(46, 19, 0);"}'); }
step "s1a993" { SELECT bcdb_tx_submit('{"hash": "59_6", "iso": "SE", "sql": "SELECT joint_pay(37, 25, 45, 0, 0);"}'); }
step "s1a994" { SELECT bcdb_tx_submit('{"hash": "59_7", "iso": "SE", "sql": "SELECT joint_pay(36, 39, 33, 0, 0);"}'); }
step "s1a995" { SELECT bcdb_tx_submit('{"hash": "59_8", "iso": "SE", "sql": "SELECT simple_pay(12, 17, 0);"}'); }
step "s1a996" { SELECT bcdb_tx_submit('{"hash": "59_9", "iso": "SE", "sql": "SELECT simple_pay(11, 37, 0);"}'); }
step "s1a997" { SELECT bcdb_tx_submit('{"hash": "59_10", "iso": "SE", "sql": "SELECT simple_pay(8, 14, 0);"}'); }
step "s1a998" { SELECT bcdb_tx_submit('{"hash": "59_11", "iso": "SE", "sql": "SELECT simple_pay(19, 9, 0);"}'); }
step "s1a999" { SELECT bcdb_tx_submit('{"hash": "59_12", "iso": "SE", "sql": "SELECT simple_pay(17, 13, 0);"}'); }
step "s1a1000" { SELECT bcdb_tx_submit('{"hash": "59_13", "iso": "SE", "sql": "SELECT joint_pay(42, 26, 11, 0, 0);"}'); }
step "s1a1001" { SELECT bcdb_tx_submit('{"hash": "59_14", "iso": "SE", "sql": "SELECT joint_pay(37, 1, 22, 0, 0);"}'); }
step "s1a1002" { SELECT bcdb_tx_submit('{"hash": "59_15", "iso": "SE", "sql": "SELECT simple_pay(30, 43, 0);"}'); }
step "s1a1003" { SELECT bcdb_block_submit('{"bid": 59, "txs": ["59_0", "59_1", "59_2", "59_3", "59_4", "59_5", "59_6", "59_7", "59_8", "59_9", "59_10", "59_11", "59_12", "59_13", "59_14", "59_15"]}'); }
step "s1a1004" { SELECT bcdb_tx_submit('{"hash": "60_0", "iso": "SE", "sql": "SELECT joint_pay(47, 17, 5, 0, 0);"}'); }
step "s1a1005" { SELECT bcdb_tx_submit('{"hash": "60_1", "iso": "SE", "sql": "SELECT simple_pay(44, 39, 0);"}'); }
step "s1a1006" { SELECT bcdb_tx_submit('{"hash": "60_2", "iso": "SE", "sql": "SELECT simple_pay(17, 38, 0);"}'); }
step "s1a1007" { SELECT bcdb_tx_submit('{"hash": "60_3", "iso": "SE", "sql": "SELECT simple_pay(0, 9, 0);"}'); }
step "s1a1008" { SELECT bcdb_tx_submit('{"hash": "60_4", "iso": "SE", "sql": "SELECT simple_pay(47, 36, 0);"}'); }
step "s1a1009" { SELECT bcdb_tx_submit('{"hash": "60_5", "iso": "SE", "sql": "SELECT simple_pay(26, 8, 0);"}'); }
step "s1a1010" { SELECT bcdb_tx_submit('{"hash": "60_6", "iso": "SE", "sql": "SELECT joint_pay(34, 2, 32, 0, 0);"}'); }
step "s1a1011" { SELECT bcdb_tx_submit('{"hash": "60_7", "iso": "SE", "sql": "SELECT simple_pay(14, 42, 0);"}'); }
step "s1a1012" { SELECT bcdb_tx_submit('{"hash": "60_8", "iso": "SE", "sql": "SELECT joint_pay(20, 42, 28, 0, 0);"}'); }
step "s1a1013" { SELECT bcdb_tx_submit('{"hash": "60_9", "iso": "SE", "sql": "SELECT simple_pay(41, 40, 0);"}'); }
step "s1a1014" { SELECT bcdb_tx_submit('{"hash": "60_10", "iso": "SE", "sql": "SELECT simple_pay(43, 45, 0);"}'); }
step "s1a1015" { SELECT bcdb_tx_submit('{"hash": "60_11", "iso": "SE", "sql": "SELECT joint_pay(22, 31, 17, 0, 0);"}'); }
step "s1a1016" { SELECT bcdb_tx_submit('{"hash": "60_12", "iso": "SE", "sql": "SELECT simple_pay(37, 18, 0);"}'); }
step "s1a1017" { SELECT bcdb_tx_submit('{"hash": "60_13", "iso": "SE", "sql": "SELECT simple_pay(35, 25, 0);"}'); }
step "s1a1018" { SELECT bcdb_tx_submit('{"hash": "60_14", "iso": "SE", "sql": "SELECT joint_pay(24, 7, 37, 0, 0);"}'); }
step "s1a1019" { SELECT bcdb_tx_submit('{"hash": "60_15", "iso": "SE", "sql": "SELECT simple_pay(6, 33, 0);"}'); }
step "s1a1020" { SELECT bcdb_block_submit('{"bid": 60, "txs": ["60_0", "60_1", "60_2", "60_3", "60_4", "60_5", "60_6", "60_7", "60_8", "60_9", "60_10", "60_11", "60_12", "60_13", "60_14", "60_15"]}'); }
step "s1a1021" { SELECT bcdb_tx_submit('{"hash": "61_0", "iso": "SE", "sql": "SELECT simple_pay(45, 29, 0);"}'); }
step "s1a1022" { SELECT bcdb_tx_submit('{"hash": "61_1", "iso": "SE", "sql": "SELECT joint_pay(16, 46, 34, 0, 0);"}'); }
step "s1a1023" { SELECT bcdb_tx_submit('{"hash": "61_2", "iso": "SE", "sql": "SELECT joint_pay(11, 47, 4, 0, 0);"}'); }
step "s1a1024" { SELECT bcdb_tx_submit('{"hash": "61_3", "iso": "SE", "sql": "SELECT simple_pay(20, 24, 0);"}'); }
step "s1a1025" { SELECT bcdb_tx_submit('{"hash": "61_4", "iso": "SE", "sql": "SELECT simple_pay(22, 24, 0);"}'); }
step "s1a1026" { SELECT bcdb_tx_submit('{"hash": "61_5", "iso": "SE", "sql": "SELECT simple_pay(24, 35, 0);"}'); }
step "s1a1027" { SELECT bcdb_tx_submit('{"hash": "61_6", "iso": "SE", "sql": "SELECT joint_pay(45, 34, 36, 0, 0);"}'); }
step "s1a1028" { SELECT bcdb_tx_submit('{"hash": "61_7", "iso": "SE", "sql": "SELECT joint_pay(2, 19, 39, 0, 0);"}'); }
step "s1a1029" { SELECT bcdb_tx_submit('{"hash": "61_8", "iso": "SE", "sql": "SELECT simple_pay(48, 36, 0);"}'); }
step "s1a1030" { SELECT bcdb_tx_submit('{"hash": "61_9", "iso": "SE", "sql": "SELECT simple_pay(13, 29, 0);"}'); }
step "s1a1031" { SELECT bcdb_tx_submit('{"hash": "61_10", "iso": "SE", "sql": "SELECT simple_pay(5, 6, 0);"}'); }
step "s1a1032" { SELECT bcdb_tx_submit('{"hash": "61_11", "iso": "SE", "sql": "SELECT simple_pay(7, 32, 0);"}'); }
step "s1a1033" { SELECT bcdb_tx_submit('{"hash": "61_12", "iso": "SE", "sql": "SELECT simple_pay(47, 41, 0);"}'); }
step "s1a1034" { SELECT bcdb_tx_submit('{"hash": "61_13", "iso": "SE", "sql": "SELECT joint_pay(12, 14, 15, 0, 0);"}'); }
step "s1a1035" { SELECT bcdb_tx_submit('{"hash": "61_14", "iso": "SE", "sql": "SELECT joint_pay(24, 26, 4, 0, 0);"}'); }
step "s1a1036" { SELECT bcdb_tx_submit('{"hash": "61_15", "iso": "SE", "sql": "SELECT simple_pay(35, 13, 0);"}'); }
step "s1a1037" { SELECT bcdb_block_submit('{"bid": 61, "txs": ["61_0", "61_1", "61_2", "61_3", "61_4", "61_5", "61_6", "61_7", "61_8", "61_9", "61_10", "61_11", "61_12", "61_13", "61_14", "61_15"]}'); }
step "s1a1038" { SELECT bcdb_tx_submit('{"hash": "62_0", "iso": "SE", "sql": "SELECT simple_pay(13, 31, 0);"}'); }
step "s1a1039" { SELECT bcdb_tx_submit('{"hash": "62_1", "iso": "SE", "sql": "SELECT joint_pay(6, 32, 8, 0, 0);"}'); }
step "s1a1040" { SELECT bcdb_tx_submit('{"hash": "62_2", "iso": "SE", "sql": "SELECT simple_pay(35, 36, 0);"}'); }
step "s1a1041" { SELECT bcdb_tx_submit('{"hash": "62_3", "iso": "SE", "sql": "SELECT simple_pay(39, 27, 0);"}'); }
step "s1a1042" { SELECT bcdb_tx_submit('{"hash": "62_4", "iso": "SE", "sql": "SELECT simple_pay(41, 16, 0);"}'); }
step "s1a1043" { SELECT bcdb_tx_submit('{"hash": "62_5", "iso": "SE", "sql": "SELECT simple_pay(30, 40, 0);"}'); }
step "s1a1044" { SELECT bcdb_tx_submit('{"hash": "62_6", "iso": "SE", "sql": "SELECT simple_pay(1, 22, 0);"}'); }
step "s1a1045" { SELECT bcdb_tx_submit('{"hash": "62_7", "iso": "SE", "sql": "SELECT simple_pay(49, 13, 0);"}'); }
step "s1a1046" { SELECT bcdb_tx_submit('{"hash": "62_8", "iso": "SE", "sql": "SELECT simple_pay(2, 12, 0);"}'); }
step "s1a1047" { SELECT bcdb_tx_submit('{"hash": "62_9", "iso": "SE", "sql": "SELECT simple_pay(33, 43, 0);"}'); }
step "s1a1048" { SELECT bcdb_tx_submit('{"hash": "62_10", "iso": "SE", "sql": "SELECT simple_pay(0, 9, 0);"}'); }
step "s1a1049" { SELECT bcdb_tx_submit('{"hash": "62_11", "iso": "SE", "sql": "SELECT simple_pay(30, 5, 0);"}'); }
step "s1a1050" { SELECT bcdb_tx_submit('{"hash": "62_12", "iso": "SE", "sql": "SELECT simple_pay(41, 18, 0);"}'); }
step "s1a1051" { SELECT bcdb_tx_submit('{"hash": "62_13", "iso": "SE", "sql": "SELECT simple_pay(47, 46, 0);"}'); }
step "s1a1052" { SELECT bcdb_tx_submit('{"hash": "62_14", "iso": "SE", "sql": "SELECT simple_pay(45, 19, 0);"}'); }
step "s1a1053" { SELECT bcdb_tx_submit('{"hash": "62_15", "iso": "SE", "sql": "SELECT simple_pay(5, 39, 0);"}'); }
step "s1a1054" { SELECT bcdb_block_submit('{"bid": 62, "txs": ["62_0", "62_1", "62_2", "62_3", "62_4", "62_5", "62_6", "62_7", "62_8", "62_9", "62_10", "62_11", "62_12", "62_13", "62_14", "62_15"]}'); }
step "s1a1055" { SELECT bcdb_tx_submit('{"hash": "63_0", "iso": "SE", "sql": "SELECT joint_pay(31, 23, 39, 0, 0);"}'); }
step "s1a1056" { SELECT bcdb_tx_submit('{"hash": "63_1", "iso": "SE", "sql": "SELECT simple_pay(5, 14, 0);"}'); }
step "s1a1057" { SELECT bcdb_tx_submit('{"hash": "63_2", "iso": "SE", "sql": "SELECT simple_pay(26, 15, 0);"}'); }
step "s1a1058" { SELECT bcdb_tx_submit('{"hash": "63_3", "iso": "SE", "sql": "SELECT simple_pay(31, 18, 0);"}'); }
step "s1a1059" { SELECT bcdb_tx_submit('{"hash": "63_4", "iso": "SE", "sql": "SELECT joint_pay(40, 23, 47, 0, 0);"}'); }
step "s1a1060" { SELECT bcdb_tx_submit('{"hash": "63_5", "iso": "SE", "sql": "SELECT simple_pay(7, 32, 0);"}'); }
step "s1a1061" { SELECT bcdb_tx_submit('{"hash": "63_6", "iso": "SE", "sql": "SELECT simple_pay(43, 46, 0);"}'); }
step "s1a1062" { SELECT bcdb_tx_submit('{"hash": "63_7", "iso": "SE", "sql": "SELECT joint_pay(12, 18, 33, 0, 0);"}'); }
step "s1a1063" { SELECT bcdb_tx_submit('{"hash": "63_8", "iso": "SE", "sql": "SELECT simple_pay(41, 46, 0);"}'); }
step "s1a1064" { SELECT bcdb_tx_submit('{"hash": "63_9", "iso": "SE", "sql": "SELECT simple_pay(25, 2, 0);"}'); }
step "s1a1065" { SELECT bcdb_tx_submit('{"hash": "63_10", "iso": "SE", "sql": "SELECT joint_pay(4, 18, 40, 0, 0);"}'); }
step "s1a1066" { SELECT bcdb_tx_submit('{"hash": "63_11", "iso": "SE", "sql": "SELECT simple_pay(33, 12, 0);"}'); }
step "s1a1067" { SELECT bcdb_tx_submit('{"hash": "63_12", "iso": "SE", "sql": "SELECT simple_pay(31, 22, 0);"}'); }
step "s1a1068" { SELECT bcdb_tx_submit('{"hash": "63_13", "iso": "SE", "sql": "SELECT joint_pay(9, 36, 27, 0, 0);"}'); }
step "s1a1069" { SELECT bcdb_tx_submit('{"hash": "63_14", "iso": "SE", "sql": "SELECT simple_pay(13, 7, 0);"}'); }
step "s1a1070" { SELECT bcdb_tx_submit('{"hash": "63_15", "iso": "SE", "sql": "SELECT simple_pay(8, 28, 0);"}'); }
step "s1a1071" { SELECT bcdb_block_submit('{"bid": 63, "txs": ["63_0", "63_1", "63_2", "63_3", "63_4", "63_5", "63_6", "63_7", "63_8", "63_9", "63_10", "63_11", "63_12", "63_13", "63_14", "63_15"]}'); }
step "s1a1072" { SELECT bcdb_tx_submit('{"hash": "64_0", "iso": "SE", "sql": "SELECT simple_pay(34, 27, 0);"}'); }
step "s1a1073" { SELECT bcdb_tx_submit('{"hash": "64_1", "iso": "SE", "sql": "SELECT simple_pay(2, 19, 0);"}'); }
step "s1a1074" { SELECT bcdb_tx_submit('{"hash": "64_2", "iso": "SE", "sql": "SELECT simple_pay(36, 5, 0);"}'); }
step "s1a1075" { SELECT bcdb_tx_submit('{"hash": "64_3", "iso": "SE", "sql": "SELECT simple_pay(41, 6, 0);"}'); }
step "s1a1076" { SELECT bcdb_tx_submit('{"hash": "64_4", "iso": "SE", "sql": "SELECT joint_pay(15, 33, 2, 0, 0);"}'); }
step "s1a1077" { SELECT bcdb_tx_submit('{"hash": "64_5", "iso": "SE", "sql": "SELECT joint_pay(45, 43, 37, 0, 0);"}'); }
step "s1a1078" { SELECT bcdb_tx_submit('{"hash": "64_6", "iso": "SE", "sql": "SELECT joint_pay(16, 47, 37, 0, 0);"}'); }
step "s1a1079" { SELECT bcdb_tx_submit('{"hash": "64_7", "iso": "SE", "sql": "SELECT simple_pay(35, 24, 0);"}'); }
step "s1a1080" { SELECT bcdb_tx_submit('{"hash": "64_8", "iso": "SE", "sql": "SELECT joint_pay(40, 7, 43, 0, 0);"}'); }
step "s1a1081" { SELECT bcdb_tx_submit('{"hash": "64_9", "iso": "SE", "sql": "SELECT simple_pay(46, 49, 0);"}'); }
step "s1a1082" { SELECT bcdb_tx_submit('{"hash": "64_10", "iso": "SE", "sql": "SELECT simple_pay(31, 41, 0);"}'); }
step "s1a1083" { SELECT bcdb_tx_submit('{"hash": "64_11", "iso": "SE", "sql": "SELECT simple_pay(15, 0, 0);"}'); }
step "s1a1084" { SELECT bcdb_tx_submit('{"hash": "64_12", "iso": "SE", "sql": "SELECT simple_pay(45, 38, 0);"}'); }
step "s1a1085" { SELECT bcdb_tx_submit('{"hash": "64_13", "iso": "SE", "sql": "SELECT simple_pay(9, 40, 0);"}'); }
step "s1a1086" { SELECT bcdb_tx_submit('{"hash": "64_14", "iso": "SE", "sql": "SELECT simple_pay(48, 37, 0);"}'); }
step "s1a1087" { SELECT bcdb_tx_submit('{"hash": "64_15", "iso": "SE", "sql": "SELECT simple_pay(4, 6, 0);"}'); }
step "s1a1088" { SELECT bcdb_block_submit('{"bid": 64, "txs": ["64_0", "64_1", "64_2", "64_3", "64_4", "64_5", "64_6", "64_7", "64_8", "64_9", "64_10", "64_11", "64_12", "64_13", "64_14", "64_15"]}'); }
step "s1a1089" { SELECT bcdb_tx_submit('{"hash": "65_0", "iso": "SE", "sql": "SELECT simple_pay(17, 39, 0);"}'); }
step "s1a1090" { SELECT bcdb_tx_submit('{"hash": "65_1", "iso": "SE", "sql": "SELECT simple_pay(49, 16, 0);"}'); }
step "s1a1091" { SELECT bcdb_tx_submit('{"hash": "65_2", "iso": "SE", "sql": "SELECT simple_pay(2, 45, 0);"}'); }
step "s1a1092" { SELECT bcdb_tx_submit('{"hash": "65_3", "iso": "SE", "sql": "SELECT joint_pay(28, 3, 22, 0, 0);"}'); }
step "s1a1093" { SELECT bcdb_tx_submit('{"hash": "65_4", "iso": "SE", "sql": "SELECT simple_pay(40, 26, 0);"}'); }
step "s1a1094" { SELECT bcdb_tx_submit('{"hash": "65_5", "iso": "SE", "sql": "SELECT simple_pay(1, 18, 0);"}'); }
step "s1a1095" { SELECT bcdb_tx_submit('{"hash": "65_6", "iso": "SE", "sql": "SELECT simple_pay(13, 49, 0);"}'); }
step "s1a1096" { SELECT bcdb_tx_submit('{"hash": "65_7", "iso": "SE", "sql": "SELECT joint_pay(46, 9, 15, 0, 0);"}'); }
step "s1a1097" { SELECT bcdb_tx_submit('{"hash": "65_8", "iso": "SE", "sql": "SELECT simple_pay(13, 28, 0);"}'); }
step "s1a1098" { SELECT bcdb_tx_submit('{"hash": "65_9", "iso": "SE", "sql": "SELECT simple_pay(0, 48, 0);"}'); }
step "s1a1099" { SELECT bcdb_tx_submit('{"hash": "65_10", "iso": "SE", "sql": "SELECT simple_pay(37, 33, 0);"}'); }
step "s1a1100" { SELECT bcdb_tx_submit('{"hash": "65_11", "iso": "SE", "sql": "SELECT simple_pay(8, 45, 0);"}'); }
step "s1a1101" { SELECT bcdb_tx_submit('{"hash": "65_12", "iso": "SE", "sql": "SELECT simple_pay(36, 41, 0);"}'); }
step "s1a1102" { SELECT bcdb_tx_submit('{"hash": "65_13", "iso": "SE", "sql": "SELECT simple_pay(24, 12, 0);"}'); }
step "s1a1103" { SELECT bcdb_tx_submit('{"hash": "65_14", "iso": "SE", "sql": "SELECT simple_pay(28, 41, 0);"}'); }
step "s1a1104" { SELECT bcdb_tx_submit('{"hash": "65_15", "iso": "SE", "sql": "SELECT simple_pay(15, 41, 0);"}'); }
step "s1a1105" { SELECT bcdb_block_submit('{"bid": 65, "txs": ["65_0", "65_1", "65_2", "65_3", "65_4", "65_5", "65_6", "65_7", "65_8", "65_9", "65_10", "65_11", "65_12", "65_13", "65_14", "65_15"]}'); }
step "s1a1106" { SELECT bcdb_tx_submit('{"hash": "66_0", "iso": "SE", "sql": "SELECT simple_pay(49, 19, 0);"}'); }
step "s1a1107" { SELECT bcdb_tx_submit('{"hash": "66_1", "iso": "SE", "sql": "SELECT joint_pay(9, 28, 1, 0, 0);"}'); }
step "s1a1108" { SELECT bcdb_tx_submit('{"hash": "66_2", "iso": "SE", "sql": "SELECT simple_pay(41, 28, 0);"}'); }
step "s1a1109" { SELECT bcdb_tx_submit('{"hash": "66_3", "iso": "SE", "sql": "SELECT joint_pay(49, 18, 32, 0, 0);"}'); }
step "s1a1110" { SELECT bcdb_tx_submit('{"hash": "66_4", "iso": "SE", "sql": "SELECT simple_pay(27, 29, 0);"}'); }
step "s1a1111" { SELECT bcdb_tx_submit('{"hash": "66_5", "iso": "SE", "sql": "SELECT simple_pay(36, 47, 0);"}'); }
step "s1a1112" { SELECT bcdb_tx_submit('{"hash": "66_6", "iso": "SE", "sql": "SELECT simple_pay(10, 0, 0);"}'); }
step "s1a1113" { SELECT bcdb_tx_submit('{"hash": "66_7", "iso": "SE", "sql": "SELECT simple_pay(24, 45, 0);"}'); }
step "s1a1114" { SELECT bcdb_tx_submit('{"hash": "66_8", "iso": "SE", "sql": "SELECT simple_pay(31, 30, 0);"}'); }
step "s1a1115" { SELECT bcdb_tx_submit('{"hash": "66_9", "iso": "SE", "sql": "SELECT simple_pay(25, 8, 0);"}'); }
step "s1a1116" { SELECT bcdb_tx_submit('{"hash": "66_10", "iso": "SE", "sql": "SELECT simple_pay(17, 11, 0);"}'); }
step "s1a1117" { SELECT bcdb_tx_submit('{"hash": "66_11", "iso": "SE", "sql": "SELECT simple_pay(13, 21, 0);"}'); }
step "s1a1118" { SELECT bcdb_tx_submit('{"hash": "66_12", "iso": "SE", "sql": "SELECT simple_pay(45, 6, 0);"}'); }
step "s1a1119" { SELECT bcdb_tx_submit('{"hash": "66_13", "iso": "SE", "sql": "SELECT simple_pay(27, 19, 0);"}'); }
step "s1a1120" { SELECT bcdb_tx_submit('{"hash": "66_14", "iso": "SE", "sql": "SELECT simple_pay(46, 12, 0);"}'); }
step "s1a1121" { SELECT bcdb_tx_submit('{"hash": "66_15", "iso": "SE", "sql": "SELECT simple_pay(49, 8, 0);"}'); }
step "s1a1122" { SELECT bcdb_block_submit('{"bid": 66, "txs": ["66_0", "66_1", "66_2", "66_3", "66_4", "66_5", "66_6", "66_7", "66_8", "66_9", "66_10", "66_11", "66_12", "66_13", "66_14", "66_15"]}'); }
step "s1a1123" { SELECT bcdb_tx_submit('{"hash": "67_0", "iso": "SE", "sql": "SELECT simple_pay(7, 15, 0);"}'); }
step "s1a1124" { SELECT bcdb_tx_submit('{"hash": "67_1", "iso": "SE", "sql": "SELECT simple_pay(46, 30, 0);"}'); }
step "s1a1125" { SELECT bcdb_tx_submit('{"hash": "67_2", "iso": "SE", "sql": "SELECT simple_pay(43, 22, 0);"}'); }
step "s1a1126" { SELECT bcdb_tx_submit('{"hash": "67_3", "iso": "SE", "sql": "SELECT simple_pay(27, 26, 0);"}'); }
step "s1a1127" { SELECT bcdb_tx_submit('{"hash": "67_4", "iso": "SE", "sql": "SELECT simple_pay(6, 5, 0);"}'); }
step "s1a1128" { SELECT bcdb_tx_submit('{"hash": "67_5", "iso": "SE", "sql": "SELECT simple_pay(28, 8, 0);"}'); }
step "s1a1129" { SELECT bcdb_tx_submit('{"hash": "67_6", "iso": "SE", "sql": "SELECT joint_pay(33, 44, 24, 0, 0);"}'); }
step "s1a1130" { SELECT bcdb_tx_submit('{"hash": "67_7", "iso": "SE", "sql": "SELECT simple_pay(15, 25, 0);"}'); }
step "s1a1131" { SELECT bcdb_tx_submit('{"hash": "67_8", "iso": "SE", "sql": "SELECT simple_pay(6, 26, 0);"}'); }
step "s1a1132" { SELECT bcdb_tx_submit('{"hash": "67_9", "iso": "SE", "sql": "SELECT joint_pay(18, 38, 10, 0, 0);"}'); }
step "s1a1133" { SELECT bcdb_tx_submit('{"hash": "67_10", "iso": "SE", "sql": "SELECT simple_pay(33, 7, 0);"}'); }
step "s1a1134" { SELECT bcdb_tx_submit('{"hash": "67_11", "iso": "SE", "sql": "SELECT simple_pay(43, 21, 0);"}'); }
step "s1a1135" { SELECT bcdb_tx_submit('{"hash": "67_12", "iso": "SE", "sql": "SELECT joint_pay(9, 0, 5, 0, 0);"}'); }
step "s1a1136" { SELECT bcdb_tx_submit('{"hash": "67_13", "iso": "SE", "sql": "SELECT simple_pay(21, 28, 0);"}'); }
step "s1a1137" { SELECT bcdb_tx_submit('{"hash": "67_14", "iso": "SE", "sql": "SELECT simple_pay(15, 23, 0);"}'); }
step "s1a1138" { SELECT bcdb_tx_submit('{"hash": "67_15", "iso": "SE", "sql": "SELECT simple_pay(36, 29, 0);"}'); }
step "s1a1139" { SELECT bcdb_block_submit('{"bid": 67, "txs": ["67_0", "67_1", "67_2", "67_3", "67_4", "67_5", "67_6", "67_7", "67_8", "67_9", "67_10", "67_11", "67_12", "67_13", "67_14", "67_15"]}'); }
step "s1a1140" { SELECT bcdb_tx_submit('{"hash": "68_0", "iso": "SE", "sql": "SELECT simple_pay(10, 28, 0);"}'); }
step "s1a1141" { SELECT bcdb_tx_submit('{"hash": "68_1", "iso": "SE", "sql": "SELECT simple_pay(6, 0, 0);"}'); }
step "s1a1142" { SELECT bcdb_tx_submit('{"hash": "68_2", "iso": "SE", "sql": "SELECT joint_pay(46, 13, 19, 0, 0);"}'); }
step "s1a1143" { SELECT bcdb_tx_submit('{"hash": "68_3", "iso": "SE", "sql": "SELECT simple_pay(32, 49, 0);"}'); }
step "s1a1144" { SELECT bcdb_tx_submit('{"hash": "68_4", "iso": "SE", "sql": "SELECT simple_pay(5, 6, 0);"}'); }
step "s1a1145" { SELECT bcdb_tx_submit('{"hash": "68_5", "iso": "SE", "sql": "SELECT simple_pay(18, 47, 0);"}'); }
step "s1a1146" { SELECT bcdb_tx_submit('{"hash": "68_6", "iso": "SE", "sql": "SELECT joint_pay(7, 43, 10, 0, 0);"}'); }
step "s1a1147" { SELECT bcdb_tx_submit('{"hash": "68_7", "iso": "SE", "sql": "SELECT simple_pay(10, 29, 0);"}'); }
step "s1a1148" { SELECT bcdb_tx_submit('{"hash": "68_8", "iso": "SE", "sql": "SELECT simple_pay(44, 10, 0);"}'); }
step "s1a1149" { SELECT bcdb_tx_submit('{"hash": "68_9", "iso": "SE", "sql": "SELECT simple_pay(36, 1, 0);"}'); }
step "s1a1150" { SELECT bcdb_tx_submit('{"hash": "68_10", "iso": "SE", "sql": "SELECT simple_pay(1, 7, 0);"}'); }
step "s1a1151" { SELECT bcdb_tx_submit('{"hash": "68_11", "iso": "SE", "sql": "SELECT joint_pay(5, 40, 49, 0, 0);"}'); }
step "s1a1152" { SELECT bcdb_tx_submit('{"hash": "68_12", "iso": "SE", "sql": "SELECT simple_pay(16, 46, 0);"}'); }
step "s1a1153" { SELECT bcdb_tx_submit('{"hash": "68_13", "iso": "SE", "sql": "SELECT simple_pay(29, 41, 0);"}'); }
step "s1a1154" { SELECT bcdb_tx_submit('{"hash": "68_14", "iso": "SE", "sql": "SELECT simple_pay(35, 23, 0);"}'); }
step "s1a1155" { SELECT bcdb_tx_submit('{"hash": "68_15", "iso": "SE", "sql": "SELECT joint_pay(40, 0, 37, 0, 0);"}'); }
step "s1a1156" { SELECT bcdb_block_submit('{"bid": 68, "txs": ["68_0", "68_1", "68_2", "68_3", "68_4", "68_5", "68_6", "68_7", "68_8", "68_9", "68_10", "68_11", "68_12", "68_13", "68_14", "68_15"]}'); }
step "s1a1157" { SELECT bcdb_tx_submit('{"hash": "69_0", "iso": "SE", "sql": "SELECT simple_pay(38, 14, 0);"}'); }
step "s1a1158" { SELECT bcdb_tx_submit('{"hash": "69_1", "iso": "SE", "sql": "SELECT simple_pay(32, 20, 0);"}'); }
step "s1a1159" { SELECT bcdb_tx_submit('{"hash": "69_2", "iso": "SE", "sql": "SELECT simple_pay(48, 47, 0);"}'); }
step "s1a1160" { SELECT bcdb_tx_submit('{"hash": "69_3", "iso": "SE", "sql": "SELECT simple_pay(47, 45, 0);"}'); }
step "s1a1161" { SELECT bcdb_tx_submit('{"hash": "69_4", "iso": "SE", "sql": "SELECT simple_pay(22, 17, 0);"}'); }
step "s1a1162" { SELECT bcdb_tx_submit('{"hash": "69_5", "iso": "SE", "sql": "SELECT simple_pay(11, 14, 0);"}'); }
step "s1a1163" { SELECT bcdb_tx_submit('{"hash": "69_6", "iso": "SE", "sql": "SELECT simple_pay(20, 41, 0);"}'); }
step "s1a1164" { SELECT bcdb_tx_submit('{"hash": "69_7", "iso": "SE", "sql": "SELECT joint_pay(30, 39, 44, 0, 0);"}'); }
step "s1a1165" { SELECT bcdb_tx_submit('{"hash": "69_8", "iso": "SE", "sql": "SELECT simple_pay(15, 1, 0);"}'); }
step "s1a1166" { SELECT bcdb_tx_submit('{"hash": "69_9", "iso": "SE", "sql": "SELECT simple_pay(29, 46, 0);"}'); }
step "s1a1167" { SELECT bcdb_tx_submit('{"hash": "69_10", "iso": "SE", "sql": "SELECT simple_pay(11, 12, 0);"}'); }
step "s1a1168" { SELECT bcdb_tx_submit('{"hash": "69_11", "iso": "SE", "sql": "SELECT simple_pay(44, 38, 0);"}'); }
step "s1a1169" { SELECT bcdb_tx_submit('{"hash": "69_12", "iso": "SE", "sql": "SELECT simple_pay(8, 2, 0);"}'); }
step "s1a1170" { SELECT bcdb_tx_submit('{"hash": "69_13", "iso": "SE", "sql": "SELECT simple_pay(29, 28, 0);"}'); }
step "s1a1171" { SELECT bcdb_tx_submit('{"hash": "69_14", "iso": "SE", "sql": "SELECT simple_pay(12, 36, 0);"}'); }
step "s1a1172" { SELECT bcdb_tx_submit('{"hash": "69_15", "iso": "SE", "sql": "SELECT simple_pay(31, 8, 0);"}'); }
step "s1a1173" { SELECT bcdb_block_submit('{"bid": 69, "txs": ["69_0", "69_1", "69_2", "69_3", "69_4", "69_5", "69_6", "69_7", "69_8", "69_9", "69_10", "69_11", "69_12", "69_13", "69_14", "69_15"]}'); }
step "s1a1174" { SELECT bcdb_tx_submit('{"hash": "70_0", "iso": "SE", "sql": "SELECT simple_pay(46, 33, 0);"}'); }
step "s1a1175" { SELECT bcdb_tx_submit('{"hash": "70_1", "iso": "SE", "sql": "SELECT simple_pay(35, 25, 0);"}'); }
step "s1a1176" { SELECT bcdb_tx_submit('{"hash": "70_2", "iso": "SE", "sql": "SELECT simple_pay(13, 5, 0);"}'); }
step "s1a1177" { SELECT bcdb_tx_submit('{"hash": "70_3", "iso": "SE", "sql": "SELECT simple_pay(34, 30, 0);"}'); }
step "s1a1178" { SELECT bcdb_tx_submit('{"hash": "70_4", "iso": "SE", "sql": "SELECT simple_pay(21, 47, 0);"}'); }
step "s1a1179" { SELECT bcdb_tx_submit('{"hash": "70_5", "iso": "SE", "sql": "SELECT simple_pay(12, 39, 0);"}'); }
step "s1a1180" { SELECT bcdb_tx_submit('{"hash": "70_6", "iso": "SE", "sql": "SELECT simple_pay(48, 49, 0);"}'); }
step "s1a1181" { SELECT bcdb_tx_submit('{"hash": "70_7", "iso": "SE", "sql": "SELECT simple_pay(28, 45, 0);"}'); }
step "s1a1182" { SELECT bcdb_tx_submit('{"hash": "70_8", "iso": "SE", "sql": "SELECT simple_pay(18, 4, 0);"}'); }
step "s1a1183" { SELECT bcdb_tx_submit('{"hash": "70_9", "iso": "SE", "sql": "SELECT simple_pay(5, 22, 0);"}'); }
step "s1a1184" { SELECT bcdb_tx_submit('{"hash": "70_10", "iso": "SE", "sql": "SELECT simple_pay(26, 24, 0);"}'); }
step "s1a1185" { SELECT bcdb_tx_submit('{"hash": "70_11", "iso": "SE", "sql": "SELECT simple_pay(44, 48, 0);"}'); }
step "s1a1186" { SELECT bcdb_tx_submit('{"hash": "70_12", "iso": "SE", "sql": "SELECT simple_pay(14, 18, 0);"}'); }
step "s1a1187" { SELECT bcdb_tx_submit('{"hash": "70_13", "iso": "SE", "sql": "SELECT simple_pay(25, 35, 0);"}'); }
step "s1a1188" { SELECT bcdb_tx_submit('{"hash": "70_14", "iso": "SE", "sql": "SELECT joint_pay(27, 40, 18, 0, 0);"}'); }
step "s1a1189" { SELECT bcdb_tx_submit('{"hash": "70_15", "iso": "SE", "sql": "SELECT simple_pay(9, 25, 0);"}'); }
step "s1a1190" { SELECT bcdb_block_submit('{"bid": 70, "txs": ["70_0", "70_1", "70_2", "70_3", "70_4", "70_5", "70_6", "70_7", "70_8", "70_9", "70_10", "70_11", "70_12", "70_13", "70_14", "70_15"]}'); }
step "s1a1191" { SELECT bcdb_tx_submit('{"hash": "71_0", "iso": "SE", "sql": "SELECT simple_pay(27, 25, 0);"}'); }
step "s1a1192" { SELECT bcdb_tx_submit('{"hash": "71_1", "iso": "SE", "sql": "SELECT simple_pay(49, 37, 0);"}'); }
step "s1a1193" { SELECT bcdb_tx_submit('{"hash": "71_2", "iso": "SE", "sql": "SELECT simple_pay(19, 30, 0);"}'); }
step "s1a1194" { SELECT bcdb_tx_submit('{"hash": "71_3", "iso": "SE", "sql": "SELECT simple_pay(19, 26, 0);"}'); }
step "s1a1195" { SELECT bcdb_tx_submit('{"hash": "71_4", "iso": "SE", "sql": "SELECT simple_pay(37, 41, 0);"}'); }
step "s1a1196" { SELECT bcdb_tx_submit('{"hash": "71_5", "iso": "SE", "sql": "SELECT simple_pay(22, 2, 0);"}'); }
step "s1a1197" { SELECT bcdb_tx_submit('{"hash": "71_6", "iso": "SE", "sql": "SELECT simple_pay(28, 19, 0);"}'); }
step "s1a1198" { SELECT bcdb_tx_submit('{"hash": "71_7", "iso": "SE", "sql": "SELECT joint_pay(14, 21, 24, 0, 0);"}'); }
step "s1a1199" { SELECT bcdb_tx_submit('{"hash": "71_8", "iso": "SE", "sql": "SELECT joint_pay(21, 9, 11, 0, 0);"}'); }
step "s1a1200" { SELECT bcdb_tx_submit('{"hash": "71_9", "iso": "SE", "sql": "SELECT simple_pay(31, 4, 0);"}'); }
step "s1a1201" { SELECT bcdb_tx_submit('{"hash": "71_10", "iso": "SE", "sql": "SELECT simple_pay(11, 38, 0);"}'); }
step "s1a1202" { SELECT bcdb_tx_submit('{"hash": "71_11", "iso": "SE", "sql": "SELECT joint_pay(41, 11, 0, 0, 0);"}'); }
step "s1a1203" { SELECT bcdb_tx_submit('{"hash": "71_12", "iso": "SE", "sql": "SELECT simple_pay(43, 27, 0);"}'); }
step "s1a1204" { SELECT bcdb_tx_submit('{"hash": "71_13", "iso": "SE", "sql": "SELECT simple_pay(11, 18, 0);"}'); }
step "s1a1205" { SELECT bcdb_tx_submit('{"hash": "71_14", "iso": "SE", "sql": "SELECT simple_pay(19, 34, 0);"}'); }
step "s1a1206" { SELECT bcdb_tx_submit('{"hash": "71_15", "iso": "SE", "sql": "SELECT joint_pay(30, 10, 6, 0, 0);"}'); }
step "s1a1207" { SELECT bcdb_block_submit('{"bid": 71, "txs": ["71_0", "71_1", "71_2", "71_3", "71_4", "71_5", "71_6", "71_7", "71_8", "71_9", "71_10", "71_11", "71_12", "71_13", "71_14", "71_15"]}'); }
step "s1a1208" { SELECT bcdb_tx_submit('{"hash": "72_0", "iso": "SE", "sql": "SELECT simple_pay(30, 46, 0);"}'); }
step "s1a1209" { SELECT bcdb_tx_submit('{"hash": "72_1", "iso": "SE", "sql": "SELECT simple_pay(19, 25, 0);"}'); }
step "s1a1210" { SELECT bcdb_tx_submit('{"hash": "72_2", "iso": "SE", "sql": "SELECT joint_pay(17, 21, 48, 0, 0);"}'); }
step "s1a1211" { SELECT bcdb_tx_submit('{"hash": "72_3", "iso": "SE", "sql": "SELECT simple_pay(3, 48, 0);"}'); }
step "s1a1212" { SELECT bcdb_tx_submit('{"hash": "72_4", "iso": "SE", "sql": "SELECT simple_pay(18, 14, 0);"}'); }
step "s1a1213" { SELECT bcdb_tx_submit('{"hash": "72_5", "iso": "SE", "sql": "SELECT simple_pay(29, 40, 0);"}'); }
step "s1a1214" { SELECT bcdb_tx_submit('{"hash": "72_6", "iso": "SE", "sql": "SELECT simple_pay(13, 24, 0);"}'); }
step "s1a1215" { SELECT bcdb_tx_submit('{"hash": "72_7", "iso": "SE", "sql": "SELECT simple_pay(27, 2, 0);"}'); }
step "s1a1216" { SELECT bcdb_tx_submit('{"hash": "72_8", "iso": "SE", "sql": "SELECT joint_pay(5, 23, 0, 0, 0);"}'); }
step "s1a1217" { SELECT bcdb_tx_submit('{"hash": "72_9", "iso": "SE", "sql": "SELECT simple_pay(3, 0, 0);"}'); }
step "s1a1218" { SELECT bcdb_tx_submit('{"hash": "72_10", "iso": "SE", "sql": "SELECT joint_pay(2, 9, 38, 0, 0);"}'); }
step "s1a1219" { SELECT bcdb_tx_submit('{"hash": "72_11", "iso": "SE", "sql": "SELECT simple_pay(30, 41, 0);"}'); }
step "s1a1220" { SELECT bcdb_tx_submit('{"hash": "72_12", "iso": "SE", "sql": "SELECT joint_pay(8, 1, 47, 0, 0);"}'); }
step "s1a1221" { SELECT bcdb_tx_submit('{"hash": "72_13", "iso": "SE", "sql": "SELECT simple_pay(6, 4, 0);"}'); }
step "s1a1222" { SELECT bcdb_tx_submit('{"hash": "72_14", "iso": "SE", "sql": "SELECT simple_pay(38, 49, 0);"}'); }
step "s1a1223" { SELECT bcdb_tx_submit('{"hash": "72_15", "iso": "SE", "sql": "SELECT simple_pay(12, 6, 0);"}'); }
step "s1a1224" { SELECT bcdb_block_submit('{"bid": 72, "txs": ["72_0", "72_1", "72_2", "72_3", "72_4", "72_5", "72_6", "72_7", "72_8", "72_9", "72_10", "72_11", "72_12", "72_13", "72_14", "72_15"]}'); }
step "s1a1225" { SELECT bcdb_tx_submit('{"hash": "73_0", "iso": "SE", "sql": "SELECT simple_pay(27, 5, 0);"}'); }
step "s1a1226" { SELECT bcdb_tx_submit('{"hash": "73_1", "iso": "SE", "sql": "SELECT joint_pay(45, 28, 32, 0, 0);"}'); }
step "s1a1227" { SELECT bcdb_tx_submit('{"hash": "73_2", "iso": "SE", "sql": "SELECT simple_pay(10, 34, 0);"}'); }
step "s1a1228" { SELECT bcdb_tx_submit('{"hash": "73_3", "iso": "SE", "sql": "SELECT joint_pay(23, 46, 27, 0, 0);"}'); }
step "s1a1229" { SELECT bcdb_tx_submit('{"hash": "73_4", "iso": "SE", "sql": "SELECT simple_pay(5, 40, 0);"}'); }
step "s1a1230" { SELECT bcdb_tx_submit('{"hash": "73_5", "iso": "SE", "sql": "SELECT simple_pay(2, 46, 0);"}'); }
step "s1a1231" { SELECT bcdb_tx_submit('{"hash": "73_6", "iso": "SE", "sql": "SELECT simple_pay(15, 6, 0);"}'); }
step "s1a1232" { SELECT bcdb_tx_submit('{"hash": "73_7", "iso": "SE", "sql": "SELECT simple_pay(24, 23, 0);"}'); }
step "s1a1233" { SELECT bcdb_tx_submit('{"hash": "73_8", "iso": "SE", "sql": "SELECT simple_pay(20, 35, 0);"}'); }
step "s1a1234" { SELECT bcdb_tx_submit('{"hash": "73_9", "iso": "SE", "sql": "SELECT simple_pay(34, 25, 0);"}'); }
step "s1a1235" { SELECT bcdb_tx_submit('{"hash": "73_10", "iso": "SE", "sql": "SELECT simple_pay(15, 36, 0);"}'); }
step "s1a1236" { SELECT bcdb_tx_submit('{"hash": "73_11", "iso": "SE", "sql": "SELECT simple_pay(9, 38, 0);"}'); }
step "s1a1237" { SELECT bcdb_tx_submit('{"hash": "73_12", "iso": "SE", "sql": "SELECT simple_pay(49, 23, 0);"}'); }
step "s1a1238" { SELECT bcdb_tx_submit('{"hash": "73_13", "iso": "SE", "sql": "SELECT simple_pay(22, 32, 0);"}'); }
step "s1a1239" { SELECT bcdb_tx_submit('{"hash": "73_14", "iso": "SE", "sql": "SELECT simple_pay(0, 9, 0);"}'); }
step "s1a1240" { SELECT bcdb_tx_submit('{"hash": "73_15", "iso": "SE", "sql": "SELECT simple_pay(43, 44, 0);"}'); }
step "s1a1241" { SELECT bcdb_block_submit('{"bid": 73, "txs": ["73_0", "73_1", "73_2", "73_3", "73_4", "73_5", "73_6", "73_7", "73_8", "73_9", "73_10", "73_11", "73_12", "73_13", "73_14", "73_15"]}'); }
step "s1a1242" { SELECT bcdb_tx_submit('{"hash": "74_0", "iso": "SE", "sql": "SELECT simple_pay(8, 11, 0);"}'); }
step "s1a1243" { SELECT bcdb_tx_submit('{"hash": "74_1", "iso": "SE", "sql": "SELECT joint_pay(31, 47, 30, 0, 0);"}'); }
step "s1a1244" { SELECT bcdb_tx_submit('{"hash": "74_2", "iso": "SE", "sql": "SELECT simple_pay(17, 16, 0);"}'); }
step "s1a1245" { SELECT bcdb_tx_submit('{"hash": "74_3", "iso": "SE", "sql": "SELECT simple_pay(2, 11, 0);"}'); }
step "s1a1246" { SELECT bcdb_tx_submit('{"hash": "74_4", "iso": "SE", "sql": "SELECT simple_pay(22, 47, 0);"}'); }
step "s1a1247" { SELECT bcdb_tx_submit('{"hash": "74_5", "iso": "SE", "sql": "SELECT simple_pay(40, 6, 0);"}'); }
step "s1a1248" { SELECT bcdb_tx_submit('{"hash": "74_6", "iso": "SE", "sql": "SELECT simple_pay(31, 9, 0);"}'); }
step "s1a1249" { SELECT bcdb_tx_submit('{"hash": "74_7", "iso": "SE", "sql": "SELECT simple_pay(20, 12, 0);"}'); }
step "s1a1250" { SELECT bcdb_tx_submit('{"hash": "74_8", "iso": "SE", "sql": "SELECT simple_pay(39, 42, 0);"}'); }
step "s1a1251" { SELECT bcdb_tx_submit('{"hash": "74_9", "iso": "SE", "sql": "SELECT simple_pay(22, 25, 0);"}'); }
step "s1a1252" { SELECT bcdb_tx_submit('{"hash": "74_10", "iso": "SE", "sql": "SELECT simple_pay(17, 49, 0);"}'); }
step "s1a1253" { SELECT bcdb_tx_submit('{"hash": "74_11", "iso": "SE", "sql": "SELECT simple_pay(24, 35, 0);"}'); }
step "s1a1254" { SELECT bcdb_tx_submit('{"hash": "74_12", "iso": "SE", "sql": "SELECT simple_pay(40, 21, 0);"}'); }
step "s1a1255" { SELECT bcdb_tx_submit('{"hash": "74_13", "iso": "SE", "sql": "SELECT simple_pay(2, 48, 0);"}'); }
step "s1a1256" { SELECT bcdb_tx_submit('{"hash": "74_14", "iso": "SE", "sql": "SELECT simple_pay(17, 49, 0);"}'); }
step "s1a1257" { SELECT bcdb_tx_submit('{"hash": "74_15", "iso": "SE", "sql": "SELECT simple_pay(16, 2, 0);"}'); }
step "s1a1258" { SELECT bcdb_block_submit('{"bid": 74, "txs": ["74_0", "74_1", "74_2", "74_3", "74_4", "74_5", "74_6", "74_7", "74_8", "74_9", "74_10", "74_11", "74_12", "74_13", "74_14", "74_15"]}'); }
step "s1a1259" { SELECT bcdb_tx_submit('{"hash": "75_0", "iso": "SE", "sql": "SELECT simple_pay(17, 46, 0);"}'); }
step "s1a1260" { SELECT bcdb_tx_submit('{"hash": "75_1", "iso": "SE", "sql": "SELECT joint_pay(21, 41, 26, 0, 0);"}'); }
step "s1a1261" { SELECT bcdb_tx_submit('{"hash": "75_2", "iso": "SE", "sql": "SELECT joint_pay(43, 17, 14, 0, 0);"}'); }
step "s1a1262" { SELECT bcdb_tx_submit('{"hash": "75_3", "iso": "SE", "sql": "SELECT simple_pay(49, 45, 0);"}'); }
step "s1a1263" { SELECT bcdb_tx_submit('{"hash": "75_4", "iso": "SE", "sql": "SELECT joint_pay(23, 33, 40, 0, 0);"}'); }
step "s1a1264" { SELECT bcdb_tx_submit('{"hash": "75_5", "iso": "SE", "sql": "SELECT joint_pay(31, 12, 36, 0, 0);"}'); }
step "s1a1265" { SELECT bcdb_tx_submit('{"hash": "75_6", "iso": "SE", "sql": "SELECT simple_pay(4, 26, 0);"}'); }
step "s1a1266" { SELECT bcdb_tx_submit('{"hash": "75_7", "iso": "SE", "sql": "SELECT simple_pay(44, 43, 0);"}'); }
step "s1a1267" { SELECT bcdb_tx_submit('{"hash": "75_8", "iso": "SE", "sql": "SELECT joint_pay(0, 1, 38, 0, 0);"}'); }
step "s1a1268" { SELECT bcdb_tx_submit('{"hash": "75_9", "iso": "SE", "sql": "SELECT joint_pay(11, 25, 14, 0, 0);"}'); }
step "s1a1269" { SELECT bcdb_tx_submit('{"hash": "75_10", "iso": "SE", "sql": "SELECT simple_pay(12, 2, 0);"}'); }
step "s1a1270" { SELECT bcdb_tx_submit('{"hash": "75_11", "iso": "SE", "sql": "SELECT simple_pay(48, 12, 0);"}'); }
step "s1a1271" { SELECT bcdb_tx_submit('{"hash": "75_12", "iso": "SE", "sql": "SELECT simple_pay(34, 42, 0);"}'); }
step "s1a1272" { SELECT bcdb_tx_submit('{"hash": "75_13", "iso": "SE", "sql": "SELECT simple_pay(39, 21, 0);"}'); }
step "s1a1273" { SELECT bcdb_tx_submit('{"hash": "75_14", "iso": "SE", "sql": "SELECT simple_pay(22, 23, 0);"}'); }
step "s1a1274" { SELECT bcdb_tx_submit('{"hash": "75_15", "iso": "SE", "sql": "SELECT joint_pay(1, 26, 23, 0, 0);"}'); }
step "s1a1275" { SELECT bcdb_block_submit('{"bid": 75, "txs": ["75_0", "75_1", "75_2", "75_3", "75_4", "75_5", "75_6", "75_7", "75_8", "75_9", "75_10", "75_11", "75_12", "75_13", "75_14", "75_15"]}'); }
step "s1a1276" { SELECT bcdb_tx_submit('{"hash": "76_0", "iso": "SE", "sql": "SELECT joint_pay(14, 46, 43, 0, 0);"}'); }
step "s1a1277" { SELECT bcdb_tx_submit('{"hash": "76_1", "iso": "SE", "sql": "SELECT simple_pay(40, 47, 0);"}'); }
step "s1a1278" { SELECT bcdb_tx_submit('{"hash": "76_2", "iso": "SE", "sql": "SELECT simple_pay(40, 24, 0);"}'); }
step "s1a1279" { SELECT bcdb_tx_submit('{"hash": "76_3", "iso": "SE", "sql": "SELECT simple_pay(0, 42, 0);"}'); }
step "s1a1280" { SELECT bcdb_tx_submit('{"hash": "76_4", "iso": "SE", "sql": "SELECT simple_pay(12, 39, 0);"}'); }
step "s1a1281" { SELECT bcdb_tx_submit('{"hash": "76_5", "iso": "SE", "sql": "SELECT simple_pay(26, 48, 0);"}'); }
step "s1a1282" { SELECT bcdb_tx_submit('{"hash": "76_6", "iso": "SE", "sql": "SELECT simple_pay(9, 43, 0);"}'); }
step "s1a1283" { SELECT bcdb_tx_submit('{"hash": "76_7", "iso": "SE", "sql": "SELECT simple_pay(28, 47, 0);"}'); }
step "s1a1284" { SELECT bcdb_tx_submit('{"hash": "76_8", "iso": "SE", "sql": "SELECT simple_pay(47, 13, 0);"}'); }
step "s1a1285" { SELECT bcdb_tx_submit('{"hash": "76_9", "iso": "SE", "sql": "SELECT simple_pay(44, 10, 0);"}'); }
step "s1a1286" { SELECT bcdb_tx_submit('{"hash": "76_10", "iso": "SE", "sql": "SELECT simple_pay(0, 19, 0);"}'); }
step "s1a1287" { SELECT bcdb_tx_submit('{"hash": "76_11", "iso": "SE", "sql": "SELECT simple_pay(47, 11, 0);"}'); }
step "s1a1288" { SELECT bcdb_tx_submit('{"hash": "76_12", "iso": "SE", "sql": "SELECT joint_pay(9, 16, 11, 0, 0);"}'); }
step "s1a1289" { SELECT bcdb_tx_submit('{"hash": "76_13", "iso": "SE", "sql": "SELECT simple_pay(33, 41, 0);"}'); }
step "s1a1290" { SELECT bcdb_tx_submit('{"hash": "76_14", "iso": "SE", "sql": "SELECT simple_pay(34, 46, 0);"}'); }
step "s1a1291" { SELECT bcdb_tx_submit('{"hash": "76_15", "iso": "SE", "sql": "SELECT simple_pay(29, 7, 0);"}'); }
step "s1a1292" { SELECT bcdb_block_submit('{"bid": 76, "txs": ["76_0", "76_1", "76_2", "76_3", "76_4", "76_5", "76_6", "76_7", "76_8", "76_9", "76_10", "76_11", "76_12", "76_13", "76_14", "76_15"]}'); }
step "s1a1293" { SELECT bcdb_tx_submit('{"hash": "77_0", "iso": "SE", "sql": "SELECT simple_pay(20, 16, 0);"}'); }
step "s1a1294" { SELECT bcdb_tx_submit('{"hash": "77_1", "iso": "SE", "sql": "SELECT simple_pay(18, 24, 0);"}'); }
step "s1a1295" { SELECT bcdb_tx_submit('{"hash": "77_2", "iso": "SE", "sql": "SELECT simple_pay(1, 31, 0);"}'); }
step "s1a1296" { SELECT bcdb_tx_submit('{"hash": "77_3", "iso": "SE", "sql": "SELECT simple_pay(32, 12, 0);"}'); }
step "s1a1297" { SELECT bcdb_tx_submit('{"hash": "77_4", "iso": "SE", "sql": "SELECT simple_pay(46, 41, 0);"}'); }
step "s1a1298" { SELECT bcdb_tx_submit('{"hash": "77_5", "iso": "SE", "sql": "SELECT simple_pay(46, 2, 0);"}'); }
step "s1a1299" { SELECT bcdb_tx_submit('{"hash": "77_6", "iso": "SE", "sql": "SELECT simple_pay(26, 35, 0);"}'); }
step "s1a1300" { SELECT bcdb_tx_submit('{"hash": "77_7", "iso": "SE", "sql": "SELECT joint_pay(17, 45, 1, 0, 0);"}'); }
step "s1a1301" { SELECT bcdb_tx_submit('{"hash": "77_8", "iso": "SE", "sql": "SELECT joint_pay(43, 24, 34, 0, 0);"}'); }
step "s1a1302" { SELECT bcdb_tx_submit('{"hash": "77_9", "iso": "SE", "sql": "SELECT simple_pay(30, 33, 0);"}'); }
step "s1a1303" { SELECT bcdb_tx_submit('{"hash": "77_10", "iso": "SE", "sql": "SELECT simple_pay(47, 46, 0);"}'); }
step "s1a1304" { SELECT bcdb_tx_submit('{"hash": "77_11", "iso": "SE", "sql": "SELECT simple_pay(30, 37, 0);"}'); }
step "s1a1305" { SELECT bcdb_tx_submit('{"hash": "77_12", "iso": "SE", "sql": "SELECT joint_pay(37, 48, 1, 0, 0);"}'); }
step "s1a1306" { SELECT bcdb_tx_submit('{"hash": "77_13", "iso": "SE", "sql": "SELECT simple_pay(13, 19, 0);"}'); }
step "s1a1307" { SELECT bcdb_tx_submit('{"hash": "77_14", "iso": "SE", "sql": "SELECT simple_pay(14, 6, 0);"}'); }
step "s1a1308" { SELECT bcdb_tx_submit('{"hash": "77_15", "iso": "SE", "sql": "SELECT joint_pay(38, 29, 40, 0, 0);"}'); }
step "s1a1309" { SELECT bcdb_block_submit('{"bid": 77, "txs": ["77_0", "77_1", "77_2", "77_3", "77_4", "77_5", "77_6", "77_7", "77_8", "77_9", "77_10", "77_11", "77_12", "77_13", "77_14", "77_15"]}'); }
step "s1a1310" { SELECT bcdb_tx_submit('{"hash": "78_0", "iso": "SE", "sql": "SELECT joint_pay(31, 20, 28, 0, 0);"}'); }
step "s1a1311" { SELECT bcdb_tx_submit('{"hash": "78_1", "iso": "SE", "sql": "SELECT simple_pay(9, 31, 0);"}'); }
step "s1a1312" { SELECT bcdb_tx_submit('{"hash": "78_2", "iso": "SE", "sql": "SELECT simple_pay(16, 31, 0);"}'); }
step "s1a1313" { SELECT bcdb_tx_submit('{"hash": "78_3", "iso": "SE", "sql": "SELECT simple_pay(33, 46, 0);"}'); }
step "s1a1314" { SELECT bcdb_tx_submit('{"hash": "78_4", "iso": "SE", "sql": "SELECT simple_pay(14, 49, 0);"}'); }
step "s1a1315" { SELECT bcdb_tx_submit('{"hash": "78_5", "iso": "SE", "sql": "SELECT joint_pay(32, 16, 25, 0, 0);"}'); }
step "s1a1316" { SELECT bcdb_tx_submit('{"hash": "78_6", "iso": "SE", "sql": "SELECT simple_pay(41, 38, 0);"}'); }
step "s1a1317" { SELECT bcdb_tx_submit('{"hash": "78_7", "iso": "SE", "sql": "SELECT joint_pay(8, 32, 9, 0, 0);"}'); }
step "s1a1318" { SELECT bcdb_tx_submit('{"hash": "78_8", "iso": "SE", "sql": "SELECT joint_pay(21, 12, 2, 0, 0);"}'); }
step "s1a1319" { SELECT bcdb_tx_submit('{"hash": "78_9", "iso": "SE", "sql": "SELECT joint_pay(30, 4, 36, 0, 0);"}'); }
step "s1a1320" { SELECT bcdb_tx_submit('{"hash": "78_10", "iso": "SE", "sql": "SELECT simple_pay(8, 40, 0);"}'); }
step "s1a1321" { SELECT bcdb_tx_submit('{"hash": "78_11", "iso": "SE", "sql": "SELECT simple_pay(8, 36, 0);"}'); }
step "s1a1322" { SELECT bcdb_tx_submit('{"hash": "78_12", "iso": "SE", "sql": "SELECT simple_pay(19, 22, 0);"}'); }
step "s1a1323" { SELECT bcdb_tx_submit('{"hash": "78_13", "iso": "SE", "sql": "SELECT simple_pay(29, 23, 0);"}'); }
step "s1a1324" { SELECT bcdb_tx_submit('{"hash": "78_14", "iso": "SE", "sql": "SELECT joint_pay(6, 39, 43, 0, 0);"}'); }
step "s1a1325" { SELECT bcdb_tx_submit('{"hash": "78_15", "iso": "SE", "sql": "SELECT joint_pay(42, 19, 37, 0, 0);"}'); }
step "s1a1326" { SELECT bcdb_block_submit('{"bid": 78, "txs": ["78_0", "78_1", "78_2", "78_3", "78_4", "78_5", "78_6", "78_7", "78_8", "78_9", "78_10", "78_11", "78_12", "78_13", "78_14", "78_15"]}'); }
step "s1a1327" { SELECT bcdb_tx_submit('{"hash": "79_0", "iso": "SE", "sql": "SELECT simple_pay(49, 0, 0);"}'); }
step "s1a1328" { SELECT bcdb_tx_submit('{"hash": "79_1", "iso": "SE", "sql": "SELECT simple_pay(30, 25, 0);"}'); }
step "s1a1329" { SELECT bcdb_tx_submit('{"hash": "79_2", "iso": "SE", "sql": "SELECT simple_pay(13, 5, 0);"}'); }
step "s1a1330" { SELECT bcdb_tx_submit('{"hash": "79_3", "iso": "SE", "sql": "SELECT simple_pay(17, 31, 0);"}'); }
step "s1a1331" { SELECT bcdb_tx_submit('{"hash": "79_4", "iso": "SE", "sql": "SELECT simple_pay(31, 24, 0);"}'); }
step "s1a1332" { SELECT bcdb_tx_submit('{"hash": "79_5", "iso": "SE", "sql": "SELECT joint_pay(13, 48, 27, 0, 0);"}'); }
step "s1a1333" { SELECT bcdb_tx_submit('{"hash": "79_6", "iso": "SE", "sql": "SELECT simple_pay(12, 17, 0);"}'); }
step "s1a1334" { SELECT bcdb_tx_submit('{"hash": "79_7", "iso": "SE", "sql": "SELECT joint_pay(8, 29, 20, 0, 0);"}'); }
step "s1a1335" { SELECT bcdb_tx_submit('{"hash": "79_8", "iso": "SE", "sql": "SELECT simple_pay(28, 21, 0);"}'); }
step "s1a1336" { SELECT bcdb_tx_submit('{"hash": "79_9", "iso": "SE", "sql": "SELECT simple_pay(29, 8, 0);"}'); }
step "s1a1337" { SELECT bcdb_tx_submit('{"hash": "79_10", "iso": "SE", "sql": "SELECT simple_pay(14, 31, 0);"}'); }
step "s1a1338" { SELECT bcdb_tx_submit('{"hash": "79_11", "iso": "SE", "sql": "SELECT joint_pay(34, 37, 38, 0, 0);"}'); }
step "s1a1339" { SELECT bcdb_tx_submit('{"hash": "79_12", "iso": "SE", "sql": "SELECT simple_pay(20, 11, 0);"}'); }
step "s1a1340" { SELECT bcdb_tx_submit('{"hash": "79_13", "iso": "SE", "sql": "SELECT joint_pay(20, 10, 17, 0, 0);"}'); }
step "s1a1341" { SELECT bcdb_tx_submit('{"hash": "79_14", "iso": "SE", "sql": "SELECT simple_pay(42, 45, 0);"}'); }
step "s1a1342" { SELECT bcdb_tx_submit('{"hash": "79_15", "iso": "SE", "sql": "SELECT simple_pay(7, 24, 0);"}'); }
step "s1a1343" { SELECT bcdb_block_submit('{"bid": 79, "txs": ["79_0", "79_1", "79_2", "79_3", "79_4", "79_5", "79_6", "79_7", "79_8", "79_9", "79_10", "79_11", "79_12", "79_13", "79_14", "79_15"]}'); }
step "s1a1344" { SELECT bcdb_tx_submit('{"hash": "80_0", "iso": "SE", "sql": "SELECT simple_pay(20, 19, 0);"}'); }
step "s1a1345" { SELECT bcdb_tx_submit('{"hash": "80_1", "iso": "SE", "sql": "SELECT simple_pay(48, 0, 0);"}'); }
step "s1a1346" { SELECT bcdb_tx_submit('{"hash": "80_2", "iso": "SE", "sql": "SELECT joint_pay(41, 19, 40, 0, 0);"}'); }
step "s1a1347" { SELECT bcdb_tx_submit('{"hash": "80_3", "iso": "SE", "sql": "SELECT joint_pay(35, 10, 30, 0, 0);"}'); }
step "s1a1348" { SELECT bcdb_tx_submit('{"hash": "80_4", "iso": "SE", "sql": "SELECT simple_pay(5, 45, 0);"}'); }
step "s1a1349" { SELECT bcdb_tx_submit('{"hash": "80_5", "iso": "SE", "sql": "SELECT simple_pay(16, 45, 0);"}'); }
step "s1a1350" { SELECT bcdb_tx_submit('{"hash": "80_6", "iso": "SE", "sql": "SELECT joint_pay(24, 47, 5, 0, 0);"}'); }
step "s1a1351" { SELECT bcdb_tx_submit('{"hash": "80_7", "iso": "SE", "sql": "SELECT simple_pay(31, 42, 0);"}'); }
step "s1a1352" { SELECT bcdb_tx_submit('{"hash": "80_8", "iso": "SE", "sql": "SELECT joint_pay(9, 3, 7, 0, 0);"}'); }
step "s1a1353" { SELECT bcdb_tx_submit('{"hash": "80_9", "iso": "SE", "sql": "SELECT joint_pay(7, 25, 38, 0, 0);"}'); }
step "s1a1354" { SELECT bcdb_tx_submit('{"hash": "80_10", "iso": "SE", "sql": "SELECT simple_pay(18, 5, 0);"}'); }
step "s1a1355" { SELECT bcdb_tx_submit('{"hash": "80_11", "iso": "SE", "sql": "SELECT simple_pay(6, 13, 0);"}'); }
step "s1a1356" { SELECT bcdb_tx_submit('{"hash": "80_12", "iso": "SE", "sql": "SELECT simple_pay(19, 25, 0);"}'); }
step "s1a1357" { SELECT bcdb_tx_submit('{"hash": "80_13", "iso": "SE", "sql": "SELECT simple_pay(33, 28, 0);"}'); }
step "s1a1358" { SELECT bcdb_tx_submit('{"hash": "80_14", "iso": "SE", "sql": "SELECT simple_pay(48, 21, 0);"}'); }
step "s1a1359" { SELECT bcdb_tx_submit('{"hash": "80_15", "iso": "SE", "sql": "SELECT simple_pay(41, 25, 0);"}'); }
step "s1a1360" { SELECT bcdb_block_submit('{"bid": 80, "txs": ["80_0", "80_1", "80_2", "80_3", "80_4", "80_5", "80_6", "80_7", "80_8", "80_9", "80_10", "80_11", "80_12", "80_13", "80_14", "80_15"]}'); }
step "s1a1361" { SELECT bcdb_tx_submit('{"hash": "81_0", "iso": "SE", "sql": "SELECT simple_pay(11, 10, 0);"}'); }
step "s1a1362" { SELECT bcdb_tx_submit('{"hash": "81_1", "iso": "SE", "sql": "SELECT simple_pay(5, 13, 0);"}'); }
step "s1a1363" { SELECT bcdb_tx_submit('{"hash": "81_2", "iso": "SE", "sql": "SELECT simple_pay(49, 22, 0);"}'); }
step "s1a1364" { SELECT bcdb_tx_submit('{"hash": "81_3", "iso": "SE", "sql": "SELECT simple_pay(29, 42, 0);"}'); }
step "s1a1365" { SELECT bcdb_tx_submit('{"hash": "81_4", "iso": "SE", "sql": "SELECT simple_pay(21, 33, 0);"}'); }
step "s1a1366" { SELECT bcdb_tx_submit('{"hash": "81_5", "iso": "SE", "sql": "SELECT simple_pay(19, 29, 0);"}'); }
step "s1a1367" { SELECT bcdb_tx_submit('{"hash": "81_6", "iso": "SE", "sql": "SELECT simple_pay(8, 22, 0);"}'); }
step "s1a1368" { SELECT bcdb_tx_submit('{"hash": "81_7", "iso": "SE", "sql": "SELECT joint_pay(14, 4, 8, 0, 0);"}'); }
step "s1a1369" { SELECT bcdb_tx_submit('{"hash": "81_8", "iso": "SE", "sql": "SELECT simple_pay(28, 27, 0);"}'); }
step "s1a1370" { SELECT bcdb_tx_submit('{"hash": "81_9", "iso": "SE", "sql": "SELECT joint_pay(48, 14, 7, 0, 0);"}'); }
step "s1a1371" { SELECT bcdb_tx_submit('{"hash": "81_10", "iso": "SE", "sql": "SELECT simple_pay(12, 15, 0);"}'); }
step "s1a1372" { SELECT bcdb_tx_submit('{"hash": "81_11", "iso": "SE", "sql": "SELECT simple_pay(20, 42, 0);"}'); }
step "s1a1373" { SELECT bcdb_tx_submit('{"hash": "81_12", "iso": "SE", "sql": "SELECT simple_pay(21, 37, 0);"}'); }
step "s1a1374" { SELECT bcdb_tx_submit('{"hash": "81_13", "iso": "SE", "sql": "SELECT simple_pay(30, 32, 0);"}'); }
step "s1a1375" { SELECT bcdb_tx_submit('{"hash": "81_14", "iso": "SE", "sql": "SELECT simple_pay(17, 49, 0);"}'); }
step "s1a1376" { SELECT bcdb_tx_submit('{"hash": "81_15", "iso": "SE", "sql": "SELECT simple_pay(39, 43, 0);"}'); }
step "s1a1377" { SELECT bcdb_block_submit('{"bid": 81, "txs": ["81_0", "81_1", "81_2", "81_3", "81_4", "81_5", "81_6", "81_7", "81_8", "81_9", "81_10", "81_11", "81_12", "81_13", "81_14", "81_15"]}'); }
step "s1a1378" { SELECT bcdb_tx_submit('{"hash": "82_0", "iso": "SE", "sql": "SELECT simple_pay(11, 17, 0);"}'); }
step "s1a1379" { SELECT bcdb_tx_submit('{"hash": "82_1", "iso": "SE", "sql": "SELECT joint_pay(35, 45, 7, 0, 0);"}'); }
step "s1a1380" { SELECT bcdb_tx_submit('{"hash": "82_2", "iso": "SE", "sql": "SELECT simple_pay(11, 7, 0);"}'); }
step "s1a1381" { SELECT bcdb_tx_submit('{"hash": "82_3", "iso": "SE", "sql": "SELECT joint_pay(33, 35, 39, 0, 0);"}'); }
step "s1a1382" { SELECT bcdb_tx_submit('{"hash": "82_4", "iso": "SE", "sql": "SELECT simple_pay(47, 42, 0);"}'); }
step "s1a1383" { SELECT bcdb_tx_submit('{"hash": "82_5", "iso": "SE", "sql": "SELECT simple_pay(26, 20, 0);"}'); }
step "s1a1384" { SELECT bcdb_tx_submit('{"hash": "82_6", "iso": "SE", "sql": "SELECT simple_pay(21, 14, 0);"}'); }
step "s1a1385" { SELECT bcdb_tx_submit('{"hash": "82_7", "iso": "SE", "sql": "SELECT simple_pay(31, 9, 0);"}'); }
step "s1a1386" { SELECT bcdb_tx_submit('{"hash": "82_8", "iso": "SE", "sql": "SELECT simple_pay(47, 1, 0);"}'); }
step "s1a1387" { SELECT bcdb_tx_submit('{"hash": "82_9", "iso": "SE", "sql": "SELECT simple_pay(30, 8, 0);"}'); }
step "s1a1388" { SELECT bcdb_tx_submit('{"hash": "82_10", "iso": "SE", "sql": "SELECT joint_pay(35, 1, 8, 0, 0);"}'); }
step "s1a1389" { SELECT bcdb_tx_submit('{"hash": "82_11", "iso": "SE", "sql": "SELECT simple_pay(7, 3, 0);"}'); }
step "s1a1390" { SELECT bcdb_tx_submit('{"hash": "82_12", "iso": "SE", "sql": "SELECT simple_pay(19, 42, 0);"}'); }
step "s1a1391" { SELECT bcdb_tx_submit('{"hash": "82_13", "iso": "SE", "sql": "SELECT joint_pay(4, 43, 3, 0, 0);"}'); }
step "s1a1392" { SELECT bcdb_tx_submit('{"hash": "82_14", "iso": "SE", "sql": "SELECT simple_pay(46, 11, 0);"}'); }
step "s1a1393" { SELECT bcdb_tx_submit('{"hash": "82_15", "iso": "SE", "sql": "SELECT simple_pay(23, 24, 0);"}'); }
step "s1a1394" { SELECT bcdb_block_submit('{"bid": 82, "txs": ["82_0", "82_1", "82_2", "82_3", "82_4", "82_5", "82_6", "82_7", "82_8", "82_9", "82_10", "82_11", "82_12", "82_13", "82_14", "82_15"]}'); }
step "s1a1395" { SELECT bcdb_tx_submit('{"hash": "83_0", "iso": "SE", "sql": "SELECT simple_pay(33, 39, 0);"}'); }
step "s1a1396" { SELECT bcdb_tx_submit('{"hash": "83_1", "iso": "SE", "sql": "SELECT simple_pay(23, 26, 0);"}'); }
step "s1a1397" { SELECT bcdb_tx_submit('{"hash": "83_2", "iso": "SE", "sql": "SELECT simple_pay(46, 2, 0);"}'); }
step "s1a1398" { SELECT bcdb_tx_submit('{"hash": "83_3", "iso": "SE", "sql": "SELECT simple_pay(14, 36, 0);"}'); }
step "s1a1399" { SELECT bcdb_tx_submit('{"hash": "83_4", "iso": "SE", "sql": "SELECT joint_pay(28, 47, 0, 0, 0);"}'); }
step "s1a1400" { SELECT bcdb_tx_submit('{"hash": "83_5", "iso": "SE", "sql": "SELECT simple_pay(49, 12, 0);"}'); }
step "s1a1401" { SELECT bcdb_tx_submit('{"hash": "83_6", "iso": "SE", "sql": "SELECT joint_pay(40, 8, 20, 0, 0);"}'); }
step "s1a1402" { SELECT bcdb_tx_submit('{"hash": "83_7", "iso": "SE", "sql": "SELECT simple_pay(18, 49, 0);"}'); }
step "s1a1403" { SELECT bcdb_tx_submit('{"hash": "83_8", "iso": "SE", "sql": "SELECT simple_pay(21, 33, 0);"}'); }
step "s1a1404" { SELECT bcdb_tx_submit('{"hash": "83_9", "iso": "SE", "sql": "SELECT simple_pay(21, 17, 0);"}'); }
step "s1a1405" { SELECT bcdb_tx_submit('{"hash": "83_10", "iso": "SE", "sql": "SELECT simple_pay(19, 28, 0);"}'); }
step "s1a1406" { SELECT bcdb_tx_submit('{"hash": "83_11", "iso": "SE", "sql": "SELECT simple_pay(21, 25, 0);"}'); }
step "s1a1407" { SELECT bcdb_tx_submit('{"hash": "83_12", "iso": "SE", "sql": "SELECT simple_pay(25, 48, 0);"}'); }
step "s1a1408" { SELECT bcdb_tx_submit('{"hash": "83_13", "iso": "SE", "sql": "SELECT simple_pay(44, 0, 0);"}'); }
step "s1a1409" { SELECT bcdb_tx_submit('{"hash": "83_14", "iso": "SE", "sql": "SELECT simple_pay(45, 29, 0);"}'); }
step "s1a1410" { SELECT bcdb_tx_submit('{"hash": "83_15", "iso": "SE", "sql": "SELECT simple_pay(25, 27, 0);"}'); }
step "s1a1411" { SELECT bcdb_block_submit('{"bid": 83, "txs": ["83_0", "83_1", "83_2", "83_3", "83_4", "83_5", "83_6", "83_7", "83_8", "83_9", "83_10", "83_11", "83_12", "83_13", "83_14", "83_15"]}'); }
step "s1a1412" { SELECT bcdb_tx_submit('{"hash": "84_0", "iso": "SE", "sql": "SELECT simple_pay(43, 8, 0);"}'); }
step "s1a1413" { SELECT bcdb_tx_submit('{"hash": "84_1", "iso": "SE", "sql": "SELECT simple_pay(11, 30, 0);"}'); }
step "s1a1414" { SELECT bcdb_tx_submit('{"hash": "84_2", "iso": "SE", "sql": "SELECT joint_pay(10, 39, 12, 0, 0);"}'); }
step "s1a1415" { SELECT bcdb_tx_submit('{"hash": "84_3", "iso": "SE", "sql": "SELECT joint_pay(17, 32, 10, 0, 0);"}'); }
step "s1a1416" { SELECT bcdb_tx_submit('{"hash": "84_4", "iso": "SE", "sql": "SELECT simple_pay(11, 42, 0);"}'); }
step "s1a1417" { SELECT bcdb_tx_submit('{"hash": "84_5", "iso": "SE", "sql": "SELECT simple_pay(30, 15, 0);"}'); }
step "s1a1418" { SELECT bcdb_tx_submit('{"hash": "84_6", "iso": "SE", "sql": "SELECT simple_pay(11, 7, 0);"}'); }
step "s1a1419" { SELECT bcdb_tx_submit('{"hash": "84_7", "iso": "SE", "sql": "SELECT simple_pay(3, 33, 0);"}'); }
step "s1a1420" { SELECT bcdb_tx_submit('{"hash": "84_8", "iso": "SE", "sql": "SELECT joint_pay(47, 5, 46, 0, 0);"}'); }
step "s1a1421" { SELECT bcdb_tx_submit('{"hash": "84_9", "iso": "SE", "sql": "SELECT joint_pay(37, 8, 9, 0, 0);"}'); }
step "s1a1422" { SELECT bcdb_tx_submit('{"hash": "84_10", "iso": "SE", "sql": "SELECT simple_pay(41, 22, 0);"}'); }
step "s1a1423" { SELECT bcdb_tx_submit('{"hash": "84_11", "iso": "SE", "sql": "SELECT simple_pay(6, 24, 0);"}'); }
step "s1a1424" { SELECT bcdb_tx_submit('{"hash": "84_12", "iso": "SE", "sql": "SELECT simple_pay(21, 36, 0);"}'); }
step "s1a1425" { SELECT bcdb_tx_submit('{"hash": "84_13", "iso": "SE", "sql": "SELECT simple_pay(13, 38, 0);"}'); }
step "s1a1426" { SELECT bcdb_tx_submit('{"hash": "84_14", "iso": "SE", "sql": "SELECT simple_pay(38, 36, 0);"}'); }
step "s1a1427" { SELECT bcdb_tx_submit('{"hash": "84_15", "iso": "SE", "sql": "SELECT simple_pay(18, 6, 0);"}'); }
step "s1a1428" { SELECT bcdb_block_submit('{"bid": 84, "txs": ["84_0", "84_1", "84_2", "84_3", "84_4", "84_5", "84_6", "84_7", "84_8", "84_9", "84_10", "84_11", "84_12", "84_13", "84_14", "84_15"]}'); }
step "s1a1429" { SELECT bcdb_tx_submit('{"hash": "85_0", "iso": "SE", "sql": "SELECT joint_pay(6, 47, 12, 0, 0);"}'); }
step "s1a1430" { SELECT bcdb_tx_submit('{"hash": "85_1", "iso": "SE", "sql": "SELECT simple_pay(8, 11, 0);"}'); }
step "s1a1431" { SELECT bcdb_tx_submit('{"hash": "85_2", "iso": "SE", "sql": "SELECT simple_pay(17, 43, 0);"}'); }
step "s1a1432" { SELECT bcdb_tx_submit('{"hash": "85_3", "iso": "SE", "sql": "SELECT simple_pay(28, 45, 0);"}'); }
step "s1a1433" { SELECT bcdb_tx_submit('{"hash": "85_4", "iso": "SE", "sql": "SELECT simple_pay(6, 48, 0);"}'); }
step "s1a1434" { SELECT bcdb_tx_submit('{"hash": "85_5", "iso": "SE", "sql": "SELECT joint_pay(0, 3, 12, 0, 0);"}'); }
step "s1a1435" { SELECT bcdb_tx_submit('{"hash": "85_6", "iso": "SE", "sql": "SELECT simple_pay(15, 21, 0);"}'); }
step "s1a1436" { SELECT bcdb_tx_submit('{"hash": "85_7", "iso": "SE", "sql": "SELECT simple_pay(37, 7, 0);"}'); }
step "s1a1437" { SELECT bcdb_tx_submit('{"hash": "85_8", "iso": "SE", "sql": "SELECT simple_pay(30, 38, 0);"}'); }
step "s1a1438" { SELECT bcdb_tx_submit('{"hash": "85_9", "iso": "SE", "sql": "SELECT simple_pay(15, 24, 0);"}'); }
step "s1a1439" { SELECT bcdb_tx_submit('{"hash": "85_10", "iso": "SE", "sql": "SELECT simple_pay(3, 22, 0);"}'); }
step "s1a1440" { SELECT bcdb_tx_submit('{"hash": "85_11", "iso": "SE", "sql": "SELECT simple_pay(5, 35, 0);"}'); }
step "s1a1441" { SELECT bcdb_tx_submit('{"hash": "85_12", "iso": "SE", "sql": "SELECT simple_pay(29, 0, 0);"}'); }
step "s1a1442" { SELECT bcdb_tx_submit('{"hash": "85_13", "iso": "SE", "sql": "SELECT simple_pay(39, 40, 0);"}'); }
step "s1a1443" { SELECT bcdb_tx_submit('{"hash": "85_14", "iso": "SE", "sql": "SELECT joint_pay(9, 47, 35, 0, 0);"}'); }
step "s1a1444" { SELECT bcdb_tx_submit('{"hash": "85_15", "iso": "SE", "sql": "SELECT simple_pay(21, 43, 0);"}'); }
step "s1a1445" { SELECT bcdb_block_submit('{"bid": 85, "txs": ["85_0", "85_1", "85_2", "85_3", "85_4", "85_5", "85_6", "85_7", "85_8", "85_9", "85_10", "85_11", "85_12", "85_13", "85_14", "85_15"]}'); }
step "s1a1446" { SELECT bcdb_tx_submit('{"hash": "86_0", "iso": "SE", "sql": "SELECT simple_pay(44, 4, 0);"}'); }
step "s1a1447" { SELECT bcdb_tx_submit('{"hash": "86_1", "iso": "SE", "sql": "SELECT simple_pay(17, 29, 0);"}'); }
step "s1a1448" { SELECT bcdb_tx_submit('{"hash": "86_2", "iso": "SE", "sql": "SELECT simple_pay(25, 1, 0);"}'); }
step "s1a1449" { SELECT bcdb_tx_submit('{"hash": "86_3", "iso": "SE", "sql": "SELECT simple_pay(29, 7, 0);"}'); }
step "s1a1450" { SELECT bcdb_tx_submit('{"hash": "86_4", "iso": "SE", "sql": "SELECT joint_pay(19, 21, 38, 0, 0);"}'); }
step "s1a1451" { SELECT bcdb_tx_submit('{"hash": "86_5", "iso": "SE", "sql": "SELECT joint_pay(28, 0, 38, 0, 0);"}'); }
step "s1a1452" { SELECT bcdb_tx_submit('{"hash": "86_6", "iso": "SE", "sql": "SELECT simple_pay(9, 26, 0);"}'); }
step "s1a1453" { SELECT bcdb_tx_submit('{"hash": "86_7", "iso": "SE", "sql": "SELECT simple_pay(19, 11, 0);"}'); }
step "s1a1454" { SELECT bcdb_tx_submit('{"hash": "86_8", "iso": "SE", "sql": "SELECT simple_pay(10, 5, 0);"}'); }
step "s1a1455" { SELECT bcdb_tx_submit('{"hash": "86_9", "iso": "SE", "sql": "SELECT simple_pay(48, 32, 0);"}'); }
step "s1a1456" { SELECT bcdb_tx_submit('{"hash": "86_10", "iso": "SE", "sql": "SELECT simple_pay(34, 41, 0);"}'); }
step "s1a1457" { SELECT bcdb_tx_submit('{"hash": "86_11", "iso": "SE", "sql": "SELECT simple_pay(26, 21, 0);"}'); }
step "s1a1458" { SELECT bcdb_tx_submit('{"hash": "86_12", "iso": "SE", "sql": "SELECT joint_pay(35, 23, 37, 0, 0);"}'); }
step "s1a1459" { SELECT bcdb_tx_submit('{"hash": "86_13", "iso": "SE", "sql": "SELECT joint_pay(5, 15, 7, 0, 0);"}'); }
step "s1a1460" { SELECT bcdb_tx_submit('{"hash": "86_14", "iso": "SE", "sql": "SELECT simple_pay(45, 41, 0);"}'); }
step "s1a1461" { SELECT bcdb_tx_submit('{"hash": "86_15", "iso": "SE", "sql": "SELECT simple_pay(1, 24, 0);"}'); }
step "s1a1462" { SELECT bcdb_block_submit('{"bid": 86, "txs": ["86_0", "86_1", "86_2", "86_3", "86_4", "86_5", "86_6", "86_7", "86_8", "86_9", "86_10", "86_11", "86_12", "86_13", "86_14", "86_15"]}'); }
step "s1a1463" { SELECT bcdb_tx_submit('{"hash": "87_0", "iso": "SE", "sql": "SELECT simple_pay(22, 37, 0);"}'); }
step "s1a1464" { SELECT bcdb_tx_submit('{"hash": "87_1", "iso": "SE", "sql": "SELECT simple_pay(33, 47, 0);"}'); }
step "s1a1465" { SELECT bcdb_tx_submit('{"hash": "87_2", "iso": "SE", "sql": "SELECT simple_pay(2, 19, 0);"}'); }
step "s1a1466" { SELECT bcdb_tx_submit('{"hash": "87_3", "iso": "SE", "sql": "SELECT simple_pay(27, 14, 0);"}'); }
step "s1a1467" { SELECT bcdb_tx_submit('{"hash": "87_4", "iso": "SE", "sql": "SELECT simple_pay(47, 30, 0);"}'); }
step "s1a1468" { SELECT bcdb_tx_submit('{"hash": "87_5", "iso": "SE", "sql": "SELECT joint_pay(38, 46, 25, 0, 0);"}'); }
step "s1a1469" { SELECT bcdb_tx_submit('{"hash": "87_6", "iso": "SE", "sql": "SELECT simple_pay(21, 13, 0);"}'); }
step "s1a1470" { SELECT bcdb_tx_submit('{"hash": "87_7", "iso": "SE", "sql": "SELECT simple_pay(36, 22, 0);"}'); }
step "s1a1471" { SELECT bcdb_tx_submit('{"hash": "87_8", "iso": "SE", "sql": "SELECT simple_pay(10, 11, 0);"}'); }
step "s1a1472" { SELECT bcdb_tx_submit('{"hash": "87_9", "iso": "SE", "sql": "SELECT simple_pay(17, 12, 0);"}'); }
step "s1a1473" { SELECT bcdb_tx_submit('{"hash": "87_10", "iso": "SE", "sql": "SELECT simple_pay(7, 22, 0);"}'); }
step "s1a1474" { SELECT bcdb_tx_submit('{"hash": "87_11", "iso": "SE", "sql": "SELECT simple_pay(9, 19, 0);"}'); }
step "s1a1475" { SELECT bcdb_tx_submit('{"hash": "87_12", "iso": "SE", "sql": "SELECT simple_pay(45, 39, 0);"}'); }
step "s1a1476" { SELECT bcdb_tx_submit('{"hash": "87_13", "iso": "SE", "sql": "SELECT simple_pay(25, 1, 0);"}'); }
step "s1a1477" { SELECT bcdb_tx_submit('{"hash": "87_14", "iso": "SE", "sql": "SELECT simple_pay(4, 11, 0);"}'); }
step "s1a1478" { SELECT bcdb_tx_submit('{"hash": "87_15", "iso": "SE", "sql": "SELECT simple_pay(26, 5, 0);"}'); }
step "s1a1479" { SELECT bcdb_block_submit('{"bid": 87, "txs": ["87_0", "87_1", "87_2", "87_3", "87_4", "87_5", "87_6", "87_7", "87_8", "87_9", "87_10", "87_11", "87_12", "87_13", "87_14", "87_15"]}'); }
step "s1a1480" { SELECT bcdb_tx_submit('{"hash": "88_0", "iso": "SE", "sql": "SELECT joint_pay(36, 15, 34, 0, 0);"}'); }
step "s1a1481" { SELECT bcdb_tx_submit('{"hash": "88_1", "iso": "SE", "sql": "SELECT joint_pay(20, 47, 28, 0, 0);"}'); }
step "s1a1482" { SELECT bcdb_tx_submit('{"hash": "88_2", "iso": "SE", "sql": "SELECT simple_pay(45, 38, 0);"}'); }
step "s1a1483" { SELECT bcdb_tx_submit('{"hash": "88_3", "iso": "SE", "sql": "SELECT simple_pay(49, 10, 0);"}'); }
step "s1a1484" { SELECT bcdb_tx_submit('{"hash": "88_4", "iso": "SE", "sql": "SELECT simple_pay(10, 49, 0);"}'); }
step "s1a1485" { SELECT bcdb_tx_submit('{"hash": "88_5", "iso": "SE", "sql": "SELECT simple_pay(38, 3, 0);"}'); }
step "s1a1486" { SELECT bcdb_tx_submit('{"hash": "88_6", "iso": "SE", "sql": "SELECT simple_pay(28, 49, 0);"}'); }
step "s1a1487" { SELECT bcdb_tx_submit('{"hash": "88_7", "iso": "SE", "sql": "SELECT simple_pay(34, 3, 0);"}'); }
step "s1a1488" { SELECT bcdb_tx_submit('{"hash": "88_8", "iso": "SE", "sql": "SELECT simple_pay(1, 41, 0);"}'); }
step "s1a1489" { SELECT bcdb_tx_submit('{"hash": "88_9", "iso": "SE", "sql": "SELECT joint_pay(12, 10, 31, 0, 0);"}'); }
step "s1a1490" { SELECT bcdb_tx_submit('{"hash": "88_10", "iso": "SE", "sql": "SELECT simple_pay(12, 33, 0);"}'); }
step "s1a1491" { SELECT bcdb_tx_submit('{"hash": "88_11", "iso": "SE", "sql": "SELECT simple_pay(47, 36, 0);"}'); }
step "s1a1492" { SELECT bcdb_tx_submit('{"hash": "88_12", "iso": "SE", "sql": "SELECT joint_pay(23, 34, 0, 0, 0);"}'); }
step "s1a1493" { SELECT bcdb_tx_submit('{"hash": "88_13", "iso": "SE", "sql": "SELECT simple_pay(39, 21, 0);"}'); }
step "s1a1494" { SELECT bcdb_tx_submit('{"hash": "88_14", "iso": "SE", "sql": "SELECT simple_pay(34, 14, 0);"}'); }
step "s1a1495" { SELECT bcdb_tx_submit('{"hash": "88_15", "iso": "SE", "sql": "SELECT simple_pay(0, 36, 0);"}'); }
step "s1a1496" { SELECT bcdb_block_submit('{"bid": 88, "txs": ["88_0", "88_1", "88_2", "88_3", "88_4", "88_5", "88_6", "88_7", "88_8", "88_9", "88_10", "88_11", "88_12", "88_13", "88_14", "88_15"]}'); }
step "s1a1497" { SELECT bcdb_tx_submit('{"hash": "89_0", "iso": "SE", "sql": "SELECT simple_pay(4, 21, 0);"}'); }
step "s1a1498" { SELECT bcdb_tx_submit('{"hash": "89_1", "iso": "SE", "sql": "SELECT simple_pay(49, 22, 0);"}'); }
step "s1a1499" { SELECT bcdb_tx_submit('{"hash": "89_2", "iso": "SE", "sql": "SELECT simple_pay(19, 36, 0);"}'); }
step "s1a1500" { SELECT bcdb_tx_submit('{"hash": "89_3", "iso": "SE", "sql": "SELECT joint_pay(2, 46, 0, 0, 0);"}'); }
step "s1a1501" { SELECT bcdb_tx_submit('{"hash": "89_4", "iso": "SE", "sql": "SELECT simple_pay(38, 25, 0);"}'); }
step "s1a1502" { SELECT bcdb_tx_submit('{"hash": "89_5", "iso": "SE", "sql": "SELECT joint_pay(14, 27, 36, 0, 0);"}'); }
step "s1a1503" { SELECT bcdb_tx_submit('{"hash": "89_6", "iso": "SE", "sql": "SELECT simple_pay(0, 11, 0);"}'); }
step "s1a1504" { SELECT bcdb_tx_submit('{"hash": "89_7", "iso": "SE", "sql": "SELECT simple_pay(29, 34, 0);"}'); }
step "s1a1505" { SELECT bcdb_tx_submit('{"hash": "89_8", "iso": "SE", "sql": "SELECT joint_pay(49, 0, 42, 0, 0);"}'); }
step "s1a1506" { SELECT bcdb_tx_submit('{"hash": "89_9", "iso": "SE", "sql": "SELECT joint_pay(5, 8, 25, 0, 0);"}'); }
step "s1a1507" { SELECT bcdb_tx_submit('{"hash": "89_10", "iso": "SE", "sql": "SELECT simple_pay(11, 46, 0);"}'); }
step "s1a1508" { SELECT bcdb_tx_submit('{"hash": "89_11", "iso": "SE", "sql": "SELECT simple_pay(35, 6, 0);"}'); }
step "s1a1509" { SELECT bcdb_tx_submit('{"hash": "89_12", "iso": "SE", "sql": "SELECT joint_pay(2, 25, 18, 0, 0);"}'); }
step "s1a1510" { SELECT bcdb_tx_submit('{"hash": "89_13", "iso": "SE", "sql": "SELECT joint_pay(24, 1, 42, 0, 0);"}'); }
step "s1a1511" { SELECT bcdb_tx_submit('{"hash": "89_14", "iso": "SE", "sql": "SELECT simple_pay(26, 33, 0);"}'); }
step "s1a1512" { SELECT bcdb_tx_submit('{"hash": "89_15", "iso": "SE", "sql": "SELECT simple_pay(32, 22, 0);"}'); }
step "s1a1513" { SELECT bcdb_block_submit('{"bid": 89, "txs": ["89_0", "89_1", "89_2", "89_3", "89_4", "89_5", "89_6", "89_7", "89_8", "89_9", "89_10", "89_11", "89_12", "89_13", "89_14", "89_15"]}'); }
step "s1a1514" { SELECT bcdb_tx_submit('{"hash": "90_0", "iso": "SE", "sql": "SELECT simple_pay(43, 2, 0);"}'); }
step "s1a1515" { SELECT bcdb_tx_submit('{"hash": "90_1", "iso": "SE", "sql": "SELECT simple_pay(32, 40, 0);"}'); }
step "s1a1516" { SELECT bcdb_tx_submit('{"hash": "90_2", "iso": "SE", "sql": "SELECT joint_pay(12, 21, 29, 0, 0);"}'); }
step "s1a1517" { SELECT bcdb_tx_submit('{"hash": "90_3", "iso": "SE", "sql": "SELECT simple_pay(36, 12, 0);"}'); }
step "s1a1518" { SELECT bcdb_tx_submit('{"hash": "90_4", "iso": "SE", "sql": "SELECT simple_pay(12, 7, 0);"}'); }
step "s1a1519" { SELECT bcdb_tx_submit('{"hash": "90_5", "iso": "SE", "sql": "SELECT simple_pay(20, 21, 0);"}'); }
step "s1a1520" { SELECT bcdb_tx_submit('{"hash": "90_6", "iso": "SE", "sql": "SELECT simple_pay(9, 11, 0);"}'); }
step "s1a1521" { SELECT bcdb_tx_submit('{"hash": "90_7", "iso": "SE", "sql": "SELECT simple_pay(26, 17, 0);"}'); }
step "s1a1522" { SELECT bcdb_tx_submit('{"hash": "90_8", "iso": "SE", "sql": "SELECT joint_pay(24, 7, 48, 0, 0);"}'); }
step "s1a1523" { SELECT bcdb_tx_submit('{"hash": "90_9", "iso": "SE", "sql": "SELECT simple_pay(31, 10, 0);"}'); }
step "s1a1524" { SELECT bcdb_tx_submit('{"hash": "90_10", "iso": "SE", "sql": "SELECT simple_pay(14, 26, 0);"}'); }
step "s1a1525" { SELECT bcdb_tx_submit('{"hash": "90_11", "iso": "SE", "sql": "SELECT simple_pay(8, 35, 0);"}'); }
step "s1a1526" { SELECT bcdb_tx_submit('{"hash": "90_12", "iso": "SE", "sql": "SELECT simple_pay(39, 44, 0);"}'); }
step "s1a1527" { SELECT bcdb_tx_submit('{"hash": "90_13", "iso": "SE", "sql": "SELECT simple_pay(2, 41, 0);"}'); }
step "s1a1528" { SELECT bcdb_tx_submit('{"hash": "90_14", "iso": "SE", "sql": "SELECT simple_pay(14, 13, 0);"}'); }
step "s1a1529" { SELECT bcdb_tx_submit('{"hash": "90_15", "iso": "SE", "sql": "SELECT simple_pay(31, 14, 0);"}'); }
step "s1a1530" { SELECT bcdb_block_submit('{"bid": 90, "txs": ["90_0", "90_1", "90_2", "90_3", "90_4", "90_5", "90_6", "90_7", "90_8", "90_9", "90_10", "90_11", "90_12", "90_13", "90_14", "90_15"]}'); }
step "s1a1531" { SELECT bcdb_tx_submit('{"hash": "91_0", "iso": "SE", "sql": "SELECT simple_pay(5, 34, 0);"}'); }
step "s1a1532" { SELECT bcdb_tx_submit('{"hash": "91_1", "iso": "SE", "sql": "SELECT joint_pay(10, 19, 1, 0, 0);"}'); }
step "s1a1533" { SELECT bcdb_tx_submit('{"hash": "91_2", "iso": "SE", "sql": "SELECT simple_pay(8, 39, 0);"}'); }
step "s1a1534" { SELECT bcdb_tx_submit('{"hash": "91_3", "iso": "SE", "sql": "SELECT simple_pay(33, 39, 0);"}'); }
step "s1a1535" { SELECT bcdb_tx_submit('{"hash": "91_4", "iso": "SE", "sql": "SELECT simple_pay(34, 26, 0);"}'); }
step "s1a1536" { SELECT bcdb_tx_submit('{"hash": "91_5", "iso": "SE", "sql": "SELECT simple_pay(48, 23, 0);"}'); }
step "s1a1537" { SELECT bcdb_tx_submit('{"hash": "91_6", "iso": "SE", "sql": "SELECT joint_pay(32, 13, 45, 0, 0);"}'); }
step "s1a1538" { SELECT bcdb_tx_submit('{"hash": "91_7", "iso": "SE", "sql": "SELECT simple_pay(39, 17, 0);"}'); }
step "s1a1539" { SELECT bcdb_tx_submit('{"hash": "91_8", "iso": "SE", "sql": "SELECT simple_pay(49, 3, 0);"}'); }
step "s1a1540" { SELECT bcdb_tx_submit('{"hash": "91_9", "iso": "SE", "sql": "SELECT simple_pay(37, 17, 0);"}'); }
step "s1a1541" { SELECT bcdb_tx_submit('{"hash": "91_10", "iso": "SE", "sql": "SELECT joint_pay(42, 6, 44, 0, 0);"}'); }
step "s1a1542" { SELECT bcdb_tx_submit('{"hash": "91_11", "iso": "SE", "sql": "SELECT simple_pay(31, 23, 0);"}'); }
step "s1a1543" { SELECT bcdb_tx_submit('{"hash": "91_12", "iso": "SE", "sql": "SELECT simple_pay(3, 16, 0);"}'); }
step "s1a1544" { SELECT bcdb_tx_submit('{"hash": "91_13", "iso": "SE", "sql": "SELECT simple_pay(22, 18, 0);"}'); }
step "s1a1545" { SELECT bcdb_tx_submit('{"hash": "91_14", "iso": "SE", "sql": "SELECT joint_pay(21, 14, 15, 0, 0);"}'); }
step "s1a1546" { SELECT bcdb_tx_submit('{"hash": "91_15", "iso": "SE", "sql": "SELECT simple_pay(12, 43, 0);"}'); }
step "s1a1547" { SELECT bcdb_block_submit('{"bid": 91, "txs": ["91_0", "91_1", "91_2", "91_3", "91_4", "91_5", "91_6", "91_7", "91_8", "91_9", "91_10", "91_11", "91_12", "91_13", "91_14", "91_15"]}'); }
step "s1a1548" { SELECT bcdb_tx_submit('{"hash": "92_0", "iso": "SE", "sql": "SELECT simple_pay(34, 16, 0);"}'); }
step "s1a1549" { SELECT bcdb_tx_submit('{"hash": "92_1", "iso": "SE", "sql": "SELECT simple_pay(22, 25, 0);"}'); }
step "s1a1550" { SELECT bcdb_tx_submit('{"hash": "92_2", "iso": "SE", "sql": "SELECT joint_pay(34, 42, 2, 0, 0);"}'); }
step "s1a1551" { SELECT bcdb_tx_submit('{"hash": "92_3", "iso": "SE", "sql": "SELECT simple_pay(43, 7, 0);"}'); }
step "s1a1552" { SELECT bcdb_tx_submit('{"hash": "92_4", "iso": "SE", "sql": "SELECT simple_pay(45, 12, 0);"}'); }
step "s1a1553" { SELECT bcdb_tx_submit('{"hash": "92_5", "iso": "SE", "sql": "SELECT simple_pay(47, 5, 0);"}'); }
step "s1a1554" { SELECT bcdb_tx_submit('{"hash": "92_6", "iso": "SE", "sql": "SELECT simple_pay(6, 32, 0);"}'); }
step "s1a1555" { SELECT bcdb_tx_submit('{"hash": "92_7", "iso": "SE", "sql": "SELECT simple_pay(43, 35, 0);"}'); }
step "s1a1556" { SELECT bcdb_tx_submit('{"hash": "92_8", "iso": "SE", "sql": "SELECT simple_pay(9, 7, 0);"}'); }
step "s1a1557" { SELECT bcdb_tx_submit('{"hash": "92_9", "iso": "SE", "sql": "SELECT simple_pay(47, 48, 0);"}'); }
step "s1a1558" { SELECT bcdb_tx_submit('{"hash": "92_10", "iso": "SE", "sql": "SELECT simple_pay(31, 18, 0);"}'); }
step "s1a1559" { SELECT bcdb_tx_submit('{"hash": "92_11", "iso": "SE", "sql": "SELECT simple_pay(34, 37, 0);"}'); }
step "s1a1560" { SELECT bcdb_tx_submit('{"hash": "92_12", "iso": "SE", "sql": "SELECT simple_pay(4, 30, 0);"}'); }
step "s1a1561" { SELECT bcdb_tx_submit('{"hash": "92_13", "iso": "SE", "sql": "SELECT simple_pay(22, 27, 0);"}'); }
step "s1a1562" { SELECT bcdb_tx_submit('{"hash": "92_14", "iso": "SE", "sql": "SELECT simple_pay(20, 6, 0);"}'); }
step "s1a1563" { SELECT bcdb_tx_submit('{"hash": "92_15", "iso": "SE", "sql": "SELECT simple_pay(8, 29, 0);"}'); }
step "s1a1564" { SELECT bcdb_block_submit('{"bid": 92, "txs": ["92_0", "92_1", "92_2", "92_3", "92_4", "92_5", "92_6", "92_7", "92_8", "92_9", "92_10", "92_11", "92_12", "92_13", "92_14", "92_15"]}'); }
step "s1a1565" { SELECT bcdb_tx_submit('{"hash": "93_0", "iso": "SE", "sql": "SELECT simple_pay(22, 32, 0);"}'); }
step "s1a1566" { SELECT bcdb_tx_submit('{"hash": "93_1", "iso": "SE", "sql": "SELECT joint_pay(49, 29, 25, 0, 0);"}'); }
step "s1a1567" { SELECT bcdb_tx_submit('{"hash": "93_2", "iso": "SE", "sql": "SELECT simple_pay(20, 39, 0);"}'); }
step "s1a1568" { SELECT bcdb_tx_submit('{"hash": "93_3", "iso": "SE", "sql": "SELECT simple_pay(9, 18, 0);"}'); }
step "s1a1569" { SELECT bcdb_tx_submit('{"hash": "93_4", "iso": "SE", "sql": "SELECT joint_pay(44, 4, 29, 0, 0);"}'); }
step "s1a1570" { SELECT bcdb_tx_submit('{"hash": "93_5", "iso": "SE", "sql": "SELECT simple_pay(4, 48, 0);"}'); }
step "s1a1571" { SELECT bcdb_tx_submit('{"hash": "93_6", "iso": "SE", "sql": "SELECT joint_pay(25, 14, 18, 0, 0);"}'); }
step "s1a1572" { SELECT bcdb_tx_submit('{"hash": "93_7", "iso": "SE", "sql": "SELECT simple_pay(27, 40, 0);"}'); }
step "s1a1573" { SELECT bcdb_tx_submit('{"hash": "93_8", "iso": "SE", "sql": "SELECT simple_pay(18, 34, 0);"}'); }
step "s1a1574" { SELECT bcdb_tx_submit('{"hash": "93_9", "iso": "SE", "sql": "SELECT simple_pay(36, 3, 0);"}'); }
step "s1a1575" { SELECT bcdb_tx_submit('{"hash": "93_10", "iso": "SE", "sql": "SELECT simple_pay(47, 26, 0);"}'); }
step "s1a1576" { SELECT bcdb_tx_submit('{"hash": "93_11", "iso": "SE", "sql": "SELECT simple_pay(14, 49, 0);"}'); }
step "s1a1577" { SELECT bcdb_tx_submit('{"hash": "93_12", "iso": "SE", "sql": "SELECT simple_pay(41, 6, 0);"}'); }
step "s1a1578" { SELECT bcdb_tx_submit('{"hash": "93_13", "iso": "SE", "sql": "SELECT simple_pay(34, 38, 0);"}'); }
step "s1a1579" { SELECT bcdb_tx_submit('{"hash": "93_14", "iso": "SE", "sql": "SELECT joint_pay(22, 31, 32, 0, 0);"}'); }
step "s1a1580" { SELECT bcdb_tx_submit('{"hash": "93_15", "iso": "SE", "sql": "SELECT simple_pay(49, 9, 0);"}'); }
step "s1a1581" { SELECT bcdb_block_submit('{"bid": 93, "txs": ["93_0", "93_1", "93_2", "93_3", "93_4", "93_5", "93_6", "93_7", "93_8", "93_9", "93_10", "93_11", "93_12", "93_13", "93_14", "93_15"]}'); }
step "s1a1582" { SELECT bcdb_tx_submit('{"hash": "94_0", "iso": "SE", "sql": "SELECT simple_pay(38, 11, 0);"}'); }
step "s1a1583" { SELECT bcdb_tx_submit('{"hash": "94_1", "iso": "SE", "sql": "SELECT simple_pay(11, 48, 0);"}'); }
step "s1a1584" { SELECT bcdb_tx_submit('{"hash": "94_2", "iso": "SE", "sql": "SELECT simple_pay(1, 21, 0);"}'); }
step "s1a1585" { SELECT bcdb_tx_submit('{"hash": "94_3", "iso": "SE", "sql": "SELECT joint_pay(32, 20, 38, 0, 0);"}'); }
step "s1a1586" { SELECT bcdb_tx_submit('{"hash": "94_4", "iso": "SE", "sql": "SELECT simple_pay(6, 47, 0);"}'); }
step "s1a1587" { SELECT bcdb_tx_submit('{"hash": "94_5", "iso": "SE", "sql": "SELECT simple_pay(35, 6, 0);"}'); }
step "s1a1588" { SELECT bcdb_tx_submit('{"hash": "94_6", "iso": "SE", "sql": "SELECT simple_pay(30, 33, 0);"}'); }
step "s1a1589" { SELECT bcdb_tx_submit('{"hash": "94_7", "iso": "SE", "sql": "SELECT simple_pay(31, 18, 0);"}'); }
step "s1a1590" { SELECT bcdb_tx_submit('{"hash": "94_8", "iso": "SE", "sql": "SELECT simple_pay(39, 5, 0);"}'); }
step "s1a1591" { SELECT bcdb_tx_submit('{"hash": "94_9", "iso": "SE", "sql": "SELECT simple_pay(40, 25, 0);"}'); }
step "s1a1592" { SELECT bcdb_tx_submit('{"hash": "94_10", "iso": "SE", "sql": "SELECT simple_pay(45, 21, 0);"}'); }
step "s1a1593" { SELECT bcdb_tx_submit('{"hash": "94_11", "iso": "SE", "sql": "SELECT simple_pay(37, 21, 0);"}'); }
step "s1a1594" { SELECT bcdb_tx_submit('{"hash": "94_12", "iso": "SE", "sql": "SELECT simple_pay(47, 44, 0);"}'); }
step "s1a1595" { SELECT bcdb_tx_submit('{"hash": "94_13", "iso": "SE", "sql": "SELECT simple_pay(28, 8, 0);"}'); }
step "s1a1596" { SELECT bcdb_tx_submit('{"hash": "94_14", "iso": "SE", "sql": "SELECT joint_pay(6, 28, 45, 0, 0);"}'); }
step "s1a1597" { SELECT bcdb_tx_submit('{"hash": "94_15", "iso": "SE", "sql": "SELECT simple_pay(48, 21, 0);"}'); }
step "s1a1598" { SELECT bcdb_block_submit('{"bid": 94, "txs": ["94_0", "94_1", "94_2", "94_3", "94_4", "94_5", "94_6", "94_7", "94_8", "94_9", "94_10", "94_11", "94_12", "94_13", "94_14", "94_15"]}'); }
step "s1a1599" { SELECT bcdb_tx_submit('{"hash": "95_0", "iso": "SE", "sql": "SELECT simple_pay(1, 21, 0);"}'); }
step "s1a1600" { SELECT bcdb_tx_submit('{"hash": "95_1", "iso": "SE", "sql": "SELECT simple_pay(40, 15, 0);"}'); }
step "s1a1601" { SELECT bcdb_tx_submit('{"hash": "95_2", "iso": "SE", "sql": "SELECT simple_pay(46, 23, 0);"}'); }
step "s1a1602" { SELECT bcdb_tx_submit('{"hash": "95_3", "iso": "SE", "sql": "SELECT simple_pay(45, 24, 0);"}'); }
step "s1a1603" { SELECT bcdb_tx_submit('{"hash": "95_4", "iso": "SE", "sql": "SELECT simple_pay(25, 40, 0);"}'); }
step "s1a1604" { SELECT bcdb_tx_submit('{"hash": "95_5", "iso": "SE", "sql": "SELECT simple_pay(19, 25, 0);"}'); }
step "s1a1605" { SELECT bcdb_tx_submit('{"hash": "95_6", "iso": "SE", "sql": "SELECT simple_pay(1, 34, 0);"}'); }
step "s1a1606" { SELECT bcdb_tx_submit('{"hash": "95_7", "iso": "SE", "sql": "SELECT simple_pay(7, 20, 0);"}'); }
step "s1a1607" { SELECT bcdb_tx_submit('{"hash": "95_8", "iso": "SE", "sql": "SELECT joint_pay(9, 5, 8, 0, 0);"}'); }
step "s1a1608" { SELECT bcdb_tx_submit('{"hash": "95_9", "iso": "SE", "sql": "SELECT joint_pay(35, 18, 12, 0, 0);"}'); }
step "s1a1609" { SELECT bcdb_tx_submit('{"hash": "95_10", "iso": "SE", "sql": "SELECT simple_pay(23, 15, 0);"}'); }
step "s1a1610" { SELECT bcdb_tx_submit('{"hash": "95_11", "iso": "SE", "sql": "SELECT simple_pay(5, 48, 0);"}'); }
step "s1a1611" { SELECT bcdb_tx_submit('{"hash": "95_12", "iso": "SE", "sql": "SELECT simple_pay(27, 20, 0);"}'); }
step "s1a1612" { SELECT bcdb_tx_submit('{"hash": "95_13", "iso": "SE", "sql": "SELECT simple_pay(44, 40, 0);"}'); }
step "s1a1613" { SELECT bcdb_tx_submit('{"hash": "95_14", "iso": "SE", "sql": "SELECT simple_pay(4, 29, 0);"}'); }
step "s1a1614" { SELECT bcdb_tx_submit('{"hash": "95_15", "iso": "SE", "sql": "SELECT simple_pay(24, 13, 0);"}'); }
step "s1a1615" { SELECT bcdb_block_submit('{"bid": 95, "txs": ["95_0", "95_1", "95_2", "95_3", "95_4", "95_5", "95_6", "95_7", "95_8", "95_9", "95_10", "95_11", "95_12", "95_13", "95_14", "95_15"]}'); }
step "s1a1616" { SELECT bcdb_tx_submit('{"hash": "96_0", "iso": "SE", "sql": "SELECT joint_pay(28, 0, 10, 0, 0);"}'); }
step "s1a1617" { SELECT bcdb_tx_submit('{"hash": "96_1", "iso": "SE", "sql": "SELECT simple_pay(10, 36, 0);"}'); }
step "s1a1618" { SELECT bcdb_tx_submit('{"hash": "96_2", "iso": "SE", "sql": "SELECT simple_pay(3, 5, 0);"}'); }
step "s1a1619" { SELECT bcdb_tx_submit('{"hash": "96_3", "iso": "SE", "sql": "SELECT simple_pay(3, 42, 0);"}'); }
step "s1a1620" { SELECT bcdb_tx_submit('{"hash": "96_4", "iso": "SE", "sql": "SELECT simple_pay(14, 31, 0);"}'); }
step "s1a1621" { SELECT bcdb_tx_submit('{"hash": "96_5", "iso": "SE", "sql": "SELECT simple_pay(36, 23, 0);"}'); }
step "s1a1622" { SELECT bcdb_tx_submit('{"hash": "96_6", "iso": "SE", "sql": "SELECT simple_pay(34, 20, 0);"}'); }
step "s1a1623" { SELECT bcdb_tx_submit('{"hash": "96_7", "iso": "SE", "sql": "SELECT simple_pay(49, 44, 0);"}'); }
step "s1a1624" { SELECT bcdb_tx_submit('{"hash": "96_8", "iso": "SE", "sql": "SELECT simple_pay(39, 32, 0);"}'); }
step "s1a1625" { SELECT bcdb_tx_submit('{"hash": "96_9", "iso": "SE", "sql": "SELECT simple_pay(49, 3, 0);"}'); }
step "s1a1626" { SELECT bcdb_tx_submit('{"hash": "96_10", "iso": "SE", "sql": "SELECT simple_pay(47, 13, 0);"}'); }
step "s1a1627" { SELECT bcdb_tx_submit('{"hash": "96_11", "iso": "SE", "sql": "SELECT simple_pay(6, 8, 0);"}'); }
step "s1a1628" { SELECT bcdb_tx_submit('{"hash": "96_12", "iso": "SE", "sql": "SELECT joint_pay(38, 35, 5, 0, 0);"}'); }
step "s1a1629" { SELECT bcdb_tx_submit('{"hash": "96_13", "iso": "SE", "sql": "SELECT simple_pay(46, 39, 0);"}'); }
step "s1a1630" { SELECT bcdb_tx_submit('{"hash": "96_14", "iso": "SE", "sql": "SELECT simple_pay(41, 28, 0);"}'); }
step "s1a1631" { SELECT bcdb_tx_submit('{"hash": "96_15", "iso": "SE", "sql": "SELECT simple_pay(47, 39, 0);"}'); }
step "s1a1632" { SELECT bcdb_block_submit('{"bid": 96, "txs": ["96_0", "96_1", "96_2", "96_3", "96_4", "96_5", "96_6", "96_7", "96_8", "96_9", "96_10", "96_11", "96_12", "96_13", "96_14", "96_15"]}'); }
step "s1a1633" { SELECT bcdb_tx_submit('{"hash": "97_0", "iso": "SE", "sql": "SELECT simple_pay(33, 40, 0);"}'); }
step "s1a1634" { SELECT bcdb_tx_submit('{"hash": "97_1", "iso": "SE", "sql": "SELECT simple_pay(20, 45, 0);"}'); }
step "s1a1635" { SELECT bcdb_tx_submit('{"hash": "97_2", "iso": "SE", "sql": "SELECT simple_pay(8, 39, 0);"}'); }
step "s1a1636" { SELECT bcdb_tx_submit('{"hash": "97_3", "iso": "SE", "sql": "SELECT simple_pay(18, 43, 0);"}'); }
step "s1a1637" { SELECT bcdb_tx_submit('{"hash": "97_4", "iso": "SE", "sql": "SELECT simple_pay(33, 48, 0);"}'); }
step "s1a1638" { SELECT bcdb_tx_submit('{"hash": "97_5", "iso": "SE", "sql": "SELECT joint_pay(36, 15, 25, 0, 0);"}'); }
step "s1a1639" { SELECT bcdb_tx_submit('{"hash": "97_6", "iso": "SE", "sql": "SELECT simple_pay(42, 19, 0);"}'); }
step "s1a1640" { SELECT bcdb_tx_submit('{"hash": "97_7", "iso": "SE", "sql": "SELECT simple_pay(20, 36, 0);"}'); }
step "s1a1641" { SELECT bcdb_tx_submit('{"hash": "97_8", "iso": "SE", "sql": "SELECT simple_pay(16, 44, 0);"}'); }
step "s1a1642" { SELECT bcdb_tx_submit('{"hash": "97_9", "iso": "SE", "sql": "SELECT simple_pay(28, 6, 0);"}'); }
step "s1a1643" { SELECT bcdb_tx_submit('{"hash": "97_10", "iso": "SE", "sql": "SELECT simple_pay(19, 20, 0);"}'); }
step "s1a1644" { SELECT bcdb_tx_submit('{"hash": "97_11", "iso": "SE", "sql": "SELECT simple_pay(45, 27, 0);"}'); }
step "s1a1645" { SELECT bcdb_tx_submit('{"hash": "97_12", "iso": "SE", "sql": "SELECT simple_pay(47, 0, 0);"}'); }
step "s1a1646" { SELECT bcdb_tx_submit('{"hash": "97_13", "iso": "SE", "sql": "SELECT simple_pay(45, 21, 0);"}'); }
step "s1a1647" { SELECT bcdb_tx_submit('{"hash": "97_14", "iso": "SE", "sql": "SELECT simple_pay(6, 35, 0);"}'); }
step "s1a1648" { SELECT bcdb_tx_submit('{"hash": "97_15", "iso": "SE", "sql": "SELECT joint_pay(43, 42, 0, 0, 0);"}'); }
step "s1a1649" { SELECT bcdb_block_submit('{"bid": 97, "txs": ["97_0", "97_1", "97_2", "97_3", "97_4", "97_5", "97_6", "97_7", "97_8", "97_9", "97_10", "97_11", "97_12", "97_13", "97_14", "97_15"]}'); }
step "s1a1650" { SELECT bcdb_tx_submit('{"hash": "98_0", "iso": "SE", "sql": "SELECT simple_pay(1, 19, 0);"}'); }
step "s1a1651" { SELECT bcdb_tx_submit('{"hash": "98_1", "iso": "SE", "sql": "SELECT simple_pay(7, 33, 0);"}'); }
step "s1a1652" { SELECT bcdb_tx_submit('{"hash": "98_2", "iso": "SE", "sql": "SELECT simple_pay(1, 31, 0);"}'); }
step "s1a1653" { SELECT bcdb_tx_submit('{"hash": "98_3", "iso": "SE", "sql": "SELECT simple_pay(17, 32, 0);"}'); }
step "s1a1654" { SELECT bcdb_tx_submit('{"hash": "98_4", "iso": "SE", "sql": "SELECT simple_pay(16, 12, 0);"}'); }
step "s1a1655" { SELECT bcdb_tx_submit('{"hash": "98_5", "iso": "SE", "sql": "SELECT simple_pay(25, 38, 0);"}'); }
step "s1a1656" { SELECT bcdb_tx_submit('{"hash": "98_6", "iso": "SE", "sql": "SELECT simple_pay(30, 19, 0);"}'); }
step "s1a1657" { SELECT bcdb_tx_submit('{"hash": "98_7", "iso": "SE", "sql": "SELECT simple_pay(48, 36, 0);"}'); }
step "s1a1658" { SELECT bcdb_tx_submit('{"hash": "98_8", "iso": "SE", "sql": "SELECT simple_pay(38, 49, 0);"}'); }
step "s1a1659" { SELECT bcdb_tx_submit('{"hash": "98_9", "iso": "SE", "sql": "SELECT simple_pay(21, 44, 0);"}'); }
step "s1a1660" { SELECT bcdb_tx_submit('{"hash": "98_10", "iso": "SE", "sql": "SELECT joint_pay(24, 29, 16, 0, 0);"}'); }
step "s1a1661" { SELECT bcdb_tx_submit('{"hash": "98_11", "iso": "SE", "sql": "SELECT simple_pay(17, 39, 0);"}'); }
step "s1a1662" { SELECT bcdb_tx_submit('{"hash": "98_12", "iso": "SE", "sql": "SELECT simple_pay(47, 49, 0);"}'); }
step "s1a1663" { SELECT bcdb_tx_submit('{"hash": "98_13", "iso": "SE", "sql": "SELECT simple_pay(11, 35, 0);"}'); }
step "s1a1664" { SELECT bcdb_tx_submit('{"hash": "98_14", "iso": "SE", "sql": "SELECT simple_pay(29, 16, 0);"}'); }
step "s1a1665" { SELECT bcdb_tx_submit('{"hash": "98_15", "iso": "SE", "sql": "SELECT simple_pay(5, 43, 0);"}'); }
step "s1a1666" { SELECT bcdb_block_submit('{"bid": 98, "txs": ["98_0", "98_1", "98_2", "98_3", "98_4", "98_5", "98_6", "98_7", "98_8", "98_9", "98_10", "98_11", "98_12", "98_13", "98_14", "98_15"]}'); }
step "s1a1667" { SELECT bcdb_tx_submit('{"hash": "99_0", "iso": "SE", "sql": "SELECT simple_pay(35, 3, 0);"}'); }
step "s1a1668" { SELECT bcdb_tx_submit('{"hash": "99_1", "iso": "SE", "sql": "SELECT simple_pay(23, 21, 0);"}'); }
step "s1a1669" { SELECT bcdb_tx_submit('{"hash": "99_2", "iso": "SE", "sql": "SELECT simple_pay(24, 42, 0);"}'); }
step "s1a1670" { SELECT bcdb_tx_submit('{"hash": "99_3", "iso": "SE", "sql": "SELECT simple_pay(18, 30, 0);"}'); }
step "s1a1671" { SELECT bcdb_tx_submit('{"hash": "99_4", "iso": "SE", "sql": "SELECT joint_pay(32, 19, 20, 0, 0);"}'); }
step "s1a1672" { SELECT bcdb_tx_submit('{"hash": "99_5", "iso": "SE", "sql": "SELECT simple_pay(48, 39, 0);"}'); }
step "s1a1673" { SELECT bcdb_tx_submit('{"hash": "99_6", "iso": "SE", "sql": "SELECT simple_pay(4, 22, 0);"}'); }
step "s1a1674" { SELECT bcdb_tx_submit('{"hash": "99_7", "iso": "SE", "sql": "SELECT simple_pay(28, 39, 0);"}'); }
step "s1a1675" { SELECT bcdb_tx_submit('{"hash": "99_8", "iso": "SE", "sql": "SELECT joint_pay(39, 18, 44, 0, 0);"}'); }
step "s1a1676" { SELECT bcdb_tx_submit('{"hash": "99_9", "iso": "SE", "sql": "SELECT simple_pay(0, 28, 0);"}'); }
step "s1a1677" { SELECT bcdb_tx_submit('{"hash": "99_10", "iso": "SE", "sql": "SELECT joint_pay(22, 14, 7, 0, 0);"}'); }
step "s1a1678" { SELECT bcdb_tx_submit('{"hash": "99_11", "iso": "SE", "sql": "SELECT simple_pay(3, 24, 0);"}'); }
step "s1a1679" { SELECT bcdb_tx_submit('{"hash": "99_12", "iso": "SE", "sql": "SELECT simple_pay(24, 41, 0);"}'); }
step "s1a1680" { SELECT bcdb_tx_submit('{"hash": "99_13", "iso": "SE", "sql": "SELECT simple_pay(2, 20, 0);"}'); }
step "s1a1681" { SELECT bcdb_tx_submit('{"hash": "99_14", "iso": "SE", "sql": "SELECT joint_pay(0, 29, 16, 0, 0);"}'); }
step "s1a1682" { SELECT bcdb_tx_submit('{"hash": "99_15", "iso": "SE", "sql": "SELECT simple_pay(11, 29, 0);"}'); }
step "s1a1683" { SELECT bcdb_block_submit('{"bid": 99, "txs": ["99_0", "99_1", "99_2", "99_3", "99_4", "99_5", "99_6", "99_7", "99_8", "99_9", "99_10", "99_11", "99_12", "99_13", "99_14", "99_15"]}'); }
step "s1a1684" { SELECT bcdb_tx_submit('{"hash": "100_0", "iso": "SE", "sql": "SELECT joint_pay(49, 47, 25, 0, 0);"}'); }
step "s1a1685" { SELECT bcdb_tx_submit('{"hash": "100_1", "iso": "SE", "sql": "SELECT simple_pay(16, 6, 0);"}'); }
step "s1a1686" { SELECT bcdb_tx_submit('{"hash": "100_2", "iso": "SE", "sql": "SELECT joint_pay(0, 16, 27, 0, 0);"}'); }
step "s1a1687" { SELECT bcdb_tx_submit('{"hash": "100_3", "iso": "SE", "sql": "SELECT simple_pay(49, 37, 0);"}'); }
step "s1a1688" { SELECT bcdb_tx_submit('{"hash": "100_4", "iso": "SE", "sql": "SELECT simple_pay(4, 21, 0);"}'); }
step "s1a1689" { SELECT bcdb_tx_submit('{"hash": "100_5", "iso": "SE", "sql": "SELECT simple_pay(21, 16, 0);"}'); }
step "s1a1690" { SELECT bcdb_tx_submit('{"hash": "100_6", "iso": "SE", "sql": "SELECT simple_pay(3, 47, 0);"}'); }
step "s1a1691" { SELECT bcdb_tx_submit('{"hash": "100_7", "iso": "SE", "sql": "SELECT simple_pay(28, 33, 0);"}'); }
step "s1a1692" { SELECT bcdb_tx_submit('{"hash": "100_8", "iso": "SE", "sql": "SELECT simple_pay(43, 24, 0);"}'); }
step "s1a1693" { SELECT bcdb_tx_submit('{"hash": "100_9", "iso": "SE", "sql": "SELECT simple_pay(33, 12, 0);"}'); }
step "s1a1694" { SELECT bcdb_tx_submit('{"hash": "100_10", "iso": "SE", "sql": "SELECT simple_pay(7, 35, 0);"}'); }
step "s1a1695" { SELECT bcdb_tx_submit('{"hash": "100_11", "iso": "SE", "sql": "SELECT simple_pay(46, 34, 0);"}'); }
step "s1a1696" { SELECT bcdb_tx_submit('{"hash": "100_12", "iso": "SE", "sql": "SELECT simple_pay(9, 45, 0);"}'); }
step "s1a1697" { SELECT bcdb_tx_submit('{"hash": "100_13", "iso": "SE", "sql": "SELECT simple_pay(31, 34, 0);"}'); }
step "s1a1698" { SELECT bcdb_tx_submit('{"hash": "100_14", "iso": "SE", "sql": "SELECT simple_pay(11, 28, 0);"}'); }
step "s1a1699" { SELECT bcdb_tx_submit('{"hash": "100_15", "iso": "SE", "sql": "SELECT simple_pay(2, 23, 0);"}'); }
step "s1a1700" { SELECT bcdb_block_submit('{"bid": 100, "txs": ["100_0", "100_1", "100_2", "100_3", "100_4", "100_5", "100_6", "100_7", "100_8", "100_9", "100_10", "100_11", "100_12", "100_13", "100_14", "100_15"]}'); }
step "s1a1701" { SELECT bcdb_wait_to_finish(); }
step "s1a1702" { SELECT bcdb_check_block_status(99); }
step "s1a1703" { SELECT bcdb_num_committed(); }
step "s1a1705" { SELECT * FROM bank ORDER BY account; SELECT sum(balance) FROM bank; }
permutation "s1a0" "s1a1" "s1a2" "s1a3" "s1a4" "s1a5" "s1a6" "s1a7" "s1a8" "s1a9" "s1a10" "s1a11" "s1a12" "s1a13" "s1a14" "s1a15" "s1a16" "s1a17" "s1a18" "s1a19" "s1a20" "s1a21" "s1a22" "s1a23" "s1a24" "s1a25" "s1a26" "s1a27" "s1a28" "s1a29" "s1a30" "s1a31" "s1a32" "s1a33" "s1a34" "s1a35" "s1a36" "s1a37" "s1a38" "s1a39" "s1a40" "s1a41" "s1a42" "s1a43" "s1a44" "s1a45" "s1a46" "s1a47" "s1a48" "s1a49" "s1a50" "s1a51" "s1a52" "s1a53" "s1a54" "s1a55" "s1a56" "s1a57" "s1a58" "s1a59" "s1a60" "s1a61" "s1a62" "s1a63" "s1a64" "s1a65" "s1a66" "s1a67" "s1a68" "s1a69" "s1a70" "s1a71" "s1a72" "s1a73" "s1a74" "s1a75" "s1a76" "s1a77" "s1a78" "s1a79" "s1a80" "s1a81" "s1a82" "s1a83" "s1a84" "s1a85" "s1a86" "s1a87" "s1a88" "s1a89" "s1a90" "s1a91" "s1a92" "s1a93" "s1a94" "s1a95" "s1a96" "s1a97" "s1a98" "s1a99" "s1a100" "s1a101" "s1a102" "s1a103" "s1a104" "s1a105" "s1a106" "s1a107" "s1a108" "s1a109" "s1a110" "s1a111" "s1a112" "s1a113" "s1a114" "s1a115" "s1a116" "s1a117" "s1a118" "s1a119" "s1a120" "s1a121" "s1a122" "s1a123" "s1a124" "s1a125" "s1a126" "s1a127" "s1a128" "s1a129" "s1a130" "s1a131" "s1a132" "s1a133" "s1a134" "s1a135" "s1a136" "s1a137" "s1a138" "s1a139" "s1a140" "s1a141" "s1a142" "s1a143" "s1a144" "s1a145" "s1a146" "s1a147" "s1a148" "s1a149" "s1a150" "s1a151" "s1a152" "s1a153" "s1a154" "s1a155" "s1a156" "s1a157" "s1a158" "s1a159" "s1a160" "s1a161" "s1a162" "s1a163" "s1a164" "s1a165" "s1a166" "s1a167" "s1a168" "s1a169" "s1a170" "s1a171" "s1a172" "s1a173" "s1a174" "s1a175" "s1a176" "s1a177" "s1a178" "s1a179" "s1a180" "s1a181" "s1a182" "s1a183" "s1a184" "s1a185" "s1a186" "s1a187" "s1a188" "s1a189" "s1a190" "s1a191" "s1a192" "s1a193" "s1a194" "s1a195" "s1a196" "s1a197" "s1a198" "s1a199" "s1a200" "s1a201" "s1a202" "s1a203" "s1a204" "s1a205" "s1a206" "s1a207" "s1a208" "s1a209" "s1a210" "s1a211" "s1a212" "s1a213" "s1a214" "s1a215" "s1a216" "s1a217" "s1a218" "s1a219" "s1a220" "s1a221" "s1a222" "s1a223" "s1a224" "s1a225" "s1a226" "s1a227" "s1a228" "s1a229" "s1a230" "s1a231" "s1a232" "s1a233" "s1a234" "s1a235" "s1a236" "s1a237" "s1a238" "s1a239" "s1a240" "s1a241" "s1a242" "s1a243" "s1a244" "s1a245" "s1a246" "s1a247" "s1a248" "s1a249" "s1a250" "s1a251" "s1a252" "s1a253" "s1a254" "s1a255" "s1a256" "s1a257" "s1a258" "s1a259" "s1a260" "s1a261" "s1a262" "s1a263" "s1a264" "s1a265" "s1a266" "s1a267" "s1a268" "s1a269" "s1a270" "s1a271" "s1a272" "s1a273" "s1a274" "s1a275" "s1a276" "s1a277" "s1a278" "s1a279" "s1a280" "s1a281" "s1a282" "s1a283" "s1a284" "s1a285" "s1a286" "s1a287" "s1a288" "s1a289" "s1a290" "s1a291" "s1a292" "s1a293" "s1a294" "s1a295" "s1a296" "s1a297" "s1a298" "s1a299" "s1a300" "s1a301" "s1a302" "s1a303" "s1a304" "s1a305" "s1a306" "s1a307" "s1a308" "s1a309" "s1a310" "s1a311" "s1a312" "s1a313" "s1a314" "s1a315" "s1a316" "s1a317" "s1a318" "s1a319" "s1a320" "s1a321" "s1a322" "s1a323" "s1a324" "s1a325" "s1a326" "s1a327" "s1a328" "s1a329" "s1a330" "s1a331" "s1a332" "s1a333" "s1a334" "s1a335" "s1a336" "s1a337" "s1a338" "s1a339" "s1a340" "s1a341" "s1a342" "s1a343" "s1a344" "s1a345" "s1a346" "s1a347" "s1a348" "s1a349" "s1a350" "s1a351" "s1a352" "s1a353" "s1a354" "s1a355" "s1a356" "s1a357" "s1a358" "s1a359" "s1a360" "s1a361" "s1a362" "s1a363" "s1a364" "s1a365" "s1a366" "s1a367" "s1a368" "s1a369" "s1a370" "s1a371" "s1a372" "s1a373" "s1a374" "s1a375" "s1a376" "s1a377" "s1a378" "s1a379" "s1a380" "s1a381" "s1a382" "s1a383" "s1a384" "s1a385" "s1a386" "s1a387" "s1a388" "s1a389" "s1a390" "s1a391" "s1a392" "s1a393" "s1a394" "s1a395" "s1a396" "s1a397" "s1a398" "s1a399" "s1a400" "s1a401" "s1a402" "s1a403" "s1a404" "s1a405" "s1a406" "s1a407" "s1a408" "s1a409" "s1a410" "s1a411" "s1a412" "s1a413" "s1a414" "s1a415" "s1a416" "s1a417" "s1a418" "s1a419" "s1a420" "s1a421" "s1a422" "s1a423" "s1a424" "s1a425" "s1a426" "s1a427" "s1a428" "s1a429" "s1a430" "s1a431" "s1a432" "s1a433" "s1a434" "s1a435" "s1a436" "s1a437" "s1a438" "s1a439" "s1a440" "s1a441" "s1a442" "s1a443" "s1a444" "s1a445" "s1a446" "s1a447" "s1a448" "s1a449" "s1a450" "s1a451" "s1a452" "s1a453" "s1a454" "s1a455" "s1a456" "s1a457" "s1a458" "s1a459" "s1a460" "s1a461" "s1a462" "s1a463" "s1a464" "s1a465" "s1a466" "s1a467" "s1a468" "s1a469" "s1a470" "s1a471" "s1a472" "s1a473" "s1a474" "s1a475" "s1a476" "s1a477" "s1a478" "s1a479" "s1a480" "s1a481" "s1a482" "s1a483" "s1a484" "s1a485" "s1a486" "s1a487" "s1a488" "s1a489" "s1a490" "s1a491" "s1a492" "s1a493" "s1a494" "s1a495" "s1a496" "s1a497" "s1a498" "s1a499" "s1a500" "s1a501" "s1a502" "s1a503" "s1a504" "s1a505" "s1a506" "s1a507" "s1a508" "s1a509" "s1a510" "s1a511" "s1a512" "s1a513" "s1a514" "s1a515" "s1a516" "s1a517" "s1a518" "s1a519" "s1a520" "s1a521" "s1a522" "s1a523" "s1a524" "s1a525" "s1a526" "s1a527" "s1a528" "s1a529" "s1a530" "s1a531" "s1a532" "s1a533" "s1a534" "s1a535" "s1a536" "s1a537" "s1a538" "s1a539" "s1a540" "s1a541" "s1a542" "s1a543" "s1a544" "s1a545" "s1a546" "s1a547" "s1a548" "s1a549" "s1a550" "s1a551" "s1a552" "s1a553" "s1a554" "s1a555" "s1a556" "s1a557" "s1a558" "s1a559" "s1a560" "s1a561" "s1a562" "s1a563" "s1a564" "s1a565" "s1a566" "s1a567" "s1a568" "s1a569" "s1a570" "s1a571" "s1a572" "s1a573" "s1a574" "s1a575" "s1a576" "s1a577" "s1a578" "s1a579" "s1a580" "s1a581" "s1a582" "s1a583" "s1a584" "s1a585" "s1a586" "s1a587" "s1a588" "s1a589" "s1a590" "s1a591" "s1a592" "s1a593" "s1a594" "s1a595" "s1a596" "s1a597" "s1a598" "s1a599" "s1a600" "s1a601" "s1a602" "s1a603" "s1a604" "s1a605" "s1a606" "s1a607" "s1a608" "s1a609" "s1a610" "s1a611" "s1a612" "s1a613" "s1a614" "s1a615" "s1a616" "s1a617" "s1a618" "s1a619" "s1a620" "s1a621" "s1a622" "s1a623" "s1a624" "s1a625" "s1a626" "s1a627" "s1a628" "s1a629" "s1a630" "s1a631" "s1a632" "s1a633" "s1a634" "s1a635" "s1a636" "s1a637" "s1a638" "s1a639" "s1a640" "s1a641" "s1a642" "s1a643" "s1a644" "s1a645" "s1a646" "s1a647" "s1a648" "s1a649" "s1a650" "s1a651" "s1a652" "s1a653" "s1a654" "s1a655" "s1a656" "s1a657" "s1a658" "s1a659" "s1a660" "s1a661" "s1a662" "s1a663" "s1a664" "s1a665" "s1a666" "s1a667" "s1a668" "s1a669" "s1a670" "s1a671" "s1a672" "s1a673" "s1a674" "s1a675" "s1a676" "s1a677" "s1a678" "s1a679" "s1a680" "s1a681" "s1a682" "s1a683" "s1a684" "s1a685" "s1a686" "s1a687" "s1a688" "s1a689" "s1a690" "s1a691" "s1a692" "s1a693" "s1a694" "s1a695" "s1a696" "s1a697" "s1a698" "s1a699" "s1a700" "s1a701" "s1a702" "s1a703" "s1a704" "s1a705" "s1a706" "s1a707" "s1a708" "s1a709" "s1a710" "s1a711" "s1a712" "s1a713" "s1a714" "s1a715" "s1a716" "s1a717" "s1a718" "s1a719" "s1a720" "s1a721" "s1a722" "s1a723" "s1a724" "s1a725" "s1a726" "s1a727" "s1a728" "s1a729" "s1a730" "s1a731" "s1a732" "s1a733" "s1a734" "s1a735" "s1a736" "s1a737" "s1a738" "s1a739" "s1a740" "s1a741" "s1a742" "s1a743" "s1a744" "s1a745" "s1a746" "s1a747" "s1a748" "s1a749" "s1a750" "s1a751" "s1a752" "s1a753" "s1a754" "s1a755" "s1a756" "s1a757" "s1a758" "s1a759" "s1a760" "s1a761" "s1a762" "s1a763" "s1a764" "s1a765" "s1a766" "s1a767" "s1a768" "s1a769" "s1a770" "s1a771" "s1a772" "s1a773" "s1a774" "s1a775" "s1a776" "s1a777" "s1a778" "s1a779" "s1a780" "s1a781" "s1a782" "s1a783" "s1a784" "s1a785" "s1a786" "s1a787" "s1a788" "s1a789" "s1a790" "s1a791" "s1a792" "s1a793" "s1a794" "s1a795" "s1a796" "s1a797" "s1a798" "s1a799" "s1a800" "s1a801" "s1a802" "s1a803" "s1a804" "s1a805" "s1a806" "s1a807" "s1a808" "s1a809" "s1a810" "s1a811" "s1a812" "s1a813" "s1a814" "s1a815" "s1a816" "s1a817" "s1a818" "s1a819" "s1a820" "s1a821" "s1a822" "s1a823" "s1a824" "s1a825" "s1a826" "s1a827" "s1a828" "s1a829" "s1a830" "s1a831" "s1a832" "s1a833" "s1a834" "s1a835" "s1a836" "s1a837" "s1a838" "s1a839" "s1a840" "s1a841" "s1a842" "s1a843" "s1a844" "s1a845" "s1a846" "s1a847" "s1a848" "s1a849" "s1a850" "s1a851" "s1a852" "s1a853" "s1a854" "s1a855" "s1a856" "s1a857" "s1a858" "s1a859" "s1a860" "s1a861" "s1a862" "s1a863" "s1a864" "s1a865" "s1a866" "s1a867" "s1a868" "s1a869" "s1a870" "s1a871" "s1a872" "s1a873" "s1a874" "s1a875" "s1a876" "s1a877" "s1a878" "s1a879" "s1a880" "s1a881" "s1a882" "s1a883" "s1a884" "s1a885" "s1a886" "s1a887" "s1a888" "s1a889" "s1a890" "s1a891" "s1a892" "s1a893" "s1a894" "s1a895" "s1a896" "s1a897" "s1a898" "s1a899" "s1a900" "s1a901" "s1a902" "s1a903" "s1a904" "s1a905" "s1a906" "s1a907" "s1a908" "s1a909" "s1a910" "s1a911" "s1a912" "s1a913" "s1a914" "s1a915" "s1a916" "s1a917" "s1a918" "s1a919" "s1a920" "s1a921" "s1a922" "s1a923" "s1a924" "s1a925" "s1a926" "s1a927" "s1a928" "s1a929" "s1a930" "s1a931" "s1a932" "s1a933" "s1a934" "s1a935" "s1a936" "s1a937" "s1a938" "s1a939" "s1a940" "s1a941" "s1a942" "s1a943" "s1a944" "s1a945" "s1a946" "s1a947" "s1a948" "s1a949" "s1a950" "s1a951" "s1a952" "s1a953" "s1a954" "s1a955" "s1a956" "s1a957" "s1a958" "s1a959" "s1a960" "s1a961" "s1a962" "s1a963" "s1a964" "s1a965" "s1a966" "s1a967" "s1a968" "s1a969" "s1a970" "s1a971" "s1a972" "s1a973" "s1a974" "s1a975" "s1a976" "s1a977" "s1a978" "s1a979" "s1a980" "s1a981" "s1a982" "s1a983" "s1a984" "s1a985" "s1a986" "s1a987" "s1a988" "s1a989" "s1a990" "s1a991" "s1a992" "s1a993" "s1a994" "s1a995" "s1a996" "s1a997" "s1a998" "s1a999" "s1a1000" "s1a1001" "s1a1002" "s1a1003" "s1a1004" "s1a1005" "s1a1006" "s1a1007" "s1a1008" "s1a1009" "s1a1010" "s1a1011" "s1a1012" "s1a1013" "s1a1014" "s1a1015" "s1a1016" "s1a1017" "s1a1018" "s1a1019" "s1a1020" "s1a1021" "s1a1022" "s1a1023" "s1a1024" "s1a1025" "s1a1026" "s1a1027" "s1a1028" "s1a1029" "s1a1030" "s1a1031" "s1a1032" "s1a1033" "s1a1034" "s1a1035" "s1a1036" "s1a1037" "s1a1038" "s1a1039" "s1a1040" "s1a1041" "s1a1042" "s1a1043" "s1a1044" "s1a1045" "s1a1046" "s1a1047" "s1a1048" "s1a1049" "s1a1050" "s1a1051" "s1a1052" "s1a1053" "s1a1054" "s1a1055" "s1a1056" "s1a1057" "s1a1058" "s1a1059" "s1a1060" "s1a1061" "s1a1062" "s1a1063" "s1a1064" "s1a1065" "s1a1066" "s1a1067" "s1a1068" "s1a1069" "s1a1070" "s1a1071" "s1a1072" "s1a1073" "s1a1074" "s1a1075" "s1a1076" "s1a1077" "s1a1078" "s1a1079" "s1a1080" "s1a1081" "s1a1082" "s1a1083" "s1a1084" "s1a1085" "s1a1086" "s1a1087" "s1a1088" "s1a1089" "s1a1090" "s1a1091" "s1a1092" "s1a1093" "s1a1094" "s1a1095" "s1a1096" "s1a1097" "s1a1098" "s1a1099" "s1a1100" "s1a1101" "s1a1102" "s1a1103" "s1a1104" "s1a1105" "s1a1106" "s1a1107" "s1a1108" "s1a1109" "s1a1110" "s1a1111" "s1a1112" "s1a1113" "s1a1114" "s1a1115" "s1a1116" "s1a1117" "s1a1118" "s1a1119" "s1a1120" "s1a1121" "s1a1122" "s1a1123" "s1a1124" "s1a1125" "s1a1126" "s1a1127" "s1a1128" "s1a1129" "s1a1130" "s1a1131" "s1a1132" "s1a1133" "s1a1134" "s1a1135" "s1a1136" "s1a1137" "s1a1138" "s1a1139" "s1a1140" "s1a1141" "s1a1142" "s1a1143" "s1a1144" "s1a1145" "s1a1146" "s1a1147" "s1a1148" "s1a1149" "s1a1150" "s1a1151" "s1a1152" "s1a1153" "s1a1154" "s1a1155" "s1a1156" "s1a1157" "s1a1158" "s1a1159" "s1a1160" "s1a1161" "s1a1162" "s1a1163" "s1a1164" "s1a1165" "s1a1166" "s1a1167" "s1a1168" "s1a1169" "s1a1170" "s1a1171" "s1a1172" "s1a1173" "s1a1174" "s1a1175" "s1a1176" "s1a1177" "s1a1178" "s1a1179" "s1a1180" "s1a1181" "s1a1182" "s1a1183" "s1a1184" "s1a1185" "s1a1186" "s1a1187" "s1a1188" "s1a1189" "s1a1190" "s1a1191" "s1a1192" "s1a1193" "s1a1194" "s1a1195" "s1a1196" "s1a1197" "s1a1198" "s1a1199" "s1a1200" "s1a1201" "s1a1202" "s1a1203" "s1a1204" "s1a1205" "s1a1206" "s1a1207" "s1a1208" "s1a1209" "s1a1210" "s1a1211" "s1a1212" "s1a1213" "s1a1214" "s1a1215" "s1a1216" "s1a1217" "s1a1218" "s1a1219" "s1a1220" "s1a1221" "s1a1222" "s1a1223" "s1a1224" "s1a1225" "s1a1226" "s1a1227" "s1a1228" "s1a1229" "s1a1230" "s1a1231" "s1a1232" "s1a1233" "s1a1234" "s1a1235" "s1a1236" "s1a1237" "s1a1238" "s1a1239" "s1a1240" "s1a1241" "s1a1242" "s1a1243" "s1a1244" "s1a1245" "s1a1246" "s1a1247" "s1a1248" "s1a1249" "s1a1250" "s1a1251" "s1a1252" "s1a1253" "s1a1254" "s1a1255" "s1a1256" "s1a1257" "s1a1258" "s1a1259" "s1a1260" "s1a1261" "s1a1262" "s1a1263" "s1a1264" "s1a1265" "s1a1266" "s1a1267" "s1a1268" "s1a1269" "s1a1270" "s1a1271" "s1a1272" "s1a1273" "s1a1274" "s1a1275" "s1a1276" "s1a1277" "s1a1278" "s1a1279" "s1a1280" "s1a1281" "s1a1282" "s1a1283" "s1a1284" "s1a1285" "s1a1286" "s1a1287" "s1a1288" "s1a1289" "s1a1290" "s1a1291" "s1a1292" "s1a1293" "s1a1294" "s1a1295" "s1a1296" "s1a1297" "s1a1298" "s1a1299" "s1a1300" "s1a1301" "s1a1302" "s1a1303" "s1a1304" "s1a1305" "s1a1306" "s1a1307" "s1a1308" "s1a1309" "s1a1310" "s1a1311" "s1a1312" "s1a1313" "s1a1314" "s1a1315" "s1a1316" "s1a1317" "s1a1318" "s1a1319" "s1a1320" "s1a1321" "s1a1322" "s1a1323" "s1a1324" "s1a1325" "s1a1326" "s1a1327" "s1a1328" "s1a1329" "s1a1330" "s1a1331" "s1a1332" "s1a1333" "s1a1334" "s1a1335" "s1a1336" "s1a1337" "s1a1338" "s1a1339" "s1a1340" "s1a1341" "s1a1342" "s1a1343" "s1a1344" "s1a1345" "s1a1346" "s1a1347" "s1a1348" "s1a1349" "s1a1350" "s1a1351" "s1a1352" "s1a1353" "s1a1354" "s1a1355" "s1a1356" "s1a1357" "s1a1358" "s1a1359" "s1a1360" "s1a1361" "s1a1362" "s1a1363" "s1a1364" "s1a1365" "s1a1366" "s1a1367" "s1a1368" "s1a1369" "s1a1370" "s1a1371" "s1a1372" "s1a1373" "s1a1374" "s1a1375" "s1a1376" "s1a1377" "s1a1378" "s1a1379" "s1a1380" "s1a1381" "s1a1382" "s1a1383" "s1a1384" "s1a1385" "s1a1386" "s1a1387" "s1a1388" "s1a1389" "s1a1390" "s1a1391" "s1a1392" "s1a1393" "s1a1394" "s1a1395" "s1a1396" "s1a1397" "s1a1398" "s1a1399" "s1a1400" "s1a1401" "s1a1402" "s1a1403" "s1a1404" "s1a1405" "s1a1406" "s1a1407" "s1a1408" "s1a1409" "s1a1410" "s1a1411" "s1a1412" "s1a1413" "s1a1414" "s1a1415" "s1a1416" "s1a1417" "s1a1418" "s1a1419" "s1a1420" "s1a1421" "s1a1422" "s1a1423" "s1a1424" "s1a1425" "s1a1426" "s1a1427" "s1a1428" "s1a1429" "s1a1430" "s1a1431" "s1a1432" "s1a1433" "s1a1434" "s1a1435" "s1a1436" "s1a1437" "s1a1438" "s1a1439" "s1a1440" "s1a1441" "s1a1442" "s1a1443" "s1a1444" "s1a1445" "s1a1446" "s1a1447" "s1a1448" "s1a1449" "s1a1450" "s1a1451" "s1a1452" "s1a1453" "s1a1454" "s1a1455" "s1a1456" "s1a1457" "s1a1458" "s1a1459" "s1a1460" "s1a1461" "s1a1462" "s1a1463" "s1a1464" "s1a1465" "s1a1466" "s1a1467" "s1a1468" "s1a1469" "s1a1470" "s1a1471" "s1a1472" "s1a1473" "s1a1474" "s1a1475" "s1a1476" "s1a1477" "s1a1478" "s1a1479" "s1a1480" "s1a1481" "s1a1482" "s1a1483" "s1a1484" "s1a1485" "s1a1486" "s1a1487" "s1a1488" "s1a1489" "s1a1490" "s1a1491" "s1a1492" "s1a1493" "s1a1494" "s1a1495" "s1a1496" "s1a1497" "s1a1498" "s1a1499" "s1a1500" "s1a1501" "s1a1502" "s1a1503" "s1a1504" "s1a1505" "s1a1506" "s1a1507" "s1a1508" "s1a1509" "s1a1510" "s1a1511" "s1a1512" "s1a1513" "s1a1514" "s1a1515" "s1a1516" "s1a1517" "s1a1518" "s1a1519" "s1a1520" "s1a1521" "s1a1522" "s1a1523" "s1a1524" "s1a1525" "s1a1526" "s1a1527" "s1a1528" "s1a1529" "s1a1530" "s1a1531" "s1a1532" "s1a1533" "s1a1534" "s1a1535" "s1a1536" "s1a1537" "s1a1538" "s1a1539" "s1a1540" "s1a1541" "s1a1542" "s1a1543" "s1a1544" "s1a1545" "s1a1546" "s1a1547" "s1a1548" "s1a1549" "s1a1550" "s1a1551" "s1a1552" "s1a1553" "s1a1554" "s1a1555" "s1a1556" "s1a1557" "s1a1558" "s1a1559" "s1a1560" "s1a1561" "s1a1562" "s1a1563" "s1a1564" "s1a1565" "s1a1566" "s1a1567" "s1a1568" "s1a1569" "s1a1570" "s1a1571" "s1a1572" "s1a1573" "s1a1574" "s1a1575" "s1a1576" "s1a1577" "s1a1578" "s1a1579" "s1a1580" "s1a1581" "s1a1582" "s1a1583" "s1a1584" "s1a1585" "s1a1586" "s1a1587" "s1a1588" "s1a1589" "s1a1590" "s1a1591" "s1a1592" "s1a1593" "s1a1594" "s1a1595" "s1a1596" "s1a1597" "s1a1598" "s1a1599" "s1a1600" "s1a1601" "s1a1602" "s1a1603" "s1a1604" "s1a1605" "s1a1606" "s1a1607" "s1a1608" "s1a1609" "s1a1610" "s1a1611" "s1a1612" "s1a1613" "s1a1614" "s1a1615" "s1a1616" "s1a1617" "s1a1618" "s1a1619" "s1a1620" "s1a1621" "s1a1622" "s1a1623" "s1a1624" "s1a1625" "s1a1626" "s1a1627" "s1a1628" "s1a1629" "s1a1630" "s1a1631" "s1a1632" "s1a1633" "s1a1634" "s1a1635" "s1a1636" "s1a1637" "s1a1638" "s1a1639" "s1a1640" "s1a1641" "s1a1642" "s1a1643" "s1a1644" "s1a1645" "s1a1646" "s1a1647" "s1a1648" "s1a1649" "s1a1650" "s1a1651" "s1a1652" "s1a1653" "s1a1654" "s1a1655" "s1a1656" "s1a1657" "s1a1658" "s1a1659" "s1a1660" "s1a1661" "s1a1662" "s1a1663" "s1a1664" "s1a1665" "s1a1666" "s1a1667" "s1a1668" "s1a1669" "s1a1670" "s1a1671" "s1a1672" "s1a1673" "s1a1674" "s1a1675" "s1a1676" "s1a1677" "s1a1678" "s1a1679" "s1a1680" "s1a1681" "s1a1682" "s1a1683" "s1a1684" "s1a1685" "s1a1686" "s1a1687" "s1a1688" "s1a1689" "s1a1690" "s1a1691" "s1a1692" "s1a1693" "s1a1694" "s1a1695" "s1a1696" "s1a1697" "s1a1698" "s1a1699" "s1a1700" "s1a1701" "s1a1702" "s1a1703" "s1a1705"
