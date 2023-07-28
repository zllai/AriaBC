Create or replace function random_string(length integer) returns text as
$$
declare
  chars text[] := '{0,1,2,3,4,5,6,7,8,9,A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z,a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z}';
  result text := '';
  i integer := 0;
begin
  if length < 0 then
    raise exception 'Given length cannot be less than 0';
  end if;
  for i in 1..length loop
    result := result || chars[1+random()*(array_length(chars, 1)-1)];
  end loop;
  return result;
end;
$$ language plpgsql;

CREATE OR REPLACE FUNCTION read_modify_write(read_user_id TEXT[],
                                             update_user_id TEXT[])
                         RETURNS VOID AS
$$
DECLARE
    sql_read     CONSTANT text := 'SELECT * FROM usertable WHERE YCSB_KEY = $1';
    sql_update   CONSTANT text := 'UPDATE usertable SET FIELD0 = $1,FIELD1 = $2,FIELD2 = $3,FIELD3 = $4,FIELD4 = $5,FIELD5 = $6,FIELD6 = $7,FIELD7 = $8,FIELD8 = $9,FIELD9 = $10 WHERE YCSB_KEY = $11';
    num_field    CONSTANT integer := 10;
    field_length CONSTANT integer := 10;
    update_string CONSTANT text := '0000000000';
    user_id text;
BEGIN
    if array_length(read_user_id, 1) > 0 then
        perform setseed(substring(read_user_id[1], 5, 10)::float / 100000);
    else
        perform setseed(0);
    end if;
    FOREACH user_id IN ARRAY read_user_id loop
        EXECUTE sql_read USING user_id;
    end loop;
    FOREACH user_id IN ARRAY update_user_id loop
        EXECUTE sql_update USING random_string(10),random_string(10),random_string(10),random_string(10),random_string(10),random_string(10),random_string(10),random_string(10),random_string(10),random_string(10), user_id;
    end loop;
    RETURN;
END;
$$ LANGUAGE plpgsql;