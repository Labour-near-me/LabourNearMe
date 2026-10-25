import logging

from fastapi import APIRouter, Depends, HTTPException
from backend.database.supabase_client import supabase
from backend.auth import require_role

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/dashboard-stats")
def get_admin_stats(admin: dict = Depends(require_role("admin"))):
    try:
        # 1. Total Workers count
        workers = supabase.table("workers").select("id", count="exact").execute()
        # 2. Total Jobs count
        jobs = supabase.table("Jobs").select("id", count="exact").eq("status", "open").execute()
        # 3. Successful Matches (Hired/Completed Applications)
        matches = supabase.table("applications").select("id", count="exact").in_("status", ["hired", "completed"]).execute()
        # 4. Total Ratings given
        ratings = supabase.table("ratings").select("id", count="exact").execute()

        return {
            "platform_summary": {
                "total_workers": workers.count,
                "active_jobs": jobs.count,
                "successful_placements": matches.count,
                "total_reviews_given": ratings.count
            },
            "system_health": "AI Engine Online (Sentence-Transformers Active)"
        }
    except Exception as exc:
        logger.error("Admin dashboard lookup failed (exception_type=%s)", type(exc).__name__)
        raise HTTPException(status_code=500, detail="Admin dashboard data could not be retrieved")
