CREATE OR REPLACE FUNCTION seq(min integer, max integer, delta integer)
RETURNS TABLE(nros integer) AS $$
DECLARE
    contador integer;
BEGIN
    CREATE TABLE seqTable(nros integer);
    IF delta > 0 THEN
        contador = min;
        while contador <= max LOOP
            INSERT INTO seqTable VALUES(contador);
            contador = contador + delta;
        END LOOP;
    ELSE
        contador = max;
        while contador >= min LOOP
            INSERT INTO seqTable VALUES(contador);
            contador = contador + delta;
        END LOOP;
    END IF;
    RETURN QUERY SELECT * FROM seqTable;
    DROP TABLE seqTable;
    RETURN;
END
$$ language plpgsql