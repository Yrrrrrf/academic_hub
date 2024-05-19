-- AUTH SCHEMA DATA
-- This scirpt defines some basic data for the AUTH schema

INSERT INTO public.general_user (name, email, password) VALUES
    ('Etesech Penchs', 'some@example.com', '$2b$12$rFF3ukS9uwUP6BCflhCbVetzEV56HClCYeanpdGd2UdIDYKrTZoi6'),
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
