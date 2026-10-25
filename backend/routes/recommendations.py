import logging

from fastapi import APIRouter, Depends, HTTPException, Query
from backend.services.recommendation_service import RecommendationService
from backend.auth import require_role
from backend.database.supabase_client import supabase

router = APIRouter()
logger = logging.getLogger(__name__)

# 🔹 For Workers → Get Job Recommendations
@router.get("/jobs/{worker_id}")
def get_job_recs(
    worker_id: str,
    top_n: int = Query(default=5, ge=1, le=20),
    worker: dict = Depends(require_role("worker")),
):
    if str(worker["id"]) != worker_id:
        raise HTTPException(status_code=403, detail="You can request recommendations only for yourself")
    try:
        recs = RecommendationService.get_jobs_for_worker(worker_id, top_n)

        return {
            "worker_id": worker_id,
            "count": len(recs),
            "recommendations": recs
        }

    except Exception as exc:
        logger.error("Job recommendation generation failed (exception_type=%s)", type(exc).__name__)
        raise HTTPException(status_code=500, detail="Job recommendations could not be generated")


# 🔹 For Employers → Get Worker Recommendations
@router.get("/workers/{job_id}")
def get_worker_recs(
    job_id: str,
    top_n: int = Query(default=5, ge=1, le=20),
    employer: dict = Depends(require_role("employer")),
):
    try:
        job = (
            supabase.table("Jobs")
            .select("id, employer_id, status")
            .eq("id", job_id)
            .execute()
        )
        if not job.data:
            raise HTTPException(status_code=404, detail="Job not found")
        if str(job.data[0].get("employer_id")) != str(employer["id"]):
            raise HTTPException(status_code=403, detail="You can request recommendations only for your own jobs")

        raw_recs = RecommendationService.get_workers_for_job(job_id, top_n)
        public_fields = {
            "worker_id",
            "full_name",
            "final_score",
            "similarity",
            "skill_similarity",
            "distance_km",
            "rating",
            "match_type",
        }
        recs = [
            {key: value for key, value in item.items() if key in public_fields}
            for item in raw_recs
        ]

        return {
            "job_id": job_id,
            "count": len(recs),
            "recommendations": recs
        }

    except HTTPException:
        raise
    except Exception as exc:
        logger.error("Worker recommendation generation failed (exception_type=%s)", type(exc).__name__)
        raise HTTPException(status_code=500, detail="Worker recommendations could not be generated")
