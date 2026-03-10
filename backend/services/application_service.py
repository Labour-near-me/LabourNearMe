from datetime import datetime
from backend.database.supabase_client import supabase

def apply_job(worker_id: str, job_id: str):
    try:
        existing = (
            supabase.table("applications")
            .select("*")
            .eq("worker_id", worker_id)
            .eq("job_id", job_id)
            .execute()
        )

        if existing.data:
            return {"success": False, "error": "Worker already applied to this job"}

        data = {
            "worker_id": worker_id,
            "job_id": job_id,
            "status": "pending",
            "applied_at": datetime.utcnow().isoformat()
        }

        response = supabase.table("applications").insert(data).execute()
        return {"success": True, "data": response.data[0]}

    except Exception as e:
        return {"success": False, "error": str(e)}

def hire_worker(worker_id: str, job_id: str):
    try:
        response = (
            supabase.table("applications")
            .update({"status": "accepted"})
            .eq("worker_id", worker_id)
            .eq("job_id", job_id)
            .execute()
        )
        # Update Jobs table status (Capital 'J' as per your schema)
        supabase.table("Jobs").update({"status": "assigned"}).eq("id", job_id).execute()

        return {"success": True, "data": {"worker_id": worker_id, "job_id": job_id, "status": "assigned"}}

    except Exception as e:
        return {"success": False, "error": str(e)}

def rate_worker(job_id, reviewer_id, reviewee_id, rating_value, feedback):
    try:
        data = {
            "job_id": job_id,
            "reviewer_id": reviewer_id,
            "reviewee_id": reviewee_id,
            "rating_value": rating_value,
            "feedbck": feedback, # Matches your schema's typo 'feedbck'
            "created_at": datetime.utcnow().isoformat()
        }

        response = supabase.table("ratings").insert(data).execute()

        # Optional worker rating update
        try:
            supabase.rpc("update_worker_rating", {"worker_id_input": reviewee_id}).execute()
        except:
            pass

        return {"success": True, "data": response.data[0]}

    except Exception as e:
        return {"success": False, "error": str(e)}