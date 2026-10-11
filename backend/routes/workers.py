from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from backend.services.worker_service import WorkerService
from backend.auth import get_authenticated_user, get_current_profile
from backend.database.supabase_client import supabase

router = APIRouter()

class WorkerCreate(BaseModel):
    full_name: str
    phone: str
    experience_years: int
    expected_wage: float
    location_lat: float
    location_lng: float
    category: str
    # We make skills Optional with a default empty list
    skills: Optional[List[str]] = [] 

@router.post("/")
def register_worker(
    worker_data: WorkerCreate,
    user=Depends(get_authenticated_user),
):
    existing = (
        supabase.table("Profiles")
        .select("id, role")
        .eq("auth_user_id", str(user.id))
        .execute()
    )
    if existing.data:
        raise HTTPException(status_code=409, detail="A profile already exists for this account")

    result = WorkerService.register_new_worker(
        worker_data.model_dump(),
        auth_user_id=str(user.id),
    )
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.get("/{worker_id}")
def get_worker(worker_id: str, profile: dict = Depends(get_current_profile)):
    can_view_contact = profile.get("role") == "worker" and str(profile["id"]) == worker_id

    if profile.get("role") == "employer":
        owned_jobs = (
            supabase.table("Jobs")
            .select("id")
            .eq("employer_id", profile["id"])
            .execute()
        )
        owned_job_ids = [job["id"] for job in (owned_jobs.data or [])]
        if owned_job_ids:
            application = (
                supabase.table("applications")
                .select("id")
                .eq("worker_id", worker_id)
                .in_("job_id", owned_job_ids)
                .limit(1)
                .execute()
            )
            can_view_contact = bool(application.data)

    if not can_view_contact:
        raise HTTPException(status_code=403, detail="You are not allowed to view this worker profile")

    worker = WorkerService.get_worker_details(worker_id)
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")
    return worker
