
from fastapi import APIRouter, HTTPException, Header
from backend.database.supabase_client import supabase

router = APIRouter()

ALLOWED_APPLICATION_STATUSES = {"pending", "hired", "rejected"}


@router.post("/apply")
def apply_for_job(data: dict):
    job_id = data.get("job_id")
    worker_id = data.get("worker_id")

    if not job_id or not worker_id:
        raise HTTPException(
            status_code=400,
            detail="job_id and worker_id are required"
        )

    try:
        # Verify the job exists and is open.
        job = (
            supabase.table("Jobs")
            .select("id, status")
            .eq("id", job_id)
            .execute()
        )

        if not job.data:
            raise HTTPException(status_code=404, detail="Job not found")

        if job.data[0].get("status") != "open":
            raise HTTPException(
                status_code=400,
                detail="Applications are only accepted for open jobs"
            )

        # Prevent duplicate applications by the same worker for this job.
        existing = (
            supabase.table("applications")
            .select("id")
            .eq("job_id", job_id)
            .eq("worker_id", worker_id)
            .execute()
        )

        if existing.data:
            raise HTTPException(
                status_code=409,
                detail="You have already applied for this job"
            )

        result = supabase.table("applications").insert({
            "job_id": job_id,
            "worker_id": worker_id,
            "status": "pending"
        }).execute()

        if not result.data:
            raise HTTPException(
                status_code=500,
                detail="Application could not be saved"
            )

        return {
            "status": "success",
            "message": "Application submitted successfully!",
            "application": result.data[0]
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/status-update")

@router.post("/status-update")
def update_application_status(
    data: dict,
    x_user_id: str = Header(..., description="Employer UUID")
):
    application_id = data.get("application_id")
    new_status = data.get("new_status")

    if not application_id or not new_status:
        raise HTTPException(
            status_code=400,
            detail="application_id and new_status are required"
        )

    if new_status not in {"hired", "rejected"}:
        raise HTTPException(
            status_code=400,
            detail="new_status must be 'hired' or 'rejected'"
        )

    try:
        # Fetch the application and its associated job.
        application = (
            supabase.table("applications")
            .select("id, status, job_id")
            .eq("id", application_id)
            .execute()
        )

        if not application.data:
            raise HTTPException(
                status_code=404,
                detail="Application not found"
            )

        app = application.data[0]

        if app.get("status") != "pending":
            raise HTTPException(
                status_code=409,
                detail="Only pending applications can be updated"
            )

        # Verify that the requesting employer owns this job.
        job = (
            supabase.table("Jobs")
            .select("id, employer_id")
            .eq("id", app["job_id"])
            .execute()
        )

        if not job.data:
            raise HTTPException(status_code=404, detail="Job not found")

        if str(job.data[0].get("employer_id")) != str(x_user_id):
            raise HTTPException(
                status_code=403,
                detail="You are not authorized to manage applications for this job"
            )

        # Update only if the application is still pending.
        result = (
            supabase.table("applications")
            .update({"status": new_status})
            .eq("id", application_id)
            .eq("status", "pending")
            .execute()
        )

        if not result.data:
            raise HTTPException(
                status_code=409,
                detail="Application status changed; refresh and try again"
            )

        return {
            "status": "success",
            "message": f"Application status updated to {new_status}",
            "updated_data": result.data[0]
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/my-applications/{worker_id}")
def get_worker_apps(worker_id: str):
    try:
        result = (
            supabase.table("applications")
            .select("*, Jobs(title, budget, status)")
            .eq("worker_id", worker_id)
            .execute()
        )
        return result.data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/job/{job_id}")
def get_applications_by_job(job_id: str):
    try:
        result = (
            supabase.table("applications")
            .select("*")
            .eq("job_id", job_id)
            .execute()
        )
        return result.data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
