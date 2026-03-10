# backend/services/recommendation_service.py
from ml.engines.jobForWorkers_RE import recommend_jobs_for_worker
from ml.engines.workerForJob_RE import recommend_workers_for_job
from backend.database.supabase_client import supabase

class RecommendationService:
    @staticmethod
    def get_jobs_for_worker(worker_id: str, top_n: int = 5):
        """
        Bridge to ML engine: recommend top jobs for a worker
        """
        results = recommend_jobs_for_worker(worker_id, top_n=top_n)
        return results

    @staticmethod
    def get_workers_for_job(job_id: str, top_n: int = 5):
        """
        Bridge to ML engine: recommend top workers for a job
        Adds worker full_name for frontend display
        """
        results = recommend_workers_for_job(job_id, top_n=top_n)
        # Fetch full_name for each worker from profiles table
        for r in results:
            profile = supabase.table("Profiles").select("full_name").eq("id", r["worker_id"]).single().execute()
            if profile.data:
                r["full_name"] = profile.data.get("full_name")
            else:
                r["full_name"] = None
        return results