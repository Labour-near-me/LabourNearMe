import os
import base64
import json
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_KEY")


def _jwt_role(jwt: str) -> str | None:
    """Read the role claim so the server cannot silently use a public anon key."""
    try:
        payload = jwt.split(".")[1]
        payload += "=" * (-len(payload) % 4)
        return json.loads(base64.urlsafe_b64decode(payload)).get("role")
    except (IndexError, ValueError, json.JSONDecodeError):
        return None

supabase: Client = None  # 👈 define globally

if not url or not key:
    raise ValueError("Missing SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY in the backend environment")

if _jwt_role(key) != "service_role":
    raise ValueError(
        "Backend database access requires the Supabase service_role key. "
        "Set SUPABASE_SERVICE_ROLE_KEY server-side; never use an anon key or expose this key to the frontend."
    )

try:
    supabase = create_client(url, key)
    print("🚀 Supabase Client initialized successfully!")
except Exception as e:
    print(f"❌ Connection failed: {e}")
