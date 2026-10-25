
"""Run recommendation engines and add response fields with bounded DB calls."""

from backend.database.supabase_client import supabase


class RecommendationService:

    # Worker -> Jobs
    @staticmethod
    def get_jobs_for_worker(worker_id: str, top_n: int = 15):
        # Defer pandas/sklearn/model imports until an ML route is used.
        from ml.engines.workerForJob_RE import recommend_jobs_for_worker

        results = recommend_jobs_for_worker(worker_id, top_n=top_n)
        final_results = results[:top_n]
        for r in final_results:
            # The engine already loaded the title with its candidate row.
            # Reuse it instead of issuing one database request per result.
            r["job_title"] = r.get("title") or "Unknown"

        return final_results

    # Job -> Workers
    @staticmethod
    def get_workers_for_job(job_id: str, top_n: int = 15):
        from ml.engines.jobForWorkers_RE import recommend_workers_for_job

        results = recommend_workers_for_job(job_id, top_n=top_n)
        final_results = results[:top_n]

        worker_ids = list(dict.fromkeys(
            r["worker_id"] for r in final_results if r.get("worker_id")
        ))
        profiles = {}
        if worker_ids:
            profile_resp = supabase.table("Profiles") \
                .select("id, full_name") \
                .in_("id", worker_ids) \
                .execute()
            profiles = {
                str(profile["id"]): profile.get("full_name") or "Unknown"
                for profile in profile_resp.data
            }

        for r in final_results:
            r["full_name"] = profiles.get(str(r.get("worker_id")), "Unknown")

        return final_results
