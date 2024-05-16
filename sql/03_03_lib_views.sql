-- Assuming your structure and schemas have been set up as described

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