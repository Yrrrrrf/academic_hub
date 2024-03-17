-- Create main schemas for the project

DROP SCHEMA IF EXISTS public CASCADE;  -- Drop the public schema and all objects in it

--     create the new schemas
CREATE SCHEMA IF NOT EXISTS school_management;  -- Schema for school management(Students, Teachers, Subjects, etc)
CREATE SCHEMA IF NOT EXISTS library_management;  -- Schema for library management (Books, Authors, Loan History, etc)

-- Create the users for the schemas
CREATE ROLE library_admin WITH LOGIN PASSWORD 'secure_password_for_library';
CREATE ROLE school_admin WITH LOGIN PASSWORD 'secure_password_for_school';

-- Grant USAGE and CREATE privileges on the schema to the library_admin
GRANT USAGE, CREATE ON SCHEMA library_management TO library_admin;
GRANT USAGE, CREATE ON SCHEMA school_management TO school_admin;

-- Grant all privileges on all tables in the specific schema
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA library_management TO library_admin;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA school_management TO school_admin;

-- To automatically grant privileges on future tables:
ALTER DEFAULT PRIVILEGES IN SCHEMA library_management GRANT ALL PRIVILEGES ON TABLES TO library_admin;
ALTER DEFAULT PRIVILEGES IN SCHEMA school_management GRANT ALL PRIVILEGES ON TABLES TO school_admin;

-- If there are specific functions or procedures:
-- GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA library_management TO library_admin;
-- GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA school_management TO school_admin;

-- -- -- Grant the library_admin and school_admin roles to the specific users
-- -- -- GRANT library_admin TO library_user;
-- -- -- GRANT school_admin TO school_user;
-- -- -- SOME OTHER...

