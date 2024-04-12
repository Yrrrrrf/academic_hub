-- Assuming your structure and schemas have been set up as described




-- GENERAL SYSTEMS --------------------------------------------------
--     add some...




-- LIBRARY MANAGEMENT SYSTEM --------------------------------------------------

-- Create a view that shows the details of the books (all books)
CREATE OR REPLACE VIEW library_management.vw_book_details AS
WITH book_details AS (
  SELECT
    b.id,
    b.name AS title,
    string_agg(DISTINCT a.name, ', ') AS authors,
    p.name AS publisher,
    string_agg(DISTINCT t.name, ', ') AS topics
  FROM library_management.book b
  JOIN library_management.book_author ba ON b.id = ba.book_id
  JOIN library_management.author a ON ba.author_id = a.id
  JOIN library_management.publisher p ON b.publisher_id = p.id
  JOIN library_management.book_topic bt ON b.id = bt.book_id
  JOIN library_management.topic t ON bt.topic_id = t.id
  GROUP BY b.id, p.name
), inventory AS (
  SELECT
    bl.book_id,
    l.name AS library,
    COUNT(bl.book_series_id) AS copies
  FROM library_management.book_library bl
  JOIN library_management.library l ON bl.library_id = l.id
  GROUP BY bl.book_id, l.name
)
SELECT
  d.title,
  d.authors,
  d.publisher,
  d.topics,
  string_agg(i.library || ' ' || i.copies || ' copies', ', ') AS inventory
FROM book_details d
JOIN inventory i ON d.id = i.book_id
GROUP BY d.title, d.authors, d.publisher, d.topics;

-- Create a view for loan details
CREATE OR REPLACE VIEW library_management.vw_loan_details AS
SELECT
  l.id AS "Loan",
  (SELECT name FROM general_dt.general_user WHERE id = am.id) AS "Member",
  b.name AS "Book",
  lb.name AS "Library",
  l.loan_date AS "Loan Date",
  l.return_date AS "Return Date"
FROM library_management.loan l
JOIN library_management.academic_member am ON l.academic_member_id = am.id
JOIN library_management.book_library bl ON l.book_library_id = bl.book_series_id
JOIN library_management.book b ON bl.book_id = b.id
JOIN library_management.library lb ON bl.library_id = lb.id;

-- Create a view for library book inventory
CREATE OR REPLACE VIEW library_management.vw_library_book_inventory AS
SELECT bl.book_series_id, b.name AS book_name, l.name AS library_name
FROM library_management.book_library bl
JOIN library_management.book b ON bl.book_id = b.id
JOIN library_management.library l ON bl.library_id = l.id;

-- Create a view for academic member activities
CREATE OR REPLACE VIEW library_management.vw_academic_member_activities AS
SELECT
  (SELECT name FROM general_dt.general_user WHERE id = am.id) AS "Member",
  COUNT(l.id) FILTER (WHERE l.return_date IS NULL) AS "Current Loans",
  COUNT(l.id) FILTER (WHERE l.return_date IS NOT NULL) AS "Completed Loans"
FROM library_management.academic_member am
LEFT JOIN library_management.loan l ON am.id = l.academic_member_id
GROUP BY am.id;

-- Example of usage
SELECT * FROM library_management.vw_book_details;
SELECT * FROM library_management.vw_loan_details;
SELECT * FROM library_management.vw_library_book_inventory;



-- SCHOOL MANAGEMENT SYSTEM --------------------------------------------------
CREATE OR REPLACE VIEW school_management.vw_program_enrollment AS
SELECT
    p.id AS program_id,
    p.name AS program_name,
    COUNT(s.id) AS total_students
FROM school_management.program p
JOIN school_management.student s ON p.id = s.program_id
GROUP BY p.id;

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




CREATE OR REPLACE VIEW school_management.vw_class_students_grades AS
SELECT
    cg.id AS class_group_id,
    sub.name AS subject,
    s.id AS student_id,
    (SELECT name FROM general_dt.general_user WHERE id = s.id) AS student_name,
    array_agg(g.grade) AS grades,
    array_agg(et.name) AS exam_types
FROM school_management.student_enrollment se
JOIN school_management.student s ON se.student_id = s.id
JOIN school_management.class_group cg ON se.class_group_id = cg.id
JOIN school_management.subject sub ON cg.subject_id = sub.id
LEFT JOIN school_management.grades g ON se.id = g.student_enrollment_id
LEFT JOIN school_management.exam_type et ON g.exam_type_id = et.id
GROUP BY cg.id, sub.name, s.id;


CREATE OR REPLACE VIEW school_management.vw_student_enrollment_history AS
SELECT
    s.id AS student_id,
    (SELECT name FROM general_dt.general_user WHERE id = s.id) AS student_name,
    array_agg(sub.name) AS subjects,
    array_agg(ap.name) AS academic_periods
FROM school_management.student_enrollment se
JOIN school_management.student s ON se.student_id = s.id
JOIN school_management.class_group cg ON se.class_group_id = cg.id
JOIN school_management.subject sub ON cg.subject_id = sub.id
JOIN school_management.academic_period ap ON cg.period_id = ap.id
GROUP BY s.id;


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


-- Example of usage
SELECT * FROM school_management.vw_program_enrollment;
SELECT * FROM school_management.vw_class_schedule;

SELECT * FROM school_management.vw_class_students_grades;
-- todo: add a better way to represent the subjects taken in each academic period
SELECT * FROM school_management.vw_student_enrollment_history;
-- todo: add the order by clause
SELECT * FROM school_management.vw_class_schedule_instructor;


CREATE OR REPLACE VIEW school_management.vw_student_performance AS
SELECT
    s.id AS student_id,
    (SELECT name FROM general_dt.general_user WHERE id = s.id) AS student_name,
    sub.name AS subject,
    AVG(g.grade) AS average_grade
FROM school_management.grades g
JOIN school_management.student_enrollment se ON g.student_enrollment_id = se.id
JOIN school_management.class_group cg ON se.class_group_id = cg.id
JOIN school_management.subject sub ON cg.subject_id = sub.id
JOIN school_management.student s ON se.student_id = s.id
GROUP BY s.id, sub.name
ORDER BY s.id, AVG(g.grade) DESC;


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


-- Example of usage
SELECT * FROM school_management.vw_student_performance;
SELECT * FROM school_management.vw_class_attendance_rates;
SELECT * FROM school_management.vw_instructor_load;
