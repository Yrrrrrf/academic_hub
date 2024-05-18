-- AUTH SCHEMA DATA
-- This scirpt defines some basic data for the AUTH schema


INSERT INTO auth.general_user (name, email, password_hash, additional_info)
VALUES (
        'some-new-admin',
        'admin@localhost.mx',
        -- current password is 'some_admin_password' (it will change if I modify the SECRET_KEY in the .env file)
        'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFkbWluQGxvY2FsaG9zdCIsInBhc3N3b3JkIjoic29tZV9hZG1pbl9wYXNzd29yZCJ9.rYLNzcVDGqeaZO8LCR6X1baO5iXroOsV1FKltzYrHGA',
        '{
            "role": "ADMIN"
        }'
);
