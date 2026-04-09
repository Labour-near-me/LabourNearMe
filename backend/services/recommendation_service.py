from ml.engines.jobForWorkers_RE import recommend_jobs_for_worker, refresh_data as refresh_jobs
from ml.engines.workerForJob_RE import recommend_workers_for_job, refresh_data as refresh_workers
from backend.database.supabase_client import supabase


class RecommendationService:

    # 🔹 Worker → Jobs
    @staticmethod
    def get_jobs_for_worker(worker_id: str, top_n: int = 5):
        try:
            refresh_jobs()

            # STEP 1: Get worker skill IDs
            worker_skill_resp = supabase.table("Worker_skills") \
                .select("skill_id") \
                .eq("worker_id", worker_id) \
                .execute()
            worker_skill_ids = [s["skill_id"] for s in worker_skill_resp.data]

            # STEP 2: ML fallback if no skills
            if not worker_skill_ids:
                results = recommend_jobs_for_worker(worker_id, top_n=top_n)
            else:
                # STEP 3: Matching jobs
                job_skill_resp = supabase.table("Job_required_skill") \
                    .select("job_id") \
                    .in_("skill_id", worker_skill_ids) \
                    .execute()
                matched_job_ids = list(set([j["job_id"] for j in job_skill_resp.data]))

                # STEP 4: ML recommendations
                results = recommend_jobs_for_worker(worker_id, top_n=50)
                filtered_results = [r for r in results if r["job_id"] in matched_job_ids]

                # FALLBACK
                results = filtered_results if filtered_results else results

            # STEP 5: Limit top_n and add job_title
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


    # 🔹 Job → Workers
    @staticmethod
    def get_workers_for_job(job_id: str, top_n: int = 5):
        try:
            refresh_workers()

            # STEP 1: Get job skill IDs
            job_skill_resp = supabase.table("Job_required_skill") \
                .select("skill_id") \
                .eq("job_id", job_id) \
                .execute()
            job_skill_ids = [s["skill_id"] for s in job_skill_resp.data]

            # STEP 2: ML fallback if no skills
            if not job_skill_ids:
                results = recommend_workers_for_job(job_id, top_n=top_n)
            else:
                # STEP 3: Matching workers
                worker_skill_resp = supabase.table("Worker_skills") \
                    .select("worker_id") \
                    .in_("skill_id", job_skill_ids) \
                    .execute()
                matched_worker_ids = list(set([w["worker_id"] for w in worker_skill_resp.data]))

                # STEP 4: ML recommendations
                results = recommend_workers_for_job(job_id, top_n=50)
                filtered_results = [r for r in results if r["worker_id"] in matched_worker_ids]

                # FALLBACK
                results = filtered_results if filtered_results else results

            # STEP 5: Limit top_n and add full_name
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