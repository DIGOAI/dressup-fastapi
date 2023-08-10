import os
from dotenv import load_dotenv


class Config:
    SUPABASE_URL: str
    SUPABASE_KEY: str
    SUPABASE_BUCKET: str
    X_API_KEY: str
    JWT_SECRET: str
    JWT_ALGORITHM: str

    @classmethod
    def load_config(cls):
        load_dotenv()

        cls.SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
        cls.SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "")
        cls.SUPABASE_BUCKET: str = os.getenv("SUPABASE_BUCKET", "")
        cls.X_API_KEY: str = os.getenv("X_API_KEY", "")
        cls.JWT_SECRET = os.getenv("JWT_SECRET", "")
        cls.JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
