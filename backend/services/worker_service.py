from backend.database.supabase_client import supabase
from sentence_transformers import SentenceTransformer

embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

class WorkerService:
    @staticmethod
    def register_new_worker(data: dict):
        try:
            # --- AUTOMATION: Build AI Context ---
            skills = data.get("skills", [])
            category = data.get("category", "General")
            # Creating a descriptive string so the ML model understands the worker
            text = f"{category} worker skilled in {', '.join(skills)}. Experience: {data.get('experience_years')} years."
            vector = embedding_model.encode(text).tolist()

            # --- Database Insert: Profile ---
            profile = supabase.table("Profiles").insert({
                "full_name": data.get("full_name"),
                "phone": data.get("phone"),
                "role": "worker"
            }).execute()
            
            if not profile.data: return {"error": "Profile creation failed"}
            worker_id = profile.data[0]['id']

            # --- Database Insert: Worker ---
            supabase.table("workers").insert({
                "id": worker_id,
                "experience_years": data.get("experience_years"),
                "expected_wage": data.get("expected_wage"),
                "location_lat": data.get("location_lat"),
                "location_lng": data.get("location_lng"),
                "worker_embedding": vector,
                "availability_status": True
            }).execute()

            # --- AUTOMATION: Auto-Link Skills ---
            # Fetch all skill IDs matching the category or name
            skill_ids = []
            skill_query = supabase.table("Skill_master").select("id").or_(f"category.ilike.{category},skill_name.in.({','.join(skills)})").execute()
            if skill_query.data:
                skill_ids = [s["id"] for s in skill_query.data]
                links = [{"worker_id": worker_id, "skill_id": sid} for sid in skill_ids]
                supabase.table("Worker_skills").insert(links).execute()

            return {"status": "success", "worker_id": worker_id}
        except Exception as e:
            return {"error": str(e)}