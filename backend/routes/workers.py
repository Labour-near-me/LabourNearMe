from fastapi import APIRouter, HTTPException
from backend.services.worker_service import WorkerService

router = APIRouter()

@router.post("/")
def register_worker(worker: dict):
    result = WorkerService.create_worker(worker)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["error"])
    return result["worker"]

@router.get("/{worker_id}")
def worker_profile(worker_id: str):
    worker = WorkerService.get_worker(worker_id)
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")
    return worker

@router.get("/{worker_id}/recommendations")
def worker_recommendations(worker_id: str):
    jobs = WorkerService.get_recommended_jobs(worker_id)
    return {"worker_id": worker_id, "recommended_jobs": jobs}