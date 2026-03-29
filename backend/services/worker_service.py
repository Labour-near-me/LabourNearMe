from backend.database.supabase_client import supabase
from sentence_transformers import SentenceTransformer

# Initialize the model
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')


class WorkerService:

    @staticmethod
    def register_new_worker(data: dict):
        try:
            # --- STEP 1: Generate AI Embedding ---
            text_for_embedding = f"Worker with {data.get('experience_years')} years of experience."
            vector = embedding_model.encode(text_for_embedding).tolist()

            # --- STEP 2: Create Profile ---
            profile_resp = supabase.table("Profiles").insert({
                "full_name": data.get("full_name"),
                "phone": data.get("phone"),
                "role": "worker"
            }).execute()

            if not profile_resp.data:
                return {"error": "Failed to create profile entry"}

            new_worker_id = profile_resp.data[0]['id']

            # --- STEP 3: Create Worker ---
            supabase.table("workers").insert({
                "id": new_worker_id,
                "experience_years": data.get("experience_years"),
                "expected_wage": data.get("expected_wage"),
                "location_lat": data.get("location_lat"),
                "location_lng": data.get("location_lng"),
                "worker_embedding": vector,
                "rating": 0,
                "total_jobs_done": 0,
                "availability_status": True
            }).execute()

            # --- STEP 4: Link Skills (STRICT + USER-FRIENDLY) ---
            skill_names = data.get("skills", [])
            skill_ids = []

            for skill_name in skill_names:
                original_name = skill_name
                skill_name = skill_name.strip().lower()

                # 🔥 FIXED TABLE NAME HERE
                existing = supabase.table("Skill_master").select("*").eq("skill_name", skill_name).execute()

                if not existing.data:
                    return {
                        "error": f"Skill '{original_name}' not found. Please select from available skills."
                    }

                skill_id = existing.data[0]["id"]
                skill_ids.append(skill_id)

            if skill_ids:
                skill_mappings = [
                    {"worker_id": new_worker_id, "skill_id": sid}
                    for sid in skill_ids
                ]
                supabase.table("Worker_skills").insert(skill_mappings).execute()

            return {"status": "success", "worker_id": new_worker_id}

        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def get_worker_details(worker_id: str):
        res = supabase.table("workers").select("*, Profiles(*)").eq("id", worker_id).execute()
        return res.data[0] if res.data else None