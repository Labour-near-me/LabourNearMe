from fastapi import APIRouter, HTTPException
from backend.services.application_service import apply_job, hire_worker, rate_worker

router = APIRouter()

@router.post("/apply")
def apply(data: dict):
    result = apply_job(data.get("worker_id"), data.get("job_id"))
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["error"])
    return result["data"]

@router.post("/hire")
def hire(data: dict):
    result = hire_worker(data.get("worker_id"), data.get("job_id"))
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["error"])
    return result["data"]

@router.post("/rating")
def rating(data: dict):
    # Pass the fields from your request body
    result = rate_worker(
        data.get("job_id"),
        data.get("reviewer_id"),
        data.get("reviewee_id"),
        data.get("rating_value"),
        data.get("feedback")
    )
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["error"])
    return result["data"]