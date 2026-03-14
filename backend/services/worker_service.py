from backend.database.supabase_client import supabase
from sentence_transformers import SentenceTransformer

# Initialize the model (matches your ML engine's 384 dimensions)
# Note: On first run, it will download a small (~80MB) model file
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

class WorkerService:
    @staticmethod
    def register_new_worker(data: dict):
        try:
            # --- STEP 1: Generate AI Embedding ---
            # We combine experience and skills for a rich vector
            # You can also add actual skill names here if the frontend sends them
            text_for_embedding = f"Worker with {data.get('experience_years')} years of experience."
            vector = embedding_model.encode(text_for_embedding).tolist()

            # --- STEP 2: Create Profile (Identity) ---
            profile_resp = supabase.table("Profiles").insert({
                "full_name": data.get("full_name"),
                "phone": data.get("phone"),
                "role": "worker"
            }).execute()

            if not profile_resp.data:
                return {"error": "Failed to create profile entry"}

            new_worker_id = profile_resp.data[0]['id']

            # --- STEP 3: Create Worker (Stats + Embedding) ---
            supabase.table("workers").insert({
                "id": new_worker_id,
                "experience_years": data.get("experience_years"),
                "expected_wage": data.get("expected_wage"),
                "location_lat": data.get("location_lat"),
                "location_lng": data.get("location_lng"),
                "worker_embedding": vector,  # <--- No longer NULL!
                "rating": 0,
                "total_jobs_done": 0,
                "availability_status": True
            }).execute()

            # --- STEP 4: Link Skills (Option B) ---
            skill_ids = data.get("skills", [])
            if skill_ids:
                skill_mappings = [{"worker_id": new_worker_id, "skill_id": s_id} for s_id in skill_ids]
                supabase.table("Worker_skills").insert(skill_mappings).execute()

            return {"status": "success", "worker_id": new_worker_id}

        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def get_worker_details(worker_id: str):
        res = supabase.table("workers").select("*, Profiles(*)").eq("id", worker_id).execute()
        return res.data[0] if res.data else None