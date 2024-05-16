-- ? LIBRARY MANAGEMENT SYSTEM -------------------------------------------------------------------------------------------

-- Table: author
DROP TABLE IF EXISTS library_management.author CASCADE;
CREATE TABLE library_management.author (
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
  library_id INTEGER NOT NULL REFERENCES infrastructure_management.library(id)
);

-- Table: loan
DROP TABLE IF EXISTS library_management.loan CASCADE;
CREATE TABLE library_management.loan (
  id SERIAL PRIMARY KEY,
  student_id INTEGER NOT NULL REFERENCES school_management.student(id),
  book_library_id INTEGER REFERENCES library_management.book_library(book_series_id),
  loan_date DATE,
  return_date DATE
);
