-- AUTH SCHEMA DATA
-- This scirpt defines some basic data for the AUTH schema


INSERT INTO auth.general_user (name, email, password_hash, additional_info)
VALUES (
        'some-new-admin',
        'admin@localhost',
        'some_admin_password',
        '{
            "role": "ADMIN"
        }'
);
