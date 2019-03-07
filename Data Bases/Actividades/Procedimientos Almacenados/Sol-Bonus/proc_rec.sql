CREATE OR REPLACE FUNCTION
vuelos_posibles (c_origen varchar)
RETURNS TABLE (ciudad_destino varchar(100)) AS $$
DECLARE
  count_actual INT;
  count_previo INT;
BEGIN
  CREATE TABLE alcanzo(co varchar(100), cd varchar(100));
  INSERT INTO alcanzo(SELECT * FROM Vuelos);
  
  WHILE True LOOP
    count_previo = (SELECT COUNT(*) FROM Alcanzo);
    INSERT INTO alcanzo(
        SELECT V.co, A.cd
        FROM Alcanzo A, Vuelos V
        WHERE V.cd = A.co AND ((V.co, A.cd) NOT IN (SELECT * FROM Alcanzo))
    );
    count_actual = (SELECT COUNT(*) FROM Alcanzo);
    IF count_actual = count_previo THEN
      EXIT;
    END IF; 
  END LOOP;

  RETURN QUERY EXECUTE 'SELECT cd
    FROM Alcanzo
    WHERE co = $1'
  USING c_origen;

  DROP TABLE Alcanzo;

END
$$ language plpgsql