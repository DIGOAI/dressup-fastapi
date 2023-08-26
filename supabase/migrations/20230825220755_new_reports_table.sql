CREATE TYPE reportType AS ENUM (
    'MISREPRESENTATION_OF_CONTENT',
    'INAPPROPRIATE_CONTENT',
    'ACCURACY_ISSUES',
    'OTHER'
);

CREATE TABLE
    reports (
        id BIGSERIAL NOT NULL PRIMARY KEY,
        user_id UUID NOT NULL REFERENCES auth.users ON DELETE CASCADE,
        order_id BIGINT NOT NULL REFERENCES orders (id) ON DELETE CASCADE,
        type reportType NULL DEFAULT 'OTHER',
        description TEXT NULL,
        created_at TIMESTAMP
        WITH
            TIME ZONE DEFAULT timezone ('utc'::TEXT, NOW ()) NOT NULL
    );

ALTER TABLE reports ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Enable read access for all users" ON reports AS PERMISSIVE FOR ALL TO public USING (true);