-- ACADEMIC HUB DATABASE SCHEMA

-- Create main schemas for the project
DROP SCHEMA IF EXISTS public CASCADE;  -- Drop the public schema and all objects in it

-- Create the new schemas
CREATE SCHEMA IF NOT EXISTS general_dt; -- Schema for general data (shared tables, etc)
CREATE SCHEMA IF NOT EXISTS school_management;  -- Schema for school management(Students, Teachers, Subjects, etc)
CREATE SCHEMA IF NOT EXISTS library_management;  -- Schema for library management (Books, Authors, Loan History, etc)

-- Create the users for the schemas
DO $$  -- Do is a block that allows you to execute multiple statements in a single transaction
BEGIN  -- Do all the following in a single transaction
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'library_admin') THEN
        CREATE ROLE library_admin WITH LOGIN PASSWORD 'secure_password_for_library';
    END IF;
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'school_admin') THEN
        CREATE ROLE school_admin WITH LOGIN PASSWORD 'secure_password_for_school';
    END IF;
END $$;  -- End of the block

-- Grant USAGE and CREATE privileges on the schema to the library_admin
GRANT USAGE, CREATE ON SCHEMA general_dt, library_management TO library_admin;
GRANT USAGE, CREATE ON SCHEMA general_dt, school_management TO school_admin;

-- Grant all privileges on all tables in the specific schema
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA general_dt, library_management TO library_admin;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA general_dt, school_management TO school_admin;

-- Grant all privileges on all sequences in the specific schema
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA general_dt, library_management TO library_admin;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA general_dt, school_management TO school_admin;

-- To automatically grant privileges on future tables:
ALTER DEFAULT PRIVILEGES IN SCHEMA general_dt, library_management GRANT ALL PRIVILEGES ON TABLES TO library_admin;
ALTER DEFAULT PRIVILEGES IN SCHEMA general_dt, school_management GRANT ALL PRIVILEGES ON TABLES TO school_admin;

-- To automatically grant privileges on future sequences:
ALTER DEFAULT PRIVILEGES IN SCHEMA general_dt, library_management GRANT ALL PRIVILEGES ON SEQUENCES TO library_admin;
ALTER DEFAULT PRIVILEGES IN SCHEMA general_dt, school_management GRANT ALL PRIVILEGES ON SEQUENCES TO school_admin;
