-- 09_infrastructure_tables.sql
-- Infrastructure Management Tables for Academic Hub

-- todo: maybe this is part of another `schema`? Some schema that stores information for the payroll system?
-- todo: maybe this is part of another `table`? A table that stores information about the faculty's schedule?
-- todo: think about another possible solution for this (maybe a separate table that stores the faculty's schedule)


-- Table: Buildings
-- Stores information about campus buildings
DROP TABLE IF EXISTS infrastructure_management.building CASCADE;
CREATE TABLE infrastructure_management.building (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address TEXT,
    total_floors INT,
    accessibility_features BOOLEAN DEFAULT false
);

-- Room Types
DROP TABLE IF EXISTS infrastructure_management.room_type CASCADE;
CREATE TABLE infrastructure_management.room_type (
    id SERIAL PRIMARY KEY,
    name VARCHAR(32) UNIQUE NOT NULL  -- e.g. classroom, laboratory, conference room, etc.
);

-- Base Table: Rooms
-- Contains common attributes for all room types
DROP TABLE IF EXISTS infrastructure_management.room_base CASCADE;
CREATE TABLE infrastructure_management.room_base (
    id SERIAL PRIMARY KEY,
    building_id INTEGER NOT NULL REFERENCES infrastructure_management.building(id),
    room_type INTEGER NOT NULL REFERENCES infrastructure_management.room_type(id),
    room_number VARCHAR(32),  -- Identifier for the room (e.g. 101, 102, 103, etc.)
    capacity INT,
    equipment_details JSONB
);

-- Table: Faculty
-- Stores information about the faculty
DROP TABLE IF EXISTS infrastructure_management.faculty CASCADE;
CREATE TABLE infrastructure_management.faculty (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL  --,
--     coordinates GEOGRAPHY(POINT, 4326)  -- Added coordinates column
);

-- Table: FacultyBuildings
-- Stores the buildings where the faculty members are located
DROP TABLE IF EXISTS infrastructure_management.faculty_building CASCADE;
CREATE TABLE infrastructure_management.faculty_building (
    faculty_id INTEGER NOT NULL REFERENCES infrastructure_management.faculty(id),
    building_id INTEGER NOT NULL REFERENCES infrastructure_management.building(id),
    PRIMARY KEY (faculty_id, building_id)  -- to allow a multiple buildings for a single faculty
);

-- Table: Libraries
DROP TABLE IF EXISTS infrastructure_management.library CASCADE;
CREATE TABLE infrastructure_management.library (
    id SERIAL PRIMARY KEY,
    faculty_id INTEGER NOT NULL,
    building_id INTEGER NOT NULL,
    FOREIGN KEY (faculty_id, building_id)
        REFERENCES infrastructure_management.faculty_building(faculty_id, building_id)
);
