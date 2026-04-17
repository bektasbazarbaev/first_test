CREATE OR REPLACE FUNCTION match(p text)
RETURNS TABLE(
    id INT,
    soname Varchar,
    phone Varchar,
)
LANGUAGE plpgsql
AS $$
begin 
     RETURN QUERY 
     SELECT pb.id, pb.name, pb.phone 
     FROM phonebook pb
     WHERE pb.name ILIKE '%' || p || '%' OR
     pb.phone ILIKE '%' || p || '%';
END;
$$;

CREATE OR REPLACE FUNCTION pag(
    livit INT,
    Ofs INT
)
RETURNS TABLE (
    id INT,
    name Varchar,
    phone Varchar
)
LANGUAGE plpgsql
AS $$
begin 
    return QUERY
    SELECT pb.id,pb.name,pb.phone 
    FROM phonebook pb
    ORDER BY pb.id
    LIMIT livit OFFSET Ofs;
END;
$$