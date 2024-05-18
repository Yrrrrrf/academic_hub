INSERT INTO infrastructure_management.building (name, address, total_floors, accessibility_features) VALUES
    (
        'Building A ',
        'Cerro de Coatepec S/N, Ciudad Universitaria, Universitaria, 50110 Toluca de Lerdo, Méx.',
        4,
        true
    ),
    (
        'Building B',
        'Cerro de Coatepec S/N, Ciudad Universitaria, Universitaria, 50110 Toluca de Lerdo, Méx.',
        3,
        true
    ),
    (
        'Building C',
        'Cerro de Coatepec S/N, Ciudad Universitaria, Universitaria, 50110 Toluca de Lerdo, Méx.',
        5,
        true
    ),
    (
        'Building D',
        'Cerro de Coatepec S/N, Ciudad Universitaria, Universitaria, 50110 Toluca de Lerdo, Méx.',
        2,
        true
    ),
    (
        'Building E',
        'Cerro de Coatepec S/N, Ciudad Universitaria, Universitaria, 50110 Toluca de Lerdo, Méx.',
        2,
        true
    ),
    (
        'Building F',
        'Cerro de Coatepec S/N, Ciudad Universitaria, Universitaria, 50110 Toluca de Lerdo, Méx.',
        2,
        true
    ),
    (
        'Building G',
        'Cerro de Coatepec S/N, Ciudad Universitaria, Universitaria, 50110 Toluca de Lerdo, Méx.',
        3,
        true
    ),
    (
        'Building H',
        'Cerro de Coatepec S/N, Ciudad Universitaria, Universitaria, 50110 Toluca de Lerdo, Méx.',
        3,
        true
    ),
    (
        'Building I',
        'Cerro de Coatepec S/N, Ciudad Universitaria, Universitaria, 50110 Toluca de Lerdo, Méx.',
        2,
        true
    ),
    (
        'Some Library (Accounting) ',  -- id: 10
        'Some address...',
        1,
        false
    ),
    (
        'Some Library (Economics)',  -- id: 11
        'Some address...',
        1,
        false
    ),
    (
        'Some Library (Architecture)',  -- id: 12
        'Some address...',
        1,
        false
    ),
    (
        'Some Library (Medicine)',  -- id: 13
        'Some address...',
        1,
        false
    ),
    (
        'Some Library (Law)',  -- id: 14
        'Some address...',
        1,
        false
    ),
    (
        'Some Library (Arts)',  -- id: 15
        'Some address...',
        1,
        false
    )
;

INSERT INTO infrastructure_management.room_type (name) VALUES
    ('Classroom'),
    ('Laboratory'),
    ('Conference Room'),
    ('Auditorium'),
    ('Office')
;

INSERT INTO infrastructure_management.room (building_id, room_type, name, capacity, equipment_details) VALUES
    (1, 1, 'Sala 1', 20, '{"projector": true, "whiteboard": true, "computers": 20}'),
    (1, 1, 'Sala 2', 25, '{"projector": true, "whiteboard": true, "computers": 20}'),
    (1, 1, 'Sala 3', 30, '{"projector": true, "whiteboard": true, "computers": 20}'),
    (1, 1, 'Sala 4', 35, '{"projector": true, "whiteboard": true, "computers": 20}'),
    (1, 1, 'Sala 5', 40, '{"projector": true, "whiteboard": true, "computers": 20}'),
    (1, 1, 'Sala 6', 45, '{"projector": true, "whiteboard": true, "computers": 20}'),
    (1, 1, 'Sala 7', 50, '{"projector": true, "whiteboard": true, "computers": 20}'),
    (1, 1, 'Sala 8', 55, '{"projector": true, "whiteboard": true, "computers": 20}'),

    (1, 4, 'Auditorio 1', 100, '{}'),
    (1, 4, 'Auditorio 2', 150, '{}'),
    (1, 4, 'Auditorio 3', 200, '{}'),
    (1, 4, 'Auditorio 4', 250, '{}'),
    (1, 4, 'Auditorio 5', 300, '{}'),
    (1, 4, 'Auditorio 6', 350, '{}'),
    (1, 4, 'Auditorio 7', 400, '{}'),
    (1, 4, 'Auditorio 8', 450, '{}')
;

INSERT INTO infrastructure_management.faculty (name) VALUES
    ('Engineering'),
    ('Accounting'),
    ('Economics'),
    ('Architecture'),
    ('Medicine'),
    ('Law'),
    ('Arts')
;

INSERT INTO infrastructure_management.faculty_building (faculty_id, building_id) VALUES
    -- Engineering faculty will be assigned to the first building
    (1,  1),
    (1,  2),
    (1,  3),
    (1,  4),
    (1,  5),
    (1,  6),
    (1,  7),
    (1,  8),
    (1,  9),
    -- For the other faculties, we'll just assign them to the first building
    (2, 10),
    (3, 11),
    (4, 12),
    (5, 13),
    (6, 14),
    (7, 15)
;

INSERT INTO infrastructure_management.library (faculty_id, building_id) VALUES
    (1,  2),  -- Engineering Library (Building B)
    (2, 10),  -- Accounting Library
    (3, 11),  -- Economics Library
    (4, 12),  -- Architecture Library
    (5, 13),  -- Medicine Library
    (6, 14),  -- Law Library
    (7, 15)  -- Arts Library
;
