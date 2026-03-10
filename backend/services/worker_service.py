from backend.database.supabase_client import supabase
from ml.engines.jobForWorkers_RE import recommend_jobs_for_worker as ml_recommend_jobs
import uuid


class WorkerService:

    @staticmethod
    def create_worker(worker_data: dict):
        try:
            # Generate shared UUID
            user_id = str(uuid.uuid4())

            # Step 1️⃣ Create profile
            profile_payload = {
                "id": user_id,
                "full_name": worker_data.get("name"),
                "role": "worker"
            }

            supabase.table("Profiles").insert(profile_payload).execute()

            # Step 2️⃣ Create worker
            worker_payload = {
                "id": user_id,
                "experience_years": worker_data.get("experience_years"),
                "expected_wage": worker_data.get("expected_wage"),
                "location_lat": worker_data.get("location_lat"),
                "location_lng": worker_data.get("location_lng"),
                "availability_status": worker_data.get("availability_status", True),
                "rating": 0.0,
                "total_jobs_done": 0
            }

            response = supabase.table("workers").insert(worker_payload).execute()

            return {"success": True, "worker": response.data[0]}

        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def get_worker(worker_id: str):
        response = supabase.table("workers").select("*").eq("id", worker_id).execute()
        return response.data[0] if response.data else None

    @staticmethod
    def get_recommended_jobs(worker_id: str):

        ml_results = ml_recommend_jobs(worker_id)

        job_list = []

        for item in ml_results:

            job_resp = supabase.table("Jobs").select("*").eq("id", item['job_id']).execute()

            if job_resp.data:
                data = job_resp.data[0]
                data["match_score"] = item['score']
                job_list.append(data)

        return job_list