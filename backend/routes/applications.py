from fastapi import APIRouter, HTTPException
from backend.database.supabase_client import supabase

router = APIRouter()

# 1. Worker apply karta hai (Returns the ID for testing)
@router.post("/apply")
def apply_for_job(data: dict):
    try:
        # .execute() ke baad hum result check karenge
        res = supabase.table("applications").insert({
            "job_id": data.get("job_id"),
            "worker_id": data.get("worker_id"),
            "status": "pending"
        }).execute()
        
        if not res.data:
            raise Exception("Application failed to save in database")

        # Hum pura data return kar rahe hain jisme 'id' bhi hoga
        return {
            "status": "success", 
            "message": "Application submitted successfully!",
            "application": res.data[0]  # Isme se 'id' copy karein Swagger mein
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# 2. Employer status update karta hai (Accept/Reject)
@router.post("/status-update")
def update_application_status(data: dict):
    try:
        # data mein 'application_id' aur 'new_status' (hired/rejected) aayega
        res = supabase.table("applications")\
            .update({"status": data.get("new_status")})\
            .eq("id", data.get("application_id"))\
            .execute()
            
        if not res.data:
            raise Exception("Application ID not found or update failed")

        return {
            "status": "success", 
            "message": f"Application status updated to {data.get('new_status')}",
            "updated_data": res.data[0]
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# 3. Worker ke liye uski saari applications fetch karna
@router.get("/my-applications/{worker_id}")
def get_worker_apps(worker_id: str):
    try:
        # Hum 'Jobs' table se title aur budget bhi join kar rahe hain
        res = supabase.table("applications")\
            .select("*, Jobs(title, budget, status)")\
            .eq("worker_id", worker_id)\
            .execute()
        return res.data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))