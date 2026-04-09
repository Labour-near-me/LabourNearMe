from backend.database.supabase_client import supabase
from sentence_transformers import SentenceTransformer

embedding_model = SentenceTransformer('all-MiniLM-L6-v2')


class JobService:

    @staticmethod
    def create_job(data: dict, employer_id: str):
        try:
            # --- STEP 0: Validate employer ---
            if not employer_id:
                return {"error": "User not authenticated"}

            profile = supabase.table("Profiles") \
                .select("*") \
                .eq("id", employer_id) \
                .eq("role", "employer") \
                .execute()

            if not profile.data:
                return {"error": "Invalid employer"}

            # --- STEP 1: Generate AI Embedding (skills repeated for higher weight) ---
            title = data.get('title', '')
            desc = data.get('description', '')
            skills = " ".join(data.get('required_skills', []))
            job_text = f"{title} {skills} {skills} {desc}"

            vector = embedding_model.encode(job_text).tolist()

            # --- STEP 2: Insert Job ---
            job_resp = supabase.table("Jobs").insert({
                "employer_id": employer_id,
                "title": data.get("title"),
                "description": data.get("description"),
                "budget": data.get("budget"),
                "location_lat": data.get("location_lat"),
                "location_lng": data.get("location_lng"),
                "job_embedding": vector,
                "status": "open"
            }).execute()

            if not job_resp.data:
                return {"error": "Failed to create job entry"}

            job_id = job_resp.data[0]['id']

            # --- STEP 3: Link Required Skills (NAME → ID) ---
            skill_names = data.get("required_skills", [])
            skill_ids = []

            for skill_name in skill_names:
                skill_name = skill_name.strip()

                skill_resp = supabase.table("Skill_master") \
                    .select("*") \
                    .ilike("skill_name", skill_name) \
                    .execute()

                if not skill_resp.data:
                    return {"error": f"Skill '{skill_name}' not found in Skill_master"}

                skill_ids.append(skill_resp.data[0]["id"])

            # --- STEP 4: Insert into Job_required_skill ---
            if skill_ids:
                job_skill_links = [
                    {"job_id": job_id, "skill_id": sid}
                    for sid in skill_ids
                ]
                supabase.table("Job_required_skill").insert(job_skill_links).execute()

            return {"status": "success", "job_id": job_id}

        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def get_job_details(job_id: str):
        res = supabase.table("Jobs") \
            .select("*, Job_required_skill(skill_id)") \
            .eq("id", job_id) \
            .execute()

        return res.data[0] if res.data else None
    
    @staticmethod
    def get_all_jobs():
     res = supabase.table("Jobs") \
        .select("id, employer_id, title, description, budget, status, created_at, location_lat, location_lng")\
        .eq("status", "open") \
        .execute()

     return res.data