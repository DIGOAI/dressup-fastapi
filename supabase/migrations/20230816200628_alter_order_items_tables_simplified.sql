CREATE TYPE orderType AS ENUM ('INPUT', 'OUTPUT');

ALTER TABLE order_items
ADD COLUMN type orderType NULL DEFAULT 'INPUT';

ALTER TABLE order_items
DROP COLUMN img_output;

ALTER TABLE order_items
DROP COLUMN output_metadata;

ALTER TABLE order_items
RENAME COLUMN img_input TO img;

ALTER TABLE order_items
RENAME COLUMN input_metadata TO metadata;

ALTER TABLE order_items
ALTER COLUMN item_id TYPE UUID USING gen_random_uuid (),
ALTER COLUMN item_id
SET DEFAULT gen_random_uuid ();