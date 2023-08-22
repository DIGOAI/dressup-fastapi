ALTER TABLE orders
ADD COLUMN metadata JSONB NULL;

ALTER TABLE order_items
DROP COLUMN metadata;

ALTER TABLE order_items
DROP COLUMN status;

DROP TYPE orderItemStatus;