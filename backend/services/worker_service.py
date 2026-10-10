from backend.database.supabase_client import supabase
from backend.services.embedding_service import encode_text


class WorkerService:

    @staticmethod
    def normalize_skill(skill: str):
        return skill.strip().lower()

    @staticmethod
    def get_or_create_skill_id(skill_name: str):
        skill_name = WorkerService.normalize_skill(skill_name)

        # Check if exists
        existing = supabase.table("Skill_master") \
            .select("id") \
            .ilike("skill_name", skill_name) \
            .execute()

        if existing.data:
            return existing.data[0]["id"]

        # Create new skill
        new_skill = supabase.table("Skill_master") \
            .insert({"skill_name": skill_name}) \
            .execute()

        return new_skill.data[0]["id"]

    @staticmethod
    def register_new_worker(data: dict):
        try:
            category = data.get("category", "General")
            skills = data.get("skills", [])
            exp = data.get('experience_years', 0)

            # If no skills → fetch by category
            if not skills:
                skill_fetch = supabase.table("Skill_master") \
                    .select("skill_name") \
                    .ilike("category", category) \
                    .execute()

                if skill_fetch.data:
                    skills = [s["skill_name"] for s in skill_fetch.data]

            # --- Embedding ---
            skill_text = ", ".join(skills) if skills else "general labor"
            text = f"{category} {skill_text} {skill_text} Experience {exp} years {category} work"
            vector = encode_text(text)

            # --- Profile ---
            profile_resp = supabase.table("Profiles").insert({
                "full_name": data.get("full_name"),
                "phone": data.get("phone"),
                "role": "worker"
            }).execute()

            if not profile_resp.data:
                return {"error": "Profile creation failed"}

            worker_id = profile_resp.data[0]['id']

            # --- Worker table ---
            supabase.table("workers").insert({
                "id": worker_id,
                "experience_years": exp,
                "expected_wage": data.get("expected_wage"),
                "location_lat": data.get("location_lat"),
                "location_lng": data.get("location_lng"),
                "worker_embedding": vector,
                "availability_status": True
            }).execute()

            # --- FIXED SKILL LINKING ---
            skill_links = []

            for skill in skills:
                skill_id = WorkerService.get_or_create_skill_id(skill)

                skill_links.append({
                    "worker_id": worker_id,
                    "skill_id": skill_id
                })

            if skill_links:
                supabase.table("Worker_skills").insert(skill_links).execute()

            return {"status": "success", "worker_id": worker_id}

        except Exception as e:
            print(f"Error: {e}")
            return {"error": str(e)}

    @staticmethod
    def get_worker_details(worker_id: str):
        try:
            result = supabase.table("Profiles") \
                .select("*, workers(*)") \
                .eq("id", worker_id) \
                .single() \
                .execute()
            return result.data
        except Exception:
            return None
