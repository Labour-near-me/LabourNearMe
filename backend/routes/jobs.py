from fastapi import APIRouter, HTTPException
from backend.services.job_service import JobService

router = APIRouter()

@router.post("/")
def post_job(job: dict):
    result = JobService.create_job(job)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["error"])
    return result["job"]

@router.get("/{job_id}")
def job_details(job_id: str):
    job = JobService.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job