ALTER TABLE pose_sets
DROP COLUMN pose_1;

ALTER TABLE pose_sets
DROP COLUMN pose_2;

ALTER TABLE pose_sets
DROP COLUMN pose_3;

ALTER TABLE pose_sets
DROP COLUMN pose_4;

CREATE TABLE
    pose_sets_poses (
        set_id BIGINT NOT NULL REFERENCES pose_sets (id) ON DELETE CASCADE,
        pose_id BIGINT NOT NULL REFERENCES poses (id) ON DELETE CASCADE,
        created_at TIMESTAMP
        WITH
            TIME ZONE DEFAULT timezone ('utc'::TEXT, NOW ()) NOT NULL,
            PRIMARY KEY (set_id, pose_id)
    );

ALTER TABLE pose_sets_poses ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Enable read access for all users" ON pose_sets_poses AS PERMISSIVE FOR ALL TO public USING (true);