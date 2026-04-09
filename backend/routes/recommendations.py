from fastapi import APIRouter, HTTPException
from backend.services.recommendation_service import RecommendationService

router = APIRouter()

# 🔹 For Workers → Get Job Recommendations
@router.get("/jobs/{worker_id}")
def get_job_recs(worker_id: str, top_n: int = 5):
    try:
        recs = RecommendationService.get_jobs_for_worker(worker_id, top_n)

        return {
            "worker_id": worker_id,
            "count": len(recs),
            "recommendations": recs
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# 🔹 For Employers → Get Worker Recommendations
@router.get("/workers/{job_id}")
def get_worker_recs(job_id: str, top_n: int = 5):
    try:
        recs = RecommendationService.get_workers_for_job(job_id, top_n)

        return {
            "job_id": job_id,
            "count": len(recs),
            "recommendations": recs
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))