# backend/routes/jobs.py
from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
from typing import List, Optional
from backend.services.job_service import JobService

router = APIRouter()

# Schema for validation and automated documentation
class JobCreateSchema(BaseModel):
    title: str
    description: str
    location_lat: float
    location_lng: float
    required_skills: List[str]
    budget: Optional[float] = 0

@router.post("/")
def post_job(
    data: JobCreateSchema, 
    x_user_id: str = Header(..., description="Paste your Employer UUID here")
):
    """
    Post a new job. 
    Requires 'x-user-id' in the request header to identify the Employer.
    """
    if not x_user_id:
        raise HTTPException(status_code=401, detail="Header 'x-user-id' missing")
        
    # .model_dump() handles the Pydantic to Dict conversion automatically
    result = JobService.create_job(data.model_dump(), x_user_id)
    
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