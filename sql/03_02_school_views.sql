-- ******************************************************************
-- * Academic Hub - School Management System Views
-- * Description: This file contains views for summarizing and
-- *              presenting data in a user-friendly manner.
-- ******************************************************************

-- View: vw_program_enrollment
-- Description: Summarizes the number of students enrolled in each program.
CREATE OR REPLACE VIEW school_management.vw_program_enrollment AS
SELECT
    p.id AS program_id,
    p.name AS program_name,
    COUNT(s.id) AS total_students
FROM school_management.program p
JOIN school_management.student s ON p.id = s.program_id
GROUP BY p.id;

-- View: vw_class_schedule
-- Description: Provides details of class schedules, including subject, instructor,
--              academic period, and the number of enrolled students.
CREATE OR REPLACE VIEW school_management.vw_class_schedule AS
SELECT
    cg.id AS class_group_id,
    sub.name AS subject,
    ins.name AS instructor_name,
    ap.name AS academic_period,
    COUNT(se.student_id) AS enrolled_students,
    cs.day_of_week,
    cs.start_time,
    cs.end_time
FROM school_management.class_group cg
JOIN school_management.subject sub ON cg.subject_id = sub.id
JOIN school_management.instructor ins ON cg.instructor_id = ins.id
JOIN school_management.academic_period ap ON cg.period_id = ap.id
LEFT JOIN school_management.student_enrollment se ON cg.id = se.class_group_id
LEFT JOIN school_management.class_schedule cs ON cg.id = cs.class_group_id
GROUP BY cg.id, sub.name, ins.name, ap.name, cs.day_of_week, cs.start_time, cs.end_time;

-- View: vw_class_students_grade
-- Description: Lists the grades of students in each class group, along with exam types.
CREATE OR REPLACE VIEW school_management.vw_class_students_grade AS
SELECT
    cg.id AS class_group_id,
    sub.name AS subject,
    s.id AS student_id,
    gu.name AS student_name,
    array_agg(g.grade) AS grade,
    array_agg(et.name) AS exam_types
FROM school_management.student_enrollment se
JOIN school_management.student s ON se.student_id = s.id
JOIN public.general_user gu ON s.id = gu.id
JOIN school_management.class_group cg ON se.class_group_id = cg.id
JOIN school_management.subject sub ON cg.subject_id = sub.id
LEFT JOIN school_management.grade g ON se.id = g.student_enrollment_id
LEFT JOIN school_management.exam_type et ON g.exam_type_id = et.id
GROUP BY cg.id, sub.name, s.id, gu.name;

-- View: vw_student_enrollment_history
-- Description: Shows the enrollment history of students, including subjects and academic periods.
CREATE OR REPLACE VIEW school_management.vw_student_enrollment_history AS
SELECT
    s.id AS student_id,
    gu.name AS student_name,
    array_agg(sub.name) AS subjects,
    array_agg(ap.name) AS academic_periods
FROM school_management.student_enrollment se
JOIN school_management.student s ON se.student_id = s.id
JOIN public.general_user gu ON s.id = gu.id
JOIN school_management.class_group cg ON se.class_group_id = cg.id
JOIN school_management.subject sub ON cg.subject_id = sub.id
JOIN school_management.academic_period ap ON cg.period_id = ap.id
GROUP BY s.id, gu.name;

-- View: vw_class_schedule_instructor
-- Description: Details of class schedules organized by instructor, including day of the week and time.
CREATE OR REPLACE VIEW school_management.vw_class_schedule_instructor AS
SELECT
    cg.id AS class_group_id,
    sub.name AS subject,
    ins.name AS instructor_name,
    ap.name AS academic_period,
    cs.day_of_week,
    cs.start_time,
    cs.end_time
FROM school_management.class_schedule cs
JOIN school_management.class_group cg ON cs.class_group_id = cg.id
JOIN school_management.subject sub ON cg.subject_id = sub.id
JOIN school_management.instructor ins ON cg.instructor_id = ins.id
JOIN school_management.academic_period ap ON cg.period_id = ap.id
ORDER BY cs.day_of_week, cs.start_time;

-- View: vw_student_performance
-- Description: Shows the average grades of students across different subjects.
CREATE OR REPLACE VIEW school_management.vw_student_performance AS
SELECT
    s.id AS student_id,
    gu.name AS student_name,
    sub.name AS subject,
    AVG(g.grade) AS average_grade
FROM school_management.grade g
JOIN school_management.student_enrollment se ON g.student_enrollment_id = se.id
JOIN school_management.class_group cg ON se.class_group_id = cg.id
JOIN school_management.subject sub ON cg.subject_id = sub.id
JOIN school_management.student s ON se.student_id = s.id
JOIN public.general_user gu ON s.id = gu.id
GROUP BY s.id, gu.name, sub.name
ORDER BY s.id, AVG(g.grade) DESC;

-- View: vw_class_attendance_rates
-- Description: Calculates attendance rates for each class group.
CREATE OR REPLACE VIEW school_management.vw_class_attendance_rates AS
SELECT
    cg.id AS class_group_id,
    sub.name AS subject,
    ap.name AS academic_period,
    ins.name AS instructor,
    COUNT(a.id) FILTER (WHERE a.status = 'Present') AS total_present,
    COUNT(a.id) FILTER (WHERE a.status = 'Absent') AS total_absent,
    (COUNT(a.id) FILTER (WHERE a.status = 'Present')::DECIMAL / COUNT(a.id)) * 100 AS attendance_rate
FROM school_management.attendance a
JOIN school_management.student_enrollment se ON a.student_enrollment_id = se.id
JOIN school_management.class_group cg ON se.class_group_id = cg.id
JOIN school_management.subject sub ON cg.subject_id = sub.id
JOIN school_management.academic_period ap ON cg.period_id = ap.id
JOIN school_management.instructor ins ON cg.instructor_id = ins.id
GROUP BY cg.id, sub.name, ap.name, ins.name;

-- View: vw_instructor_load
-- Description: Summarizes the workload of instructors, including the number of classes and subjects taught.
CREATE OR REPLACE VIEW school_management.vw_instructor_load AS
SELECT
    ins.id AS instructor_id,
    ins.name AS instructor_name,
    ap.name AS academic_period,
    COUNT(cg.id) AS total_classes,
    array_agg(DISTINCT sub.name) AS subjects_taught
FROM school_management.class_group cg
JOIN school_management.instructor ins ON cg.instructor_id = ins.id
JOIN school_management.subject sub ON cg.subject_id = sub.id
JOIN school_management.academic_period ap ON cg.period_id = ap.id
GROUP BY ins.id, ap.name
ORDER BY ins.id, COUNT(cg.id) DESC;

-- Example usage:
SELECT * FROM school_management.vw_program_enrollment;
SELECT * FROM school_management.vw_class_schedule;
SELECT * FROM school_management.vw_class_students_grade;
SELECT * FROM school_management.vw_student_enrollment_history;
SELECT * FROM school_management.vw_class_schedule_instructor;
SELECT * FROM school_management.vw_student_performance;
SELECT * FROM school_management.vw_class_attendance_rates;
SELECT * FROM school_management.vw_instructor_load;


SELECT table_name FROM information_schema.views WHERE table_schema = 'school_management';
