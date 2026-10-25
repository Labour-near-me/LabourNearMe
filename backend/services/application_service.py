from datetime import datetime
import logging

from backend.database.supabase_client import supabase

logger = logging.getLogger(__name__)

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

    except Exception as exc:
        logger.error("Apply helper failed (exception_type=%s)", type(exc).__name__)
        return {"success": False, "error": "Application could not be submitted"}

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

    except Exception as exc:
        logger.error("Hire helper failed (exception_type=%s)", type(exc).__name__)
        return {"success": False, "error": "Application status could not be updated"}

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

    except Exception as exc:
        logger.error("Rating helper failed (exception_type=%s)", type(exc).__name__)
        return {"success": False, "error": "Job completion and rating could not be saved"}
