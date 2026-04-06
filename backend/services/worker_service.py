from backend.database.supabase_client import supabase
from sentence_transformers import SentenceTransformer

embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

class WorkerService:
    
    @staticmethod
    def register_new_worker(data: dict):
        try:
            category = data.get("category", "General")
            skills = data.get("skills", [])
            exp = data.get('experience_years', 0)

            # AUTOMATION: If no skills provided, fetch all skills from that category
            if not skills or len(skills) == 0:
                skill_fetch = supabase.table("Skill_master") \
                    .select("skill_name") \
                    .ilike("category", category) \
                    .execute()
                if skill_fetch.data:
                    skills = [s["skill_name"] for s in skill_fetch.data]

            # 1. Build AI Embedding (skills repeated for higher weight)
            skill_text = ", ".join(skills) if skills else "general labor"
            text = f"{category} {skill_text} {skill_text} Experience {exp} years {category} work"

            vector = embedding_model.encode(text).tolist()

            # 2. Insert Profile
            profile_resp = supabase.table("Profiles").insert({
                "full_name": data.get("full_name"),
                "phone": data.get("phone"),
                "role": "worker"
            }).execute()
            
            if not profile_resp.data:
                return {"error": "Profile creation failed"}
            
            worker_id = profile_resp.data[0]['id']

            # 3. Insert Worker Details
            supabase.table("workers").insert({
                "id": worker_id,
                "experience_years": exp,
                "expected_wage": data.get("expected_wage"),
                "location_lat": data.get("location_lat"),
                "location_lng": data.get("location_lng"),
                "worker_embedding": vector,
                "availability_status": True
            }).execute()

            # 4. Auto-Link Skills in Database
            if skills:
                formatted_skills = ",".join([f'"{s}"' for s in skills])
                skill_query = supabase.table("Skill_master") \
                    .select("id") \
                    .or_(f"category.ilike.{category},skill_name.in.({formatted_skills})") \
                    .execute()

                if skill_query.data:
                    links = [{"worker_id": worker_id, "skill_id": s["id"]} for s in skill_query.data]
                    supabase.table("Worker_skills").insert(links).execute()

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
        except Exception as e:
            return None