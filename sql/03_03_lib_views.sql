-- ******************************************************************
-- * Academic Hub - Library Management System Views
-- * Description: This file contains views for summarizing and
-- *              presenting library management data in a user-friendly manner.
-- ******************************************************************

-- View: vw_book_details
-- Description: Shows details of all books including authors, publisher, topics, and inventory.
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
    f.name AS faculty,
    COUNT(bl.book_series_id) AS copies
  FROM library_management.book_library bl
  JOIN infrastructure_management.library l ON bl.library_id = l.id
  JOIN infrastructure_management.faculty f ON l.faculty_id = f.id
  GROUP BY bl.book_id, f.name
)
SELECT
  d.title,
  d.authors,
  d.publisher,
  d.topics,
  string_agg(i.faculty || ' ' || i.copies || ' copies', ', ') AS inventory
FROM book_details d
JOIN inventory i ON d.id = i.book_id
GROUP BY d.title, d.authors, d.publisher, d.topics;

-- View: vw_loan_details
-- Description: Shows details of loans including member, book, faculty, loan date, and return date.
CREATE OR REPLACE VIEW library_management.vw_loan_details AS
SELECT
  l.id AS "Loan",
  gu.name AS "Member",
  b.name AS "Book",
  f.name AS "Faculty",
  l.loan_date AS "Loan Date",
  l.return_date AS "Return Date"
FROM library_management.loan l
JOIN school_management.student s ON l.student_id = s.id
JOIN public.general_user gu ON s.id = gu.id
JOIN library_management.book_library bl ON l.book_library_id = bl.book_series_id
JOIN library_management.book b ON bl.book_id = b.id
JOIN infrastructure_management.library lb ON bl.library_id = lb.id
JOIN infrastructure_management.faculty f ON lb.faculty_id = f.id;

-- View: vw_library_book_inventory
-- Description: Shows inventory details of books in different faculties.
CREATE OR REPLACE VIEW library_management.vw_library_book_inventory AS
SELECT
  bl.book_series_id,
  b.name AS book_name,
  f.name AS faculty_name
FROM library_management.book_library bl
JOIN library_management.book b ON bl.book_id = b.id
JOIN infrastructure_management.library l ON bl.library_id = l.id
JOIN infrastructure_management.faculty f ON l.faculty_id = f.id;

-- View: vw_academic_member_activities
-- Description: Shows activities of academic members including current and completed loans.
CREATE OR REPLACE VIEW library_management.vw_academic_member_activities AS
SELECT
  gu.name AS "Member",
  COUNT(l.id) FILTER (WHERE l.return_date IS NULL) AS "Current Loans",
  COUNT(l.id) FILTER (WHERE l.return_date IS NOT NULL) AS "Completed Loans"
FROM school_management.student s
JOIN public.general_user gu ON s.id = gu.id
LEFT JOIN library_management.loan l ON s.id = l.student_id
GROUP BY gu.name;

-- ******************************************************************
-- * New Views
-- ******************************************************************

-- View: vw_overdue_loans
-- Description: Shows details of overdue loans including member, book, faculty, and due date.
CREATE OR REPLACE VIEW library_management.vw_overdue_loans AS
SELECT
  l.id AS "Loan",
  gu.name AS "Member",
  b.name AS "Book",
  f.name AS "Faculty",
  l.loan_date AS "Loan Date",
  l.return_date AS "Return Date",
  CURRENT_DATE - l.loan_date AS "Days Overdue"
FROM library_management.loan l
JOIN school_management.student s ON l.student_id = s.id
JOIN public.general_user gu ON s.id = gu.id
JOIN library_management.book_library bl ON l.book_library_id = bl.book_series_id
JOIN library_management.book b ON bl.book_id = b.id
JOIN infrastructure_management.library lb ON bl.library_id = lb.id
JOIN infrastructure_management.faculty f ON lb.faculty_id = f.id
WHERE l.return_date IS NULL AND CURRENT_DATE > l.loan_date + INTERVAL '30 days';

-- View: vw_popular_books
-- Description: Shows the most frequently borrowed books.
CREATE OR REPLACE VIEW library_management.vw_popular_books AS
SELECT
  b.name AS book_name,
  COUNT(l.id) AS loan_count
FROM library_management.loan l
JOIN library_management.book_library bl ON l.book_library_id = bl.book_series_id
JOIN library_management.book b ON bl.book_id = b.id
GROUP BY b.name
ORDER BY loan_count DESC;

-- View: vw_library_utilization
-- Description: Shows the utilization of libraries by counting the number of books available.
CREATE OR REPLACE VIEW library_management.vw_library_utilization AS
SELECT
  f.name AS faculty_name,
  COUNT(bl.book_series_id) AS total_books,
  COUNT(l.id) FILTER (WHERE lb.return_date IS NULL) AS total_books_on_loan
FROM infrastructure_management.library l
JOIN library_management.book_library bl ON l.id = bl.library_id
JOIN infrastructure_management.faculty f ON l.faculty_id = f.id
LEFT JOIN library_management.loan lb ON bl.book_series_id = lb.book_library_id
GROUP BY f.name;


-- Example usage:
SELECT * FROM library_management.vw_book_details;
SELECT * FROM library_management.vw_loan_details;
SELECT * FROM library_management.vw_popular_books;

-- todo: Modify it to show the number of copies available in each library. (Now is just showing the book many times)
SELECT * FROM library_management.vw_library_book_inventory;

-- todo: Check if this works well
SELECT * FROM library_management.vw_academic_member_activities;
SELECT * FROM library_management.vw_overdue_loans;
SELECT * FROM library_management.vw_library_utilization;  -- check the `total_book_on_loan` column...









SELECT *
FROM information_schema.tables
WHERE table_schema = 'public'
  AND table_name = 'general_user';
