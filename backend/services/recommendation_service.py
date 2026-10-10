"""
backend/services/recommendation_service.py  (FIXED VERSION)
-------------------------------------------------
Bug fixed vs original:
  - The old fallback silently swapped in the FULL unfiltered ML result
    list whenever skill-based filtering returned nothing:

        results = filtered_results if filtered_results else results

    Because the underlying engines now enforce a real skill filter
    (see jobForWorkers_RE.py / workerForJob_RE.py fixes), the outer
    filtering here is largely redundant — but we keep a thin explicit
    layer so the API response always tells the caller HOW a result was
    produced (skill match vs semantic-only fallback), instead of
    silently blending both with no signal to the frontend.
"""

from ml.engines.workerForJob_RE import (
    recommend_jobs_for_worker,
)

from ml.engines.jobForWorkers_RE import (
    recommend_workers_for_job,
)
from backend.database.supabase_client import supabase


class RecommendationService:

    # Worker -> Jobs
    @staticmethod
    def get_jobs_for_worker(worker_id: str, top_n: int = 5):
        try:
            worker_skill_resp = supabase.table("Worker_skills") \
                .select("skill_id") \
                .eq("worker_id", worker_id) \
                .execute()
            worker_skill_ids = [s["skill_id"] for s in worker_skill_resp.data]

            # The engine itself now enforces skill overlap when the job has
            # required skills, so we no longer need a second, looser filter
            # layer here. We just tag the response so the frontend can show
            # "matched on your skills" vs "worker has no listed skills yet".
            results = recommend_jobs_for_worker(worker_id, top_n=top_n)

            if not worker_skill_ids:
                for r in results:
                    r["match_type"] = "no_worker_skills_semantic_only"

            final_results = results[:top_n]

            seen_jobs = set()
            for r in final_results:
                if r["job_id"] not in seen_jobs:
                    job = supabase.table("Jobs") \
                        .select("title") \
                        .eq("id", r["job_id"]) \
                        .execute()
                    r["job_title"] = job.data[0]["title"] if job.data else "Unknown"
                    seen_jobs.add(r["job_id"])

            return final_results

        except Exception as e:
            print("ERROR (jobs_for_worker):", e)
            return []

    # Job -> Workers
    @staticmethod
    def get_workers_for_job(job_id: str, top_n: int = 5):
        try:
            job_skill_resp = supabase.table("Job_required_skill") \
                .select("skill_id") \
                .eq("job_id", job_id) \
                .execute()
            job_skill_ids = [s["skill_id"] for s in job_skill_resp.data]

            results = recommend_workers_for_job(job_id, top_n=top_n)

            if not job_skill_ids:
                for r in results:
                    r["match_type"] = "no_job_skills_semantic_only"

            final_results = results[:top_n]

            seen_workers = set()
            for r in final_results:
                if r["worker_id"] not in seen_workers:
                    profile = supabase.table("Profiles") \
                        .select("full_name") \
                        .eq("id", r["worker_id"]) \
                        .execute()
                    r["full_name"] = profile.data[0]["full_name"] if profile.data else "Unknown"
                    seen_workers.add(r["worker_id"])

            return final_results

        except Exception as e:
            print("ERROR (workers_for_job):", e)
            return []
