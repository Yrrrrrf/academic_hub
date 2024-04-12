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
ALTER SEQUENCE school_management.grade_id_seq RESTART WITH 1;
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
DELETE FROM school_management.grade;
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


-- ? COMMON TABLES -----------------------------------------------------------------------------------------------------

-- Table: general_user (Common table for all systems)
-- todo: Add additional fields as needed for each system
-- todo: Add some constrains for email & role...
DROP TABLE IF EXISTS general_dt.general_user CASCADE;
CREATE TABLE IF NOT EXISTS general_dt.general_user (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  user_type VARCHAR(50) NOT NULL DEFAULT 'Student', -- Sets "Student" as the default user_type
  -- email VARCHAR(255) UNIQUE NOT NULL, -- Temporarily commented out as requested
  additional_info JSONB
  -- role VARCHAR(255) NOT NULL -- Additional column to specify if the member is a student, faculty, staff, etc.
);
