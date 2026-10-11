
from fastapi import APIRouter, HTTPException
from backend.database.supabase_client import supabase

router = APIRouter()


@router.post("/complete-and-rate")
def complete_job(data: dict):
    try:
        job_id = data.get("job_id")
        worker_id = data.get("reviewee_id")
        employer_id = data.get("reviewer_id")
        rating_val = data.get("rating_value")
        feedback_text = data.get("feedback", "")

        # Validate required fields
        if not all([job_id, worker_id, employer_id, rating_val is not None]):
            raise HTTPException(
                status_code=400,
                detail="job_id, reviewee_id, reviewer_id and rating_value are required"
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

        # Verify the worker exists
        worker_res = (
            supabase.table("workers")
            .select("id")
            .eq("id", worker_id)
            .execute()
        )

        if not worker_res.data:
            raise HTTPException(status_code=404, detail="Worker not found")

        # Save the rating using the existing database column name
        rating_res = supabase.table("ratings").insert({
            "job_id": job_id,
            "reviewer_id": employer_id,
            "reviewee_id": worker_id,
            "rating_value": rating_val,
            "feedbck": feedback_text
        }).execute()

        if not rating_res.data:
            raise HTTPException(
                status_code=500,
                detail="Rating could not be saved"
            )

        # Recalculate the worker's average rating
        ratings_res = (
            supabase.table("ratings")
            .select("rating_value")
            .eq("reviewee_id", worker_id)
            .execute()
        )

        if ratings_res.data:
            values = [r["rating_value"] for r in ratings_res.data]
            average = sum(values) / len(values)

            supabase.table("workers").update({
                "rating": round(average, 2)
            }).eq("id", worker_id).execute()

        # Do not mark the entire job completed here.
        # A job may involve multiple workers, so completion must
        # be handled by the appropriate job-completion workflow.

        return {
            "status": "success",
            "message": "Worker rated successfully!",
            "rating": rating_res.data[0]
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
