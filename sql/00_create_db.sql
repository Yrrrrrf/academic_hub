-- In postgresql, database creation is outside the scope of SQL scripts run within a database connection.

-- Create Database or replace if exists
DROP DATABASE IF EXISTS academic_hub;
CREATE DATABASE academic_hub WITH
    OWNER = postgres  -- owner of the database
    ENCODING = 'UTF8'  -- character encoding
    LOCALE_PROVIDER = 'libc'  -- locale provider (libc or icu) it is used to determine the locale settings for the database
    CONNECTION LIMIT = -1  -- maximum number of concurrent connections to the database (-1 means no limit)
    IS_TEMPLATE = False;  -- whether this database can be cloned as a template for creating new databases

-- todo: Modify 01..=02 files to now create a 'academic_owner' role and assign the db to this user, to do not use the main 'postgres' user and avoid that security risk
