from fastapi import FastAPI
from backend.routes import workers, jobs, applications, recommendations

app = FastAPI(title="LabourNearMe API")

# Connect the routes
app.include_router(workers.router, prefix="/workers", tags=["Workers"])
app.include_router(jobs.router, prefix="/jobs", tags=["Jobs"])
app.include_router(applications.router, prefix="/applications", tags=["Applications"])
app.include_router(recommendations.router, prefix="/recommend", tags=["Recommendations"])

@app.get("/")
def home():
    return {"message": "LabourNearMe Backend is running! 🚀"}