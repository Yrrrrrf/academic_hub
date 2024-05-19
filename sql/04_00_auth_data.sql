-- AUTH SCHEMA DATA
-- This scirpt defines some basic data for the AUTH schema

INSERT INTO public.general_user (name, email, password) VALUES
    ('some-new-admin', 'admin@localhost.mx', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFkbWluQGxvY2FsaG9zdCIsInBhc3N3b3JkIjoic29tZV9hZG1pbl9wYXNzd29yZCJ9.rYLNzcVDGqeaZO8LCR6X1baO5iXroOsV1FKltzYrHGA'),
    -- my name...
    ('Fernando Reza', 'frezac001@alumno.uaemex.mx', 'some_generic_password'),
    -- test data
    ('Jorge López', 'jlopec@alumno.uaemex.mx', 'some_generic_password'),
    ('Carmen González', 'cgonzl@alumno.uaemex.mx', 'some_generic_password'),
    ('Luis López', 'llopev@alumno.uaemex.mx', 'some_generic_password'),
    ('Erick Lara', 'elaraw@alumno.uaemex.mx', 'some_generic_password'),
    ('Juan Fuentes', 'jfueno@alumno.uaemex.mx', 'some_generic_password'),
    -- some additional test data
    ('Juan Pérez', 'jperezd001@alumno.uaemex.mx', 'some_generic_password'),
    ('María González', 'mgonzp001@alumno.uaemex.mx', 'some_generic_password')
;
