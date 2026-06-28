from supabase import create_client, Client
from config import SUPABASE_URL, SUPABASE_KEY

def get_supabase_client() -> Client:
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise ValueError("Supabase URL and Key must be provided in environment variables.")
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase_client = get_supabase_client() if SUPABASE_URL and SUPABASE_KEY else None
