# backend/services/recommendation_service.py
from ml.engines.jobForWorkers_RE import recommend_jobs_for_worker, refresh_data as refresh_jobs
from ml.engines.workerForJob_RE import recommend_workers_for_job, refresh_data as refresh_workers
from backend.database.supabase_client import supabase

class RecommendationService:
    @staticmethod
    def get_jobs_for_worker(worker_id: str, top_n: int = 5):
        # Trigger a refresh so the ML engine sees the new worker immediately
        refresh_jobs()
        results = recommend_jobs_for_worker(worker_id, top_n=top_n)
        return results

    @staticmethod
    def get_workers_for_job(job_id: str, top_n: int = 5):
        # Trigger refresh for job-to-worker matching
        refresh_workers()
        results = recommend_workers_for_job(job_id, top_n=top_n)
        
        # Add full names for the Frontend
        for r in results:
            profile = supabase.table("Profiles").select("full_name").eq("id", r["worker_id"]).execute()
            r["full_name"] = profile.data[0]["full_name"] if profile.data else "Unknown"
        return results