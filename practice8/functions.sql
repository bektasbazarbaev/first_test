CREATE OR REPLACE FUNCTION search_contacts(pattern TEXT)
RETURNS TABLE(
    id INT,
    name VARCHAR,
    phone VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT pb.id, pb.name, pb.phone
    FROM phonebook pb
    WHERE pb.name ILIKE '%' || pattern || '%'
       OR pb.phone ILIKE '%' || pattern || '%';
END;
$$;

CREATE OR REPLACE FUNCTION get_contacts_page(
    limit_count INT,
    offset_count INT
)
RETURNS TABLE(
    id INT,
    name VARCHAR,
    phone VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT pb.id, pb.name, pb.phone
    FROM phonebook pb
    ORDER BY pb.id
    LIMIT limit_count OFFSET offset_count;
END;
$$;