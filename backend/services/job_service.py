from backend.database.supabase_client import supabase
from backend.services.embedding_service import encode_text
from uuid import UUID


class JobService:

    @staticmethod
    def normalize_skill(skill: str):
        return skill.strip().lower()

    @staticmethod
    def get_or_create_skill_id(skill_name: str):
        raw_skill = str(skill_name).strip()

        # The frontend may submit a selected Skill_master UUID. Reuse it
        # directly instead of creating a skill whose name is the UUID text.
        try:
            skill_uuid = str(UUID(raw_skill))
        except ValueError:
            skill_uuid = None

        if skill_uuid:
            existing_by_id = supabase.table("Skill_master") \
                .select("id") \
                .eq("id", skill_uuid) \
                .execute()
            if existing_by_id.data:
                return existing_by_id.data[0]["id"]
            raise ValueError("Unknown skill ID")

        skill_name = JobService.normalize_skill(raw_skill)

        existing = supabase.table("Skill_master") \
            .select("id") \
            .ilike("skill_name", skill_name) \
            .execute()

        if existing.data:
            return existing.data[0]["id"]

        new_skill = supabase.table("Skill_master") \
            .insert({"skill_name": skill_name}) \
            .execute()

        return new_skill.data[0]["id"]

    @staticmethod
    def create_job(data: dict, employer_id: str):
        try:
            if not employer_id:
                return {"error": "User not authenticated"}

            profile = supabase.table("Profiles") \
                .select("*") \
                .eq("id", employer_id) \
                .eq("role", "employer") \
                .execute()

            if not profile.data:
                return {"error": "Invalid employer"}

            # --- Embedding ---
            title = data.get('title', '')
            desc = data.get('description', '')
            skill_list = data.get('required_skills', [])

            skill_text = " ".join(skill_list)
            job_text = f"{title} {skill_text} {skill_text} {desc}"

            vector = encode_text(job_text)

            # --- Insert Job ---
            job_resp = supabase.table("Jobs").insert({
                "employer_id": employer_id,
                "title": title,
                "description": desc,
                "budget": data.get("budget"),
                "location_lat": data.get("location_lat"),
                "location_lng": data.get("location_lng"),
                "job_embedding": vector,
                "status": "open"
            }).execute()

            if not job_resp.data:
                return {"error": "Failed to create job entry"}

            job_id = job_resp.data[0]['id']

            # --- FIXED SKILL LINKING ---
            job_skill_links = []

            for skill in skill_list:
                skill_id = JobService.get_or_create_skill_id(skill)

                job_skill_links.append({
                    "job_id": job_id,
                    "skill_id": skill_id
                })

            if job_skill_links:
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
            .select("id, employer_id, title, description, budget, status, created_at, location_lat, location_lng") \
            .eq("status", "open") \
            .execute()

        return res.data
