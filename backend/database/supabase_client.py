import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")

try:
    if not url or not key:
        raise ValueError("Missing SUPABASE_URL or SUPABASE_KEY in .env file")
    
    supabase: Client = create_client(url, key)
    print("🚀 Supabase Client initialized successfully!")
except Exception as e:
    print(f"❌ Connection failed: {e}")