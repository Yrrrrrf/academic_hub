
INSERT INTO school_management.program (name, school_id) VALUES
-- Engineering Programs
    ('Computer Science', 1),  -- Assuming a school with ID = 1 exists
    ('Mechanical Engineering', 1),
    ('Industrial Engineering', 1),
    ('Artificial Intelligence', 1),
    ('Civil Engineering', 1),
-- Social Sciences Programs
    ('Sociology', 1),
    ('Psychology', 1),
    ('Environmental Science', 1),
    ('Political Science', 1),
-- Economics Programs
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

INSERT INTO school_management.grade (student_enrollment_id, exam_type_id, grade, grading_date) VALUES
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

INSERT INTO school_management.class_schedule (class_group_id, classroom_id, day_of_week, start_time, end_time) VALUES
    (1, 1, 'Monday', '08:00', '10:00'),
    (1, 1, 'Wednesday', '08:00', '10:00'),
    (1, 2, 'Friday', '08:00', '10:00'),
    (2, 2, 'Monday', '10:00', '12:00'),
    (2, 3, 'Wednesday', '10:00', '12:00'),
    (2, 3, 'Friday', '10:00', '12:00'),
    (3, 4, 'Monday', '14:00', '16:00'),
    (3, 4, 'Wednesday', '14:00', '16:00'),
    (3, 4, 'Friday', '14:00', '16:00'),
    (4, 5, 'Tuesday', '08:00', '10:00'),
    (4, 5, 'Thursday', '08:00', '10:00'),
    (4, 5, 'Saturday', '08:00', '10:00'),
    (5, 6, 'Tuesday', '10:00', '12:00'),
    (5, 6, 'Thursday', '10:00', '12:00'),
    (5, 6, 'Saturday', '10:00', '12:00')
;
