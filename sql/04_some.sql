-- This file contains the scripts to create...
-- - Some other fields that are not defined yet
-- - Like: <field1>, <field2>, <field3>

-- query that returns the fields of the table
-- JUST THE TABLE COLUMNS (NO DATA)

SELECT column_name
FROM information_schema.columns
WHERE table_name = 'some_table'
ORDER BY ordinal_position;
