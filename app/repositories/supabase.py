from config import Config
from supabase.client import Client, create_client
from storage3.types import FileOptions

supabase: Client = create_client(
    Config.SUPABASE_URL,
    Config.SUPABASE_KEY
)
