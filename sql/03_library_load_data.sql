-- Load the data INTO library_management.the tables
-- This script loads the data INTO library_management.the tables for the library database.




-- RESET SEQUENCES

-- Reset Sequences for Library Management Tables
ALTER SEQUENCE library_management.author_id_seq RESTART WITH 1;
ALTER SEQUENCE library_management.book_id_seq RESTART WITH 1;
ALTER SEQUENCE library_management.book_library_book_series_id_seq RESTART WITH 1;
ALTER SEQUENCE library_management.library_id_seq RESTART WITH 1;
ALTER SEQUENCE library_management.loan_id_seq RESTART WITH 1;
ALTER SEQUENCE library_management.publisher_id_seq RESTART WITH 1;
ALTER SEQUENCE library_management.topic_id_seq RESTART WITH 1;

-- Reset Sequences for School Management Tables
ALTER SEQUENCE school_management.academic_period_id_seq RESTART WITH 1;
ALTER SEQUENCE school_management.attendance_id_seq RESTART WITH 1;
ALTER SEQUENCE school_management.class_group_id_seq RESTART WITH 1;
ALTER SEQUENCE school_management.class_schedule_id_seq RESTART WITH 1;
ALTER SEQUENCE school_management.exam_type_id_seq RESTART WITH 1;
ALTER SEQUENCE school_management.grades_id_seq RESTART WITH 1;
ALTER SEQUENCE school_management.instructor_id_seq RESTART WITH 1;
ALTER SEQUENCE school_management.program_id_seq RESTART WITH 1;
ALTER SEQUENCE school_management.school_id_seq RESTART WITH 1;
ALTER SEQUENCE school_management.student_enrollment_id_seq RESTART WITH 1;
ALTER SEQUENCE school_management.subject_id_seq RESTART WITH 1;

-- Reset Sequences for Common Tables
ALTER SEQUENCE general_dt.general_user_id_seq RESTART WITH 1;




-- Delete all the tables of the library_management schema
DELETE FROM library_management.loan;
DELETE FROM library_management.book_library;
DELETE FROM library_management.book_topic;
DELETE FROM library_management.book_author;
DELETE FROM library_management.book;
DELETE FROM library_management.topic;
DELETE FROM library_management.publisher;
DELETE FROM library_management.author;
DELETE FROM library_management.library;
DELETE FROM library_management.academic_member;

-- delete all the tables of the school_management schema
DELETE FROM school_management.attendance;
DELETE FROM school_management.grades;
DELETE FROM school_management.student_enrollment;
DELETE FROM school_management.class_schedule;
DELETE FROM school_management.class_group;
DELETE FROM school_management.academic_period;
DELETE FROM school_management.exam_type;
DELETE FROM school_management.instructor;
DELETE FROM school_management.student;
DELETE FROM school_management.program;
DELETE FROM school_management.school;
DELETE FROM school_management.subject;

-- delete all the tables of the general_dt schema
DELETE FROM general_dt.general_user;


--^ LIBRARY MANAGEMENT -----------------------------------------------------------



-- * Insert  (for basic tables (that ones without foreign keys inside them))

-- Inserting data INTO library_management.author
INSERT INTO library_management.author (name) VALUES
    ('Robert W. Johnson'),
    ('Steve Maguire'),
    ('Roger G. Schroeder'),
    ('Richard Bronson'),
    ('Katsuhiko Ogata'),
    ('Michael Hammer'),
    ('James Champy')
;

-- Inserting data INTO library_management.publisher
INSERT INTO library_management.library (name) VALUES
    ('Ingeniería'),
    ('Contaduría'),
    ('Economía'),
    ('Arquitectura'),
    ('Derecho')
;

-- Inserting data INTO library_management.publisher
INSERT INTO library_management.publisher (name) VALUES
    ('CECSA'),
    ('McGraw-Hill'),
    ('Prentice Hall'),
    ('Grupo Editorial Norma')
;

-- Inserting data INTO library_management.book
INSERT INTO library_management.book (name, publisher_id, ISBN) VALUES
    ('Administración Financiera', 1, NULL),
    ('Código sin errores', 2, NULL),
    ('Administración de Operaciones', 2, NULL),
    ('Investigación de Operaciones', 2, NULL),
    ('Ingeniería de Control Moderna', 3, NULL),
    ('Reingeniería', 4, NULL)
;

-- Inserting data INTO library_management.academic_member
INSERT INTO general_dt.general_user (name) VALUES
    ('Jorge López'),
    ('Carmen González'),
    ('Luis López'),
    ('Erick Lara'),
    ('Juan Fuentes'),

    ('Fernando Reza') -- me...
;

-- INSERT relation from general_user to academic_member
-- INSERT INTO library_management.academic_member (user_id) VALUES
--     (SELECT id FROM general_dt.general_user WHERE name = 'Fernando Reza')
-- ;
-- THe same as above but fixed
-- INSERT INTO library_management.academic_member (user_id) VALUES
--     ((SELECT id FROM general_dt.general_user WHERE name = 'Fernando Reza'))
-- ;
--     -- The same as above but for id in the where clause
-- all from 0 to 5
INSERT INTO library_management.academic_member (id) VALUES
    ((SELECT id FROM general_dt.general_user WHERE id = 1)),
    ((SELECT id FROM general_dt.general_user WHERE id = 2)),
    ((SELECT id FROM general_dt.general_user WHERE id = 3)),
    ((SELECT id FROM general_dt.general_user WHERE id = 4)),
    ((SELECT id FROM general_dt.general_user WHERE id = 5)),
    ((SELECT id FROM general_dt.general_user WHERE id = 6))
;


-- Inserting data INTO library_management.topic
INSERT INTO library_management.topic (name) VALUES
    ('Administración'),
    ('Planeación'),
    ('Finanzas'),
    ('Organización'),
    ('Sistemas'),
    ('Programación'),
    ('Procesos'),
    ('Programación Lineal'),
    ('Teoria de Juegos'),
    ('Sistemas de Control'),
    ('Transformadas'),
    ('Matrices'),
    ('Optimización'),
    ('Reingeniería')
;


-- * Inserting data INTO library_management.the "complex" tables (those that have foreign keys to other tables)

-- Inserting data INTO library_management.book_author
INSERT INTO library_management.book_author (book_id, author_id) VALUES
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (4, 3),
    (5, 5),
    (6, 6),
    (6, 7)
;

-- Inserting data INTO library_management.book_topic
INSERT INTO library_management.book_topic (book_id, topic_id) VALUES
    (1, 1),
    (1, 2),
    (1, 3),
    (1, 4),
    (2, 5),
    (2, 6),
    (3, 1),
    (3, 2),
    (3, 7),
    (4, 8),
    (4, 9),
    (4, 5),
    (5, 10),
    (5, 11),
    (5, 12),
    (5, 13),
    (6, 7),
    (6, 5),
    (6, 14)
;

-- Inserting data INTO library_management.book_library
INSERT INTO library_management.book_library (book_id, library_id) VALUES
    (1, 5), (1, 5), (1, 1), (1, 1), (1, 1), (1, 2), (1, 3),
    (2, 1), (2, 1), (2, 2), (2, 2), (2, 3),
    (3, 1), (3, 1), (3, 1), (3, 2), (3, 2), (3, 3), (3, 3), (3, 4),
    (4, 1), (4, 1), (4, 2), (4, 2), (4, 2), (4, 3), (4, 4), (4, 4),
    (5, 1), (5, 1), (5, 1),
    (6, 1), (6, 1), (6, 2), (6, 2), (6, 2)
;

SELECT * FROM general_dt.general_user;
SELECT * FROM library_management.academic_member;

-- Inserting data INTO library_management.loan
INSERT INTO library_management.loan (id, academic_member_id, book_library_id, loan_date, return_date) VALUES
    (83, 1,  3, '2023-02-09', '2023-02-11'),
    (84, 1, 32, '2023-02-09', '2023-02-14'),
    (85, 2, 33, '2023-02-09', '2023-02-11'),
    (86, 3, 34, '2023-02-11', '2023-02-14'),
    (88, 4, 26, '2023-02-11', '2023-02-16'),
    (89, 5, 13, '2023-02-11', '2023-02-13'),
    (90, 4, 14, '2023-02-11', '2023-02-16')
;











INSERT INTO school_management.school (name) VALUES
    ('Universidad Autónoma del Estado de México'),
    ('Universidad Nacional Autónoma de México'),
    ('Instituto Politécnico Nacional'),
    ('Universidad Autónoma Metropolitana'),
    ('Universidad Autónoma de Chapingo')
;

INSERT INTO school_management.program (name, school_id) VALUES
--     Engineering Programs
    ('Computer Science', 1),  -- Assuming a school with ID = 1 exists
    ('Mechanical Engineering', 1),
    ('Industrial Engineering', 1),
    ('Artificial Intelligence', 1),
    ('Civil Engineering', 1),
--     Social Sciences Programs
    ('Sociology', 1),
    ('Psychology', 1),
    ('Environmental Science', 1),
    ('Political Science', 1),

--     Economics Programs
    ('Economics', 1),
    ('Law', 1)
;

INSERT INTO school_management.student (id, program_id) VALUES
    (1, 1),
    (2, 2),
    (3, 2),
    (4, 3),
    (5, 4),
    (6, 1)
;

-- SELECT * FROM school_management.student;
INSERT INTO school_management.instructor (name) VALUES
    ('Carolina López'),
    ('Sergio González'),
    ('Lydia Smith'),
    ('William Johnson'),
    ('James Brown')
;

INSERT INTO school_management.subject (name) VALUES
    ('Mathematics'),
    ('Physics'),
    ('Chemistry'),
    ('Biology'),
    ('History')
;

INSERT INTO school_management.academic_period (name) VALUES
    ('2021A'),
    ('2021B'),
    ('2022A'),
    ('2022B'),
    ('2023A'),
    ('2023B'),
    ('2024A')
;

INSERT INTO school_management.class_group (instructor_id, subject_id, period_id) VALUES
    (1, 1, 1),
    (2, 2, 1),
    (3, 3, 1),
    (4, 4, 1),
    (5, 5, 1)
;

INSERT INTO school_management.student_enrollment (student_id, class_group_id, enrollment_date) VALUES
    (6, 1, '2021-01-01'),
    (6, 2, '2021-01-01'),
    (6, 3, '2021-01-01'),
    (6, 4, '2021-01-01'),
    (6, 5, '2021-01-01')
;

INSERT INTO school_management.exam_type (name) VALUES
    ('Ordinary'),
    ('Extraordinary'),
    ('Special')
;

INSERT INTO school_management.grades (student_enrollment_id, exam_type_id, grade, grading_date) VALUES
    (1, 1, 9, '2021-01-01'),
    (2, 1, 10, '2021-01-01'),
    (3, 1, 8, '2021-01-01'),
    (4, 1, 7, '2021-01-01'),
    (5, 2, 9, '2021-01-01')
;

INSERT INTO school_management.attendance (student_enrollment_id, date, status)
VALUES
    (1, '2021-01-01', 'Present'),
    (1, '2021-01-02', 'Present'),
    (1, '2021-01-03', 'Present'),
    (1, '2021-01-04', 'Present'),
    (1, '2021-01-05', 'Present')
;

INSERT INTO school_management.class_schedule (class_group_id, day_of_week, start_time, end_time) VALUES
    (1, 'Monday', '08:00', '10:00'),
    (1, 'Wednesday', '08:00', '10:00'),
    (1, 'Friday', '08:00', '10:00'),
    (2, 'Monday', '10:00', '12:00'),
    (2, 'Wednesday', '10:00', '12:00'),
    (2, 'Friday', '10:00', '12:00'),
    (3, 'Monday', '14:00', '16:00'),
    (3, 'Wednesday', '14:00', '16:00'),
    (3, 'Friday', '14:00', '16:00'),
    (4, 'Tuesday', '08:00', '10:00'),
    (4, 'Thursday', '08:00', '10:00'),
    (4, 'Saturday', '08:00', '10:00'),
    (5, 'Tuesday', '10:00', '12:00'),
    (5, 'Thursday', '10:00', '12:00'),
    (5, 'Saturday', '10:00', '12:00')
;