import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

supabase_url = os.getenv("SUPABASE_URL")
supabase_anon_key = os.getenv("SUPABASE_ANON_KEY")

if not supabase_url or not supabase_anon_key:
    raise EnvironmentError("Supabase configuration is missing. Ensure SUPABASE_URL and SUPABASE_ANON_KEY are set in your .env file.")

supabase: Client = create_client(supabase_url, supabase_anon_key)
