CREATE OR REPLACE FUNCTION
producto ()
RETURNS TABLE (a int, b int, c int, d int) AS $$
DECLARE
  tuple_r RECORD;
  tuple_s RECORD;
BEGIN
  CREATE TABLE producto(a int, b int, c int, d int);
  
  FOR tuple_r IN SELECT * FROM R LOOP
    FOR tuple_s IN SELECT * FROM S LOOP
      INSERT INTO producto VALUES(tuple_r.a, tuple_r.b, tuple_s.a, tuple_s.b);
    END LOOP;
  END LOOP;

  RETURN QUERY SELECT * FROM producto;

  DROP TABLE producto;

END
$$ language plpgsql