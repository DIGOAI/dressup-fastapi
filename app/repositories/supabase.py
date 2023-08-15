from storage3.types import FileOptions
from supabase.client import Client, create_client

from app.config import Config

# Config.load_config()

supabase: Client = create_client(
    Config.SUPABASE_URL,
    Config.SUPABASE_KEY
)
