from fastapi import APIRouter, HTTPException
from backend.services.job_service import JobService

router = APIRouter()

@router.post("/")
def post_job(data: dict):
    result = JobService.create_job(data)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.get("/{job_id}")
def get_job(job_id: str):
    job = JobService.get_job_details(job_id)
    return job