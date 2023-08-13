-- ========================= CREATE Orders Poses BETWEEN TABLE =============================
CREATE TABLE
    orders_poses (
        order_id BIGINT NOT NULL REFERENCES orders (id) ON DELETE CASCADE,
        pose_id BIGINT NOT NULL REFERENCES poses (id) ON DELETE CASCADE,
        PRIMARY KEY (order_id, pose_id)
    ) TABLESPACE pg_default;

ALTER TABLE orders_poses ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Enable read access for all users" ON orders_poses AS PERMISSIVE FOR ALL TO public USING (true);