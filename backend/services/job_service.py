from backend.database.supabase_client import supabase
from sentence_transformers import SentenceTransformer

embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

class JobService:
    @staticmethod
    def create_job(data: dict):
        try:
            # --- STEP 1: Generate AI Embedding ---
            job_text = f"{data.get('title')}: {data.get('description')}"
            vector = embedding_model.encode(job_text).tolist()

            # --- STEP 2: Insert Job (Stats + Embedding) ---
            job_resp = supabase.table("Jobs").insert({
                "employer_id": data.get("employer_id"),
                "title": data.get("title"),
                "description": data.get("description"),
                "budget": data.get("budget"),
                "location_lat": data.get("location_lat"),
                "location_lng": data.get("location_lng"),
                "job_embedding": vector,  # <--- No longer NULL!
                "status": "open"
            }).execute()

            if not job_resp.data:
                return {"error": "Failed to create job entry"}

            job_id = job_resp.data[0]['id']

            # --- STEP 3: Link Required Skills ---
            skill_ids = data.get("skills", [])
            if skill_ids:
                job_skill_links = [{"job_id": job_id, "skill_id": s_id} for s_id in skill_ids]
                supabase.table("Job_required_skill").insert(job_skill_links).execute()

            return {"status": "success", "job_id": job_id}

        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def get_job_details(job_id: str):
        res = supabase.table("Jobs").select("*, Job_required_skill(skill_id)").eq("id", job_id).execute()
        return res.data[0] if res.data else None