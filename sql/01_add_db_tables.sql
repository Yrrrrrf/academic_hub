-- Create the database structure for the library database
-- This script creates the tables and relationships for the library database.

-- Table: autor
DROP TABLE IF EXISTS autor CASCADE;
CREATE TABLE autor (
  id SERIAL PRIMARY KEY,
  nombre VARCHAR(255) NOT NULL
);

-- Table: biblioteca
DROP TABLE IF EXISTS biblioteca CASCADE;
CREATE TABLE biblioteca (
  id SERIAL PRIMARY KEY,
  nombre VARCHAR(255) NOT NULL
);

-- Table: editorial
DROP TABLE IF EXISTS editorial CASCADE;
CREATE TABLE editorial (
  id SERIAL PRIMARY KEY,
  nombre VARCHAR(255) NOT NULL
);

-- Table: libro
DROP TABLE IF EXISTS libro CASCADE;
CREATE TABLE libro (
  id SERIAL PRIMARY KEY,
  nombre VARCHAR(255) NOT NULL,
  editorial_id INTEGER REFERENCES editorial(id),
  ISBN VARCHAR(13)  -- ISBN is a 13-digit number
);

-- Table: libro_autor
DROP TABLE IF EXISTS libro_autor CASCADE;
CREATE TABLE libro_autor (
  libro_id INTEGER NOT NULL REFERENCES libro(id),
  autor_id INTEGER NOT NULL REFERENCES autor(id),
  PRIMARY KEY (libro_id, autor_id)
);

-- Table: tema
DROP TABLE IF EXISTS tema CASCADE;
CREATE TABLE tema (
  id SERIAL PRIMARY KEY,
  nombre VARCHAR(255) NOT NULL
);

-- Table: libro_tema
DROP TABLE IF EXISTS libro_tema CASCADE;
CREATE TABLE libro_tema (
  libro_id INTEGER NOT NULL REFERENCES libro(id),
  tema_id INTEGER NOT NULL REFERENCES tema(id),
  PRIMARY KEY (libro_id, tema_id)
);

-- Table: libro_biblioteca
DROP TABLE IF EXISTS libro_biblioteca CASCADE;
CREATE TABLE libro_biblioteca (
  libro_no_serie_id SERIAL PRIMARY KEY,
  libro_id INTEGER NOT NULL REFERENCES libro(id),
  biblioteca_id INTEGER NOT NULL REFERENCES biblioteca(id)
);

-- Table: usuario
DROP TABLE IF EXISTS usuario CASCADE;
CREATE TABLE usuario (
  id SERIAL PRIMARY KEY,
  nombre VARCHAR(255) NOT NULL
);

-- Table: prestamo
DROP TABLE IF EXISTS prestamo CASCADE;
CREATE TABLE prestamo (
  id SERIAL PRIMARY KEY,
  id_usuario INTEGER NOT NULL REFERENCES usuario(id),
  id_libro_biblioteca INTEGER REFERENCES libro_biblioteca(libro_no_serie_id),
  fecha_prestamo DATE,
  fecha_devolucion DATE
);

-- Insert statements are omitted for brevity. Use similar INSERT INTO statements as in the MySQL script.
