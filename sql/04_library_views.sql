-- This sql file adds the views to the library database.

-- Create a view that shows the details of the books (all books)
CREATE OR REPLACE VIEW vw_book_details AS
WITH book_details AS (
  SELECT
    b.id,
    b.name AS title,
    string_agg(DISTINCT a.name, ', ') AS authors,
    p.name AS publisher,
    string_agg(DISTINCT t.name, ', ') AS topics
  FROM book b
  JOIN book_author ba ON b.id = ba.book_id
  JOIN author a ON ba.author_id = a.id
  JOIN publisher p ON b.publisher_id = p.id
  JOIN book_topic bt ON b.id = bt.book_id
  JOIN topic t ON bt.topic_id = t.id
  GROUP BY b.id, p.name
), inventory AS (
  SELECT
    bl.book_id,
    l.name AS library,
    COUNT(bl.book_series_id) AS copies
  FROM book_library bl
  JOIN library l ON bl.library_id = l.id
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

-- Use the view to list all the book data
    -- SELECT * FROM vw_book_details;
-- Select a specific book from this view
    -- SELECT * FROM vw_book_details WHERE title = 'Reengineering';
    -- SELECT * FROM vw_book_details WHERE authors LIKE '%Peter Drucker%';


CREATE OR REPLACE VIEW vw_loan_details AS
SELECT
  l.id AS "Loan",
  am.name AS "Member",
  b.name AS "Book",
  lb.name AS "Library",
  l.loan_date AS "Loan Date",
  l.return_date AS "Return Date"
FROM loan l
JOIN academic_member am ON l.academic_member_id = am.id
JOIN book_library bl ON l.book_library_id = bl.book_series_id
JOIN book b ON bl.book_id = b.id
JOIN library lb ON bl.library_id = lb.id;

-- Use the view to list all the loan data
    -- SELECT * FROM vw_loan_details;
-- Select a specific book from this view
    -- SELECT * FROM vw_loan_details WHERE "Book" = 'Reengineering';
    -- SELECT * FROM vw_loan_details WHERE "Loan" = 84;

-- List all the books in all the libraries
CREATE OR REPLACE VIEW vw_library_book_inventory AS
SELECT bl.book_series_id, b.name AS book_name, l.name AS library_name
FROM book_library bl
JOIN book b ON bl.book_id = b.id
JOIN library l ON bl.library_id = l.id;

-- Another useful view: Academic member activities
CREATE OR REPLACE VIEW vw_academic_member_activities AS
SELECT
  am.name AS "Member",
  COUNT(l.id) FILTER (WHERE l.return_date IS NULL) AS "Current Loans",
  COUNT(l.id) FILTER (WHERE l.return_date IS NOT NULL) AS "Completed Loans"
FROM academic_member am
LEFT JOIN loan l ON am.id = l.academic_member_id
GROUP BY am.name;

-- To use the additional view to list all academic member activities
    -- SELECT * FROM vw_academic_member_activities;
