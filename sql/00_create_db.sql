-- Create Database
-- In PostgreSQL, database creation is outside the scope of SQL scripts run within a database connection.

CREATE DATABASE library_management
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    LOCALE_PROVIDER = 'libc'
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;

