CREATE TYPE imageType AS ENUM ('INPUT', 'OUTPUT', 'POSE', 'MODEL');

ALTER TABLE images
ADD COLUMN type imageType NULL DEFAULT 'INPUT';