-- ? AUTH TABLES
-- Tables used for authentication and authorization

-- Table: GeneralUser
DROP TABLE IF EXISTS auth.general_user CASCADE;
CREATE TABLE IF NOT EXISTS auth.general_user (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    additional_info JSONB
);
