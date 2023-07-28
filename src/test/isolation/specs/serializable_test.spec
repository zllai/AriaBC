setup
{
  CREATE TABLE foo (
	key		int PRIMARY KEY,
	value	int
  );
  INSERT INTO foo VALUES(1, 1); 
  INSERT INTO foo VALUES(2, 1); 
  INSERT INTO foo VALUES(3, 1);
}

teardown
{
  DROP TABLE foo;
}

session "A"
step "A1" {BEGIN;}
step "A2" {SELECT key, value FROM foo WHERE key = 1;}
step "A3" {UPDATE foo SET value = 2 WHERE key = 2;}
step "A4" {ROLLBACK;}

session "B"
step "B1" {BEGIN;}
step "B2" {SELECT key, value FROM foo WHERE key = 2;}
step "B3" {UPDATE foo SET value = 2 WHERE key = 3;}
step "B4" {COMMIT;}

session "C"
step "C1" {BEGIN;}
step "C2" {SELECT key, value FROM foo WHERE key = 3;}
step "C3" {UPDATE foo SET value = 2 WHERE key = 1;}
step "C4" {COMMIT;}

permutation "A1" "B1" "C1" "A2" "B2" "C2" "C3" "C4" "B3" "B4" "A3" "A4" 