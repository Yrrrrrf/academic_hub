-- In PostgreSQL, database creation is outside the scope of SQL scripts run within a database connection.

-- Create Database
CREATE DATABASE academic_hub
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    LOCALE_PROVIDER = 'libc'
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;

-- todo: Modify 01..=02 files to now create a 'academic_owner' role and assign the db to this user, to do not use the main 'postgres' user and avoid that security risk
