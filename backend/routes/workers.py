from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel
from typing import List, Optional
from backend.services.worker_service import WorkerService

router = APIRouter()

# Schema for automation & validation
class WorkerCreate(BaseModel):
    full_name: str
    phone: str
    experience_years: int
    expected_wage: float
    location_lat: float
    location_lng: float
    category: str
    skills: List[str] = []

@router.post("/")
def register_worker(worker_data: WorkerCreate):
    # .model_dump() converts Pydantic to a clean dict
    result = WorkerService.register_new_worker(worker_data.model_dump())
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.get("/{worker_id}")
def get_worker(worker_id: str):
    worker = WorkerService.get_worker_details(worker_id)
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")
    return worker