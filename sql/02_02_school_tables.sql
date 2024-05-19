--? SCHOOL MANAGEMENT SYSTEM --------------------------------------------------------------------------------------------

-- Table: Program
DROP TABLE IF EXISTS school_management.program CASCADE;
CREATE TABLE school_management.program (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  school_id INTEGER NOT NULL REFERENCES infrastructure_management.faculty(id)
);

-- Table: Student
DROP TABLE IF EXISTS school_management.student CASCADE;
-- Student Table with reference to GeneralUser
CREATE TABLE IF NOT EXISTS school_management.student (
  id INTEGER PRIMARY KEY REFERENCES public.general_user(id),
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

-- Table: Grade
DROP TABLE IF EXISTS school_management.grade CASCADE;
CREATE TABLE school_management.grade (
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
  classroom_id INTEGER NOT NULL REFERENCES infrastructure_management.room(id),
  day_of_week VARCHAR(10) NOT NULL, -- e.g., "Monday", "Tuesday" (9 characters max (Saturday))
  start_time TIME NOT NULL,
  end_time TIME NOT NULL
);
