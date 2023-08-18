-- ========================= CREATE User Role TYPE =============================
CREATE TYPE userRole AS ENUM('ADMIN', 'USER', 'PUBLIC');

-- ========================= CREATE User Status TYPE =============================
CREATE TYPE userStatus AS ENUM('ACTIVE', 'INACTIVE', 'DELETED');

-- ========================= CREATE Profiles TABLE =============================
CREATE TABLE
    profiles (
        id UUID NOT NULL REFERENCES auth.users ON DELETE CASCADE PRIMARY KEY,
        ruc VARCHAR(13) NOT NULL UNIQUE,
        names VARCHAR(80) NOT NULL,
        lastnames VARCHAR(80) NOT NULL,
        email VARCHAR(120) NOT NULL UNIQUE,
        phone VARCHAR(13) NOT NULL UNIQUE,
        role userRole NOT NULL,
        status userStatus NOT NULL,
        created_at TIMESTAMP WITH TIME ZONE NULL DEFAULT now()
    ) TABLESPACE pg_default;

ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Enable read access for all users" ON profiles AS PERMISSIVE FOR ALL TO public USING (true);

-- ========================= CREATE Handle New User FUNCTION =============================
CREATE OR REPLACE FUNCTION handle_new_user() RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO public.profiles(id, ruc, names, lastnames, email, phone, role, status)
  VALUES (
    new.id, 
    new.raw_user_meta_data->>'ruc', 
    new.raw_user_meta_data->>'names', 
    new.raw_user_meta_data->>'lastnames',
    new.raw_user_meta_data->>'email',
    new.raw_user_meta_data->>'phone',
    (new.raw_user_meta_data->>'role')::public.userRole,
    (new.raw_user_meta_data->>'status')::public.userStatus
    );
  RETURN new;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- ========================= DEFINE On Auth User Created TRIGGER =============================
CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE PROCEDURE handle_new_user();