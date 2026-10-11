
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, StrictInt
from backend.database.supabase_client import supabase
from backend.auth import require_role

router = APIRouter()


class CompleteAndRateRequest(BaseModel):
    job_id: str
    reviewee_id: str
    reviewer_id: str | None = None
    rating_value: StrictInt
    feedback: str = ""


@router.post("/complete-and-rate")
def complete_job(
    data: CompleteAndRateRequest,
    employer: dict = Depends(require_role("employer")),
):
    try:
        job_id = data.job_id
        worker_id = data.reviewee_id
        employer_id = str(employer["id"])
        rating_val = data.rating_value
        feedback_text = data.feedback

        if data.reviewer_id and str(data.reviewer_id) != employer_id:
            raise HTTPException(status_code=403, detail="Reviewer must be the signed-in employer")

        # Validate required fields
        if not all([job_id, worker_id, employer_id, rating_val is not None]):
            raise HTTPException(
                status_code=400,
                detail="job_id, reviewee_id, and rating_value are required"
            )

        # Validate rating range
        if isinstance(rating_val, bool) or not isinstance(rating_val, (int, float)):
            raise HTTPException(
                status_code=400,
                detail="rating_value must be a number between 1 and 5"
            )

        if not 1 <= rating_val <= 5:
            raise HTTPException(
                status_code=400,
                detail="rating_value must be between 1 and 5"
            )

        # Verify the job exists and retrieve its owner.
        job_res = (
            supabase.table("Jobs")
            .select("id, status, employer_id")
            .eq("id", job_id)
            .execute()
        )

        if not job_res.data:
            raise HTTPException(status_code=404, detail="Job not found")

        if str(job_res.data[0].get("employer_id")) != str(employer_id):
            raise HTTPException(
                status_code=403,
                detail="Only the employer who owns this job can submit a rating"
            )

        if job_res.data[0].get("status") != "closed":
            raise HTTPException(status_code=409, detail="Only a closed job can be completed and rated")

        # Verify the worker exists
        worker_res = (
            supabase.table("workers")
            .select("id")
            .eq("id", worker_id)
            .execute()
        )

        if not worker_res.data:
            raise HTTPException(status_code=404, detail="Worker not found")

        hired_application = (
            supabase.table("applications")
            .select("id")
            .eq("job_id", job_id)
            .eq("worker_id", worker_id)
            .eq("status", "hired")
            .execute()
        )
        if not hired_application.data:
            raise HTTPException(status_code=409, detail="Only a worker hired for this job can be rated")

        existing_rating = (
            supabase.table("ratings")
            .select("id")
            .eq("job_id", job_id)
            .eq("reviewer_id", employer_id)
            .eq("reviewee_id", worker_id)
            .execute()
        )
        if existing_rating.data:
            raise HTTPException(status_code=409, detail="This worker has already been rated for this job")

        # Keep the rating, average, and job completion update in one database transaction.
        rating_res = supabase.rpc(
            "complete_and_rate_job",
            {
                "p_job_id": job_id,
                "p_employer_id": employer_id,
                "p_worker_id": worker_id,
                "p_rating_value": rating_val,
                "p_feedback": feedback_text,
            },
        ).execute()

        if not rating_res.data:
            raise HTTPException(status_code=500, detail="Rating could not be saved")

        return {
            "status": "success",
            "message": "Worker rated successfully!",
            "rating": rating_res.data
        }

    except HTTPException:
        raise
    except Exception as e:
        if getattr(e, "code", None) == "23505" or "ratings_job_reviewer_worker_unique" in str(e):
            raise HTTPException(status_code=409, detail="This worker has already been rated for this job")
        raise HTTPException(status_code=400, detail=str(e))
