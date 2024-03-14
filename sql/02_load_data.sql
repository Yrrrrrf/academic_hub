-- Load the data into the tables
-- This script loads the data into the tables for the library database.

-- * Insert  (for basic tables (that ones without foreign keys inside them))

-- Inserting data into autor
-- DELETE FROM autor; ALTER SEQUENCE autor_id_seq RESTART WITH 1;
INSERT INTO autor (nombre) VALUES
('Robert W. Johnson'),
('Steve Maguire'),
('Roger G. Schroeder'),
('Richard Bronson'),
('Katsuhiko Ogata'),
('Michael Hammer'),
('James Champy')
;

-- Inserting data into biblioteca
-- DELETE FROM biblioteca; ALTER SEQUENCE biblioteca_id_seq RESTART WITH 1;
INSERT INTO biblioteca (nombre) VALUES
('Ingeniería'),
('Contaduría'),
('Economía'),
('Arquitectura'),
('Derecho')
;

-- Inserting data into editorial
-- DELETE FROM editorial; ALTER SEQUENCE editorial_id_seq RESTART WITH 1;
INSERT INTO editorial (nombre) VALUES
('CECSA'),
('McGraw-Hill'),
('Prentice Hall'),
('Grupo Editorial Norma')
;

-- Inserting data into libro
-- Assume that the editorial_id is the same as the order of the insertions
-- DELETE FROM libro; ALTER SEQUENCE libro_id_seq RESTART WITH 1;
INSERT INTO libro (nombre, editorial_id, ISBN) VALUES
('Administración Financiera', 1, NULL),
('Código sin errores', 2, NULL),
('Administración de Operaciones', 2, NULL),
('Investigación de Operaciones', 2, NULL),
('Ingeniería de Control Moderna', 3, NULL),
('Reingeniería', 4, NULL)
;

-- Inserting data into usuario
-- DELETE FROM usuario; ALTER SEQUENCE usuario_id_seq RESTART WITH 1;
INSERT INTO usuario (nombre) VALUES
('Jorge López'),
('Carmen González'),
('Luis López'),
('Erick Lara'),
('Juan Fuentes')
;

-- Inserting data into tema
-- DELETE FROM tema; ALTER SEQUENCE tema_id_seq RESTART WITH 1;
INSERT INTO tema (nombre) VALUES
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


-- * Inserting data into the "complex" tables (that ones that have foreign keys to other tables)

-- Inserting data into libro_autor
INSERT INTO libro_autor (libro_id, autor_id) VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(4, 3),
(5, 5),
(6, 6),
(6, 7);

-- Inserting data into libro_tema
INSERT INTO libro_tema (libro_id, tema_id) VALUES
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

-- Inserting data into libro_biblioteca
-- DELETE FROM libro_biblioteca; ALTER SEQUENCE libro_biblioteca_libro_no_serie_id_seq RESTART WITH 1;
INSERT INTO libro_biblioteca (libro_id, biblioteca_id) VALUES
(1, 5), (1, 5), (1, 1), (1, 1), (1, 1), (1, 2), (1, 3),
(2, 1), (2, 1), (2, 2), (2, 2), (2, 3),
(3, 1), (3, 1), (3, 1), (3, 2), (3, 2), (3, 3), (3, 3), (3, 4),
(4, 1), (4, 1), (4, 2), (4, 2), (4, 2), (4, 3), (4, 4), (4, 4),
(5, 1), (5, 1), (5, 1),
(6, 1), (6, 1), (6, 2), (6, 2), (6, 2)
;

-- Inserting data into prestamo
-- DELETE FROM prestamo; ALTER SEQUENCE prestamo_id_seq RESTART WITH 1;
INSERT INTO prestamo (id, id_usuario, id_libro_biblioteca, fecha_prestamo, fecha_devolucion) VALUES
(83, 1,  3, '2023-02-09', '2023-02-11'),
(84, 1, 32, '2023-02-09', '2023-02-14'),
(85, 2, 33, '2023-02-09', '2023-02-11'),
(86, 3, 34, '2023-02-11', '2023-02-14'),
(88, 4, 26, '2023-02-11', '2023-02-16'),
(89, 5, 13, '2023-02-11', '2023-02-13'),
(90, 4, 14, '2023-02-11', '2023-02-16')
;