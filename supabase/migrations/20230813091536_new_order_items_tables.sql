-- ========================= CREATE OrderItemStatus TYPE =============================
CREATE TYPE orderItemStatus AS ENUM (
    'WAITING',
    'IN_PROCESS',
    'COMPLETED',
    'CANCELLED',
    'FAILED'
);

-- ========================= CREATE Orders Item TABLE =============================
CREATE TABLE
    order_items (
        order_id BIGINT NOT NULL REFERENCES orders (id) ON DELETE CASCADE,
        item_id INTEGER NOT NULL,
        img_input BIGINT NOT NULL REFERENCES images (id) ON DELETE SET NULL,
        img_output BIGINT NULL REFERENCES images (id) ON DELETE SET NULL,
        input_metadata JSONB NULL,
        output_metadata JSONB NULL,
        status orderItemStatus NULL DEFAULT 'WAITING',
        PRIMARY KEY (order_id, item_id)
    ) TABLESPACE pg_default;

ALTER TABLE order_items ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Enable read access for all users" ON order_items AS PERMISSIVE FOR ALL TO public USING (true);