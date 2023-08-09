from supabase import create_client, Client
from app.config import config


url: str = config.get("SUPABASE_URL")
key: str = config.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)
