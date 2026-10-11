# backend/routes/jobs.py
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from backend.services.job_service import JobService
from backend.auth import require_role

router = APIRouter()

# Schema for validation and automated documentation
class JobCreateSchema(BaseModel):
    title: str
    description: str
    location_text: Optional[str] = None
    location_lat: float
    location_lng: float
    required_skills: List[str]
    budget: Optional[float] = 0

@router.post("/")
def post_job(
    data: JobCreateSchema,
    employer: dict = Depends(require_role("employer")),
):
    result = JobService.create_job(data.model_dump(), employer["id"])
    
    if "error" in result:
        # If employer_id is invalid or skill not found, return 400
        raise HTTPException(status_code=400, detail=result["error"])
        
    return result

@router.get("/{job_id}")
def get_job(job_id: str):
    """
    Fetch specific job details by its ID.
    """
    job = JobService.get_job_details(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@router.get("/")
def get_all_jobs():
    jobs = JobService.get_all_jobs()
    return jobs
