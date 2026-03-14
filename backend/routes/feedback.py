from fastapi import APIRouter, HTTPException
from backend.database.supabase_client import supabase

router = APIRouter()

@router.post("/complete-and-rate")
def complete_job(data: dict):
    try:
        job_id = data.get("job_id")
        worker_id = data.get("reviewee_id") # Table ke hisab se reviewee_id
        employer_id = data.get("reviewer_id")
        rating_val = data.get("rating_value")
        feedback_text = data.get("feedback", "")

        # Step 1: Insert into ratings table
        # Note: Typo 'feedbck' as per your schema
        supabase.table("ratings").insert({
            "job_id": job_id,
            "reviewer_id": employer_id,
            "reviewee_id": worker_id,
            "rating_value": rating_val,
            "feedbck": feedback_text 
        }).execute()

        # Step 2: Mark Job as completed
        supabase.table("Jobs").update({"status": "completed"}).eq("id", job_id).execute()

        # Step 3: Recalculate Worker's Average Rating
        ratings_res = supabase.table("ratings").select("rating_value").eq("reviewee_id", worker_id).execute()
        
        if ratings_res.data:
            all_vals = [r['rating_value'] for r in ratings_res.data]
            new_avg = sum(all_vals) / len(all_vals)
            
            # Update worker table with new rating and increment total jobs
            supabase.table("workers").update({
                "rating": round(new_avg, 2),
                "total_jobs_done": len(all_vals)
            }).eq("id", worker_id).execute()

        return {"status": "success", "message": "Job completed and worker rated!"}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))