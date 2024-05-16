--? LIBRARY MANAGEMENT -----------------------------------------------------------

-- * Insert  (for basic tables (that ones without foreign keys inside them))

-- Inserting data INTO library_management.author
INSERT INTO library_management.author (name) VALUES
    ('Robert W. Johnson'),
    ('Steve Maguire'),
    ('Roger G. Schroeder'),
    ('Richard Bronson'),
    ('Katsuhiko Ogata'),
    ('Michael Hammer'),
    ('James Champy')
;

-- Inserting data INTO library_management.publisher
INSERT INTO library_management.publisher (name) VALUES
    ('CECSA'),
    ('McGraw-Hill'),
    ('Prentice Hall'),
    ('Grupo Editorial Norma')
;

-- Inserting data INTO library_management.book
INSERT INTO library_management.book (name, publisher_id, ISBN) VALUES
    ('Administración Financiera', 1, NULL),
    ('Código sin errores', 2, NULL),
    ('Administración de Operaciones', 2, NULL),
    ('Investigación de Operaciones', 2, NULL),
    ('Ingeniería de Control Moderna', 3, NULL),
    ('Reingeniería', 4, NULL)
;

-- Inserting data INTO library_management.topic
INSERT INTO library_management.topic (name) VALUES
    ('Administración'),
    ('Planeación'),
    ('Finanzas'),
    ('Organización'),
    ('Sistemas'),
    ('Programación'),
    ('Procesos'),
    ('Programación Lineal'),
    ('Teoria de Juegos'),
    ('Sistemas de Control'),
    ('Transformadas'),
    ('Matrices'),
    ('Optimización'),
    ('Reingeniería')
;


-- * Inserting data INTO library_management.the "complex" tables (those that have foreign keys to other tables)

-- Inserting data INTO library_management.book_author
INSERT INTO library_management.book_author (book_id, author_id) VALUES
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (4, 3),
    (5, 5),
    (6, 6),
    (6, 7)
;

-- Inserting data INTO library_management.book_topic
INSERT INTO library_management.book_topic (book_id, topic_id) VALUES
    (1, 1),
    (1, 2),
    (1, 3),
    (1, 4),
    (2, 5),
    (2, 6),
    (3, 1),
    (3, 2),
    (3, 7),
    (4, 8),
    (4, 9),
    (4, 5),
    (5, 10),
    (5, 11),
    (5, 12),
    (5, 13),
    (6, 7),
    (6, 5),
    (6, 14)
;

-- Inserting data INTO library_management.book_library
INSERT INTO library_management.book_library (book_id, library_id) VALUES
    (1, 6), (1, 6), (1, 1), (1, 1), (1, 1), (1, 2), (1, 3),
    (2, 1), (2, 1), (2, 2), (2, 2), (2, 3),
    (3, 1), (3, 1), (3, 1), (3, 2), (3, 2), (3, 3), (3, 3), (3, 4),
    (4, 1), (4, 1), (4, 2), (4, 2), (4, 2), (4, 3), (4, 4), (4, 4),
    (5, 1), (5, 1), (5, 1),
    (6, 1), (6, 1), (6, 2), (6, 2), (6, 2)
;

-- Inserting data INTO library_management.loan
INSERT INTO library_management.loan (id, student_id, book_library_id, loan_date, return_date) VALUES
    (83, 1,  3, '2023-02-09', '2023-02-11'),
    (84, 1, 32, '2023-02-09', '2023-02-14'),
    (85, 2, 33, '2023-02-09', '2023-02-11'),
    (86, 3, 34, '2023-02-11', '2023-02-14'),
    (88, 4, 26, '2023-02-11', '2023-02-16'),
    (89, 5, 13, '2023-02-11', '2023-02-13'),
    (90, 4, 14, '2023-02-11', '2023-02-16')
;
