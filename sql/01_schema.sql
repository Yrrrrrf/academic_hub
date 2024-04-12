-- Create main schemas for the project

DROP SCHEMA IF EXISTS public CASCADE;  -- Drop the public schema and all objects in it

--     create the new schemas
CREATE SCHEMA IF NOT EXISTS school_management;  -- Schema for school management(Students, Teachers, Subjects, etc)
CREATE SCHEMA IF NOT EXISTS library_management;  -- Schema for library management (Books, Authors, Loan History, etc)
CREATE SCHEMA IF NOT EXISTS general_dt; -- Schema for general data (User data, etc)

-- Create the users for the schemas
CREATE ROLE library_admin WITH LOGIN PASSWORD 'secure_password_for_library';
CREATE ROLE school_admin WITH LOGIN PASSWORD 'secure_password_for_school';
-- the same but only create it if it does not exist

-- Grant USAGE and CREATE privileges on the schema to the library_admin

GRANT USAGE, CREATE ON SCHEMA general_dt, library_management TO library_admin;
GRANT USAGE, CREATE ON SCHEMA general_dt, school_management TO school_admin;

-- Grant all privileges on all tables in the specific schema
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA general_dt, library_management TO library_admin;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA general_dt, school_management TO school_admin;

-- To automatically grant privileges on future tables:
ALTER DEFAULT PRIVILEGES IN SCHEMA general_dt, library_management GRANT ALL PRIVILEGES ON TABLES TO library_admin;
ALTER DEFAULT PRIVILEGES IN SCHEMA general_dt, school_management GRANT ALL PRIVILEGES ON TABLES TO school_admin;



-- If there are specific functions or procedures:

