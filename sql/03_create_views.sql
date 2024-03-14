-- This sql file adds the views to the library database.

-- Create a view that shows the details of the books (all books)
CREATE OR REPLACE VIEW vw_libro_detalles AS
WITH libro_details AS (
  SELECT
    l.id,
    l.nombre AS titulo,
    string_agg(DISTINCT a.nombre, ', ') AS autores,
    e.nombre AS editorial,
    string_agg(DISTINCT t.nombre, ', ') AS temas
  FROM libro l
  JOIN libro_autor la ON l.id = la.libro_id
  JOIN autor a ON la.autor_id = a.id
  JOIN editorial e ON l.editorial_id = e.id
  JOIN libro_tema lt ON l.id = lt.libro_id
  JOIN tema t ON lt.tema_id = t.id
  GROUP BY l.id, e.nombre
), inventory AS (
  SELECT
    lb.libro_id,
    b.nombre AS biblioteca,
    COUNT(lb.libro_no_serie_id) AS ejemplares
  FROM libro_biblioteca lb
  JOIN biblioteca b ON lb.biblioteca_id = b.id
  GROUP BY lb.libro_id, b.nombre
)
SELECT
  d.titulo,
  d.autores,
  d.editorial,
  d.temas,
  string_agg(i.biblioteca || ' ' || i.ejemplares || ' ejemplares', ', ') AS inventario
FROM libro_details d
JOIN inventory i ON d.id = i.libro_id
GROUP BY d.titulo, d.autores, d.editorial, d.temas;

-- Use the view to list all the books data
    -- SELECT * FROM vw_libro_detalles;
-- Select an specific book of this view
    -- SELECT * FROM vw_libro_detalles WHERE titulo = 'Reingeniería';
    -- SELECT * FROM vw_libro_detalles WHERE autores = 'Peter Drucker';


CREATE OR REPLACE VIEW vw_detalles_prestamo AS
SELECT
  p.id AS "Préstamo",
  u.nombre AS "Usuario",
  l.nombre AS "Ejemplar",
  b.nombre AS "Biblioteca",
  p.fecha_prestamo AS "Fecha Préstamo",
  p.fecha_devolucion AS "Fecha Devolución"
FROM prestamo p
JOIN usuario u ON p.id_usuario = u.id
JOIN libro_biblioteca lb ON p.id_libro_biblioteca = lb.libro_no_serie_id
JOIN libro l ON lb.libro_id = l.id
JOIN biblioteca b ON lb.biblioteca_id = b.id;

-- Use the view to list all the books data
    -- SELECT * FROM vw_detalles_prestamo;
-- Select an specific book of this view
    -- SELECT * FROM vw_detalles_prestamo WHERE "Ejemplar" = 'Reingeniería';
    -- SELECT * FROM vw_detalles_prestamo WHERE "Préstamo" = 84;



-- todo: Create a view that shows the details of the books (all books)
-- List all the books in all the libraries
SELECT lb.libro_no_serie_id, l.nombre AS libro_nombre, b.nombre AS biblioteca_nombre
FROM libro_biblioteca lb
JOIN libro l ON lb.libro_id = l.id
JOIN biblioteca b ON lb.biblioteca_id = b.id
;
