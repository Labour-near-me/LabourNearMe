from fastapi import APIRouter
from ml.engines.jobForWorkers_RE import recommend_jobs_for_worker
from ml.engines.workerForJob_RE import recommend_workers_for_job

router = APIRouter()

# For Workers: "Which jobs are best for me?"
from fastapi import APIRouter, HTTPException
from ml.engines.jobForWorkers_RE import recommend_jobs_for_worker, refresh_data

router = APIRouter()

@router.get("/jobs/{worker_id}")
def get_job_recs(worker_id: str):
    try:
        # Step 1: Force Refresh taaki naye jobs memory mein aa jayein
        refresh_data()
        
        # Step 2: Get Recommendations
        recs = recommend_jobs_for_worker(worker_id)
        
        return {
            "worker_id": worker_id, 
            "count": len(recs),
            "recommendations": recs
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
# For Employers: "Which workers are best for my job?"
@router.get("/workers/{job_id}")
def get_worker_recs(job_id: str):
    return {"job_id": job_id, "recommendations": recommend_workers_for_job(job_id)}