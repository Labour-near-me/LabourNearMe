# backend/routes/recommendations.py
from fastapi import APIRouter, HTTPException
from backend.services.recommendation_service import RecommendationService

router = APIRouter()

# -----------------------------
# Job-for-Worker
# -----------------------------
@router.get("/jobs/{worker_id}")
async def get_recommended_jobs(worker_id: str, top_n: int = 5):
    try:
        recommendations = RecommendationService.get_jobs_for_worker(worker_id, top_n)
        if not recommendations:
            return {"status": "success", "data": []}
        return {"status": "success", "data": recommendations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# -----------------------------
# Worker-for-Job
# -----------------------------
@router.get("/workers/{job_id}")
async def get_recommended_workers(job_id: str, top_n: int = 5):
    try:
        recommendations = RecommendationService.get_workers_for_job(job_id, top_n)
        if not recommendations:
            return {"status": "success", "data": []}
        return {"status": "success", "data": recommendations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))