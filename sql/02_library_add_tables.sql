-- Create the database structure for the library database
-- This script creates the tables and relationships for the library database.




-- COMMON TABLES -----------------------------------------------------------------------------------------------------

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




-- LIBRARY MANAGEMENT SYSTEM -------------------------------------------------------------------------------------------

-- Table: author
DROP TABLE IF EXISTS library_management.author CASCADE;
CREATE TABLE library_management.author (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL
);

-- Table: library
DROP TABLE IF EXISTS library_management.library CASCADE;
CREATE TABLE library_management.library (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL
);

-- Table: publisher
DROP TABLE IF EXISTS library_management.publisher CASCADE;
CREATE TABLE library_management.publisher (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL
);

-- Table: book
DROP TABLE IF EXISTS library_management.book CASCADE;
CREATE TABLE library_management.book (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  publisher_id INTEGER REFERENCES library_management.publisher(id),
  ISBN VARCHAR(13)  -- ISBN is a 13-digit number
);

-- Table: book_author
DROP TABLE IF EXISTS library_management.book_author CASCADE;
CREATE TABLE library_management.book_author (
  book_id INTEGER NOT NULL REFERENCES library_management.book(id),
  author_id INTEGER NOT NULL REFERENCES library_management.author(id),
  PRIMARY KEY (book_id, author_id)
);

-- Table: topic
DROP TABLE IF EXISTS library_management.topic CASCADE;
CREATE TABLE library_management.topic (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL
);

-- Table: book_topic
DROP TABLE IF EXISTS library_management.book_topic CASCADE;
CREATE TABLE library_management.book_topic (
  book_id INTEGER NOT NULL REFERENCES library_management.book(id),
  topic_id INTEGER NOT NULL REFERENCES library_management.topic(id),
  PRIMARY KEY (book_id, topic_id)
);

-- Table: book_library
DROP TABLE IF EXISTS library_management.book_library CASCADE;
CREATE TABLE library_management.book_library (
  book_series_id SERIAL PRIMARY KEY,
  book_id INTEGER NOT NULL REFERENCES library_management.book(id),
  library_id INTEGER NOT NULL REFERENCES library_management.library(id)
);

-- Table: academic_member
DROP TABLE IF EXISTS library_management.academic_member CASCADE;
-- Academic Member Table with reference to GeneralUser
CREATE TABLE IF NOT EXISTS library_management.academic_member (
  id INTEGER PRIMARY KEY REFERENCES general_dt.general_user(id)
  -- Additional fields specific to library management system
);


-- Table: loan
DROP TABLE IF EXISTS library_management.loan CASCADE;
CREATE TABLE library_management.loan (
  id SERIAL PRIMARY KEY,
  academic_member_id INTEGER NOT NULL REFERENCES library_management.academic_member(id),
  book_library_id INTEGER REFERENCES library_management.book_library(book_series_id),
  loan_date DATE,
  return_date DATE
);




--? SCHOOL MANAGEMENT SYSTEM --------------------------------------------------------------------------------------------




--^  Create the database structure for the school management system

-- Table: School
DROP TABLE IF EXISTS school_management.school CASCADE;
CREATE TABLE school_management.school (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL
);

-- Table: Program
DROP TABLE IF EXISTS school_management.program CASCADE;
CREATE TABLE school_management.program (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  school_id INTEGER NOT NULL REFERENCES school_management.school(id)
);

-- Table: Student
DROP TABLE IF EXISTS school_management.student CASCADE;
-- Student Table with reference to GeneralUser
CREATE TABLE IF NOT EXISTS school_management.student (
  id INTEGER PRIMARY KEY REFERENCES general_dt.general_user(id),
  program_id INTEGER NOT NULL REFERENCES school_management.program(id)
  -- Other student-specific fields
);

-- Table: Instructor
DROP TABLE IF EXISTS school_management.instructor CASCADE;
CREATE TABLE school_management.instructor (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL
);

-- Table: Subject
DROP TABLE IF EXISTS school_management.subject CASCADE;
CREATE TABLE school_management.subject (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL
);

-- Table: AcademicPeriod
DROP TABLE IF EXISTS school_management.academic_period CASCADE;
CREATE TABLE school_management.academic_period (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL
);

-- Table: ClassGroup
DROP TABLE IF EXISTS school_management.class_group CASCADE;
CREATE TABLE school_management.class_group (
  id SERIAL PRIMARY KEY,
  instructor_id INTEGER NOT NULL REFERENCES school_management.instructor(id),
  subject_id INTEGER NOT NULL REFERENCES school_management.subject(id),
  period_id INTEGER NOT NULL REFERENCES school_management.academic_period(id)
);

-- Table: StudentEnrollment
DROP TABLE IF EXISTS school_management.student_enrollment CASCADE;
CREATE TABLE school_management.student_enrollment (
  id SERIAL PRIMARY KEY,
  student_id INTEGER NOT NULL REFERENCES school_management.student(id),
  class_group_id INTEGER NOT NULL REFERENCES school_management.class_group(id),
  enrollment_date DATE NOT NULL
);

-- Table: ExamType
DROP TABLE IF EXISTS school_management.exam_type CASCADE;
CREATE TABLE school_management.exam_type (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL
);

-- Table: Grades
DROP TABLE IF EXISTS school_management.grades CASCADE;
CREATE TABLE school_management.grades (
  id SERIAL PRIMARY KEY,
  student_enrollment_id INTEGER NOT NULL REFERENCES school_management.student_enrollment(id),
  exam_type_id INTEGER NOT NULL REFERENCES school_management.exam_type(id),
  grade DECIMAL NOT NULL,
  grading_date DATE NOT NULL
);

-- Additional tables such as Attendance and ClassSchedule need to be defined further.
-- Assuming basic columns for demonstration:

-- Table: Attendance
DROP TABLE IF EXISTS school_management.attendance CASCADE;
CREATE TABLE school_management.attendance (
  id SERIAL PRIMARY KEY,
  student_enrollment_id INTEGER NOT NULL REFERENCES school_management.student_enrollment(id),
  date DATE NOT NULL,
  status VARCHAR(10) NOT NULL -- e.g., "Present", "Absent", "Excused"
);

-- Table: ClassSchedule
DROP TABLE IF EXISTS school_management.class_schedule CASCADE;
CREATE TABLE school_management.class_schedule (
  id SERIAL PRIMARY KEY,
  class_group_id INTEGER NOT NULL REFERENCES school_management.class_group(id),
  day_of_week VARCHAR(10) NOT NULL, -- e.g., "Monday", "Tuesday"
  start_time TIME NOT NULL,
  end_time TIME NOT NULL
);

