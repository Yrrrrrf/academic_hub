-- ******************************************************************
-- * Academic Hub - Infrastructure Management System Views
-- * Description: This file contains views for summarizing and
-- *              presenting infrastructure data in a user-friendly manner.
-- ******************************************************************

-- View: vw_building_details
-- Description: Provides detailed information about each building, including total rooms and their capacities.
CREATE OR REPLACE VIEW infrastructure_management.vw_building_details AS
SELECT
    b.id AS building_id,
    b.name AS building_name,
    b.address,
    b.total_floors,
    b.accessibility_features,
    COUNT(r.id) AS total_rooms,
    SUM(r.capacity) AS total_capacity
FROM infrastructure_management.building b
LEFT JOIN infrastructure_management.room r ON b.id = r.building_id
GROUP BY b.id, b.name, b.address, b.total_floors, b.accessibility_features;

-- View: vw_room_details
-- Description: Provides detailed information about each room, including the building it is located in and the room type.
CREATE OR REPLACE VIEW infrastructure_management.vw_room_details AS
SELECT
    r.id AS room_id,
    rt.name AS room_type,
    r.name AS room_name,
    b.name AS building_name,
    r.capacity,
    r.equipment_details
FROM infrastructure_management.room r
JOIN infrastructure_management.room_type rt ON r.room_type = rt.id
JOIN infrastructure_management.building b ON r.building_id = b.id;

-- View: vw_faculty_buildings
-- Description: Lists all buildings associated with each faculty.
CREATE OR REPLACE VIEW infrastructure_management.vw_faculty_buildings AS
SELECT
    f.id AS faculty_id,
    f.name AS faculty_name,
    b.id AS building_id,
    b.name AS building_name
FROM infrastructure_management.faculty f
JOIN infrastructure_management.faculty_building fb ON f.id = fb.faculty_id
JOIN infrastructure_management.building b ON fb.building_id = b.id;

-- View: vw_library_details
-- Description: Provides detailed information about each library, including the faculty and building it is associated with.
CREATE OR REPLACE VIEW infrastructure_management.vw_library_details AS
SELECT
    l.id AS library_id,
    f.name AS faculty_name,
    b.name AS building_name
FROM infrastructure_management.library l
JOIN infrastructure_management.faculty_building fb ON l.faculty_id = fb.faculty_id AND l.building_id = fb.building_id
JOIN infrastructure_management.faculty f ON fb.faculty_id = f.id
JOIN infrastructure_management.building b ON fb.building_id = b.id;

-- Example usage:
SELECT * FROM infrastructure_management.vw_building_details;
SELECT * FROM infrastructure_management.vw_room_details;


-- todo: Improve this views addins some data from other schemas (and tables)
SELECT * FROM infrastructure_management.vw_faculty_buildings;
SELECT * FROM infrastructure_management.vw_library_details;
