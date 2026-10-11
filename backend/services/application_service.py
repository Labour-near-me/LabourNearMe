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

def hire_worker(worker_id: str, job_id: str, employer_id: str):
    try:
        application = (
            supabase.table("applications")
            .select("id")
            .eq("worker_id", worker_id)
            .eq("job_id", job_id)
            .eq("status", "pending")
            .execute()
        )
        if not application.data:
            return {"success": False, "error": "No pending application found for this worker and job"}

        response = supabase.rpc(
            "hire_application_for_job",
            {
                "p_application_id": application.data[0]["id"],
                "p_employer_id": employer_id,
            },
        ).execute()

        return {"success": True, "data": response.data[0]}

    except Exception as e:
        return {"success": False, "error": str(e)}

def rate_worker(job_id, reviewer_id, reviewee_id, rating_value, feedback):
    try:
        response = supabase.rpc(
            "complete_and_rate_job",
            {
                "p_job_id": job_id,
                "p_employer_id": reviewer_id,
                "p_worker_id": reviewee_id,
                "p_rating_value": rating_value,
                "p_feedback": feedback,
            },
        ).execute()

        return {"success": True, "data": response.data}

    except Exception as e:
        return {"success": False, "error": str(e)}
