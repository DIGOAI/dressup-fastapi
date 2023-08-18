DROP TABLE orders_poses;

CREATE TABLE
    pose_sets (
        id BIGSERIAL PRIMARY KEY,
        name VARCHAR(50) NOT NULL,
        pose_1 BIGINT NOT NULL REFERENCES poses (id) ON DELETE CASCADE,
        pose_2 BIGINT NOT NULL REFERENCES poses (id) ON DELETE CASCADE,
        pose_3 BIGINT NOT NULL REFERENCES poses (id) ON DELETE CASCADE,
        pose_4 BIGINT NOT NULL REFERENCES poses (id) ON DELETE CASCADE,
        created_at TIMESTAMP
        WITH
            TIME ZONE DEFAULT timezone ('utc'::TEXT, NOW ()) NOT NULL
    );

ALTER TABLE pose_sets ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Enable read access for all users" ON pose_sets AS PERMISSIVE FOR ALL TO public USING (true);


ALTER TABLE orders ADD COLUMN pose_set BIGINT NOT NULL REFERENCES pose_sets (id) ON DELETE CASCADE;