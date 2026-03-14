from fastapi import APIRouter, HTTPException
from backend.database.supabase_client import supabase # Ye line missing hai
from backend.services.worker_service import WorkerService

router = APIRouter()

@router.post("/")
def register_worker(data: dict):
    result = WorkerService.register_new_worker(data)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.get("/{worker_id}")
def get_worker(worker_id: str):
    worker = WorkerService.get_worker_details(worker_id)
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")
    return worker

@router.patch("/{worker_id}/update-profile")
def update_worker_profile(worker_id: str, data: dict):
    try:
        # data mein availability_status, expected_wage ya experience_years ho sakta hai
        res = supabase.table("workers").update(data).eq("id", worker_id).execute()
        
        if not res.data:
            raise Exception("Worker not found")
            
        return {
            "status": "success", 
            "message": "Profile updated successfully", 
            "updated_fields": data
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))