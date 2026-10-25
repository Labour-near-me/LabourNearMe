
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
import logging
from backend.database.supabase_client import supabase
from backend.auth import require_role

router = APIRouter()
logger = logging.getLogger(__name__)

class ApplicationCreate(BaseModel):
    job_id: str
    # Temporarily accepted for compatibility; identity is always taken from the token.
    worker_id: str | None = None


class ApplicationStatusUpdate(BaseModel):
    application_id: str
    new_status: str


@router.post("/apply")
def apply_for_job(
    data: ApplicationCreate,
    worker: dict = Depends(require_role("worker")),
):
    job_id = data.job_id
    worker_id = str(worker["id"])

    if data.worker_id and str(data.worker_id) != worker_id:
        raise HTTPException(status_code=403, detail="You can apply only as the signed-in worker")

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
    except Exception as exc:
        if getattr(exc, "code", None) == "23505" or "applications_job_worker_unique" in str(exc):
            raise HTTPException(status_code=409, detail="You have already applied for this job")
        logger.error("Application submission failed (exception_type=%s)", type(exc).__name__)
        raise HTTPException(status_code=500, detail="Application could not be submitted")


@router.post("/status-update")
def update_application_status(
    data: ApplicationStatusUpdate,
    employer: dict = Depends(require_role("employer")),
):
    application_id = data.application_id
    new_status = data.new_status

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
            .select("id, employer_id, status")
            .eq("id", app["job_id"])
            .execute()
        )

        if not job.data:
            raise HTTPException(status_code=404, detail="Job not found")

        if str(job.data[0].get("employer_id")) != str(employer["id"]):
            raise HTTPException(
                status_code=403,
                detail="You are not authorized to manage applications for this job"
            )

        if new_status == "hired":
            if job.data[0].get("status") != "open":
                raise HTTPException(status_code=409, detail="This job is no longer open for hiring")

            # The database function closes the job, hires this application, and
            # rejects the remaining pending applications in one transaction.
            result = supabase.rpc(
                "hire_application_for_job",
                {
                    "p_application_id": application_id,
                    "p_employer_id": str(employer["id"]),
                },
            ).execute()
        else:
            result = (
                supabase.table("applications")
                .update({"status": "rejected"})
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
            "updated_data": result.data[0] if result.data else {
                "id": application_id,
                "status": new_status,
                "job_id": app["job_id"],
            }
        }

    except HTTPException:
        raise
    except Exception as exc:
        logger.error("Application status update failed (exception_type=%s)", type(exc).__name__)
        raise HTTPException(status_code=500, detail="Application status could not be updated")


@router.get("/my-applications/{worker_id}")
def get_worker_apps(worker_id: str, worker: dict = Depends(require_role("worker"))):
    if str(worker["id"]) != worker_id:
        raise HTTPException(status_code=403, detail="You can view only your own applications")
    try:
        result = (
            supabase.table("applications")
            .select("*, Jobs(title, budget, status)")
            .eq("worker_id", worker_id)
            .execute()
        )
        return result.data
    except Exception as exc:
        logger.error("Application history lookup failed (exception_type=%s)", type(exc).__name__)
        raise HTTPException(status_code=500, detail="Application history could not be retrieved")


@router.get("/job/{job_id}")
def get_applications_by_job(job_id: str, employer: dict = Depends(require_role("employer"))):
    try:
        job = (
            supabase.table("Jobs")
            .select("id, employer_id")
            .eq("id", job_id)
            .execute()
        )
        if not job.data:
            raise HTTPException(status_code=404, detail="Job not found")
        if str(job.data[0].get("employer_id")) != str(employer["id"]):
            raise HTTPException(status_code=403, detail="You can view applicants only for your own jobs")

        result = (
            supabase.table("applications")
            .select("*")
            .eq("job_id", job_id)
            .execute()
        )
        return result.data
    except HTTPException:
        raise
    except Exception as exc:
        logger.error("Applicant list lookup failed (exception_type=%s)", type(exc).__name__)
        raise HTTPException(status_code=500, detail="Applicants could not be retrieved")
