CREATE OR REPLACE PROCEDURE insorup(
    pname Varchar,
    pphone Varchar
)
LANGUAGE plpgsql
AS $$
BEGIN
     if EXISTS (
        SELECT 1 from phonebook WHERE name=pname
     )THEN
     UPDATE phonebook 
     SET phone = pphone
     WHERE name=pname;
     ELSE
     INSERT INTO phonebook(name,phone)
     VALUES (pname,pphone);
     END if;
END;
$$


CREATE OR REPLACE PROCEDURE del_use(
    userr VARCHAR,
    uphone VARCHAR
)
AS $$
BEGIN
     Delete from phonebook(name,phone)
     WHERE name=userr
     OR phone=uphone;
END;
$$
