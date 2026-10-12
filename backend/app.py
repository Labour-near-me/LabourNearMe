import os

from fastapi import FastAPI
from backend.routes import admin
from fastapi.middleware.cors import CORSMiddleware
# Naye feedback route ko import karein
from backend.routes import workers, jobs, applications, recommendations, employers, feedback

app = FastAPI(
    title="LabourNearMe API",
    description="AI-Powered Skill Matching Platform for Daily Wage Workers",
    version="1.0.0"
)

# Set CORS_ALLOWED_ORIGINS to a comma-separated list of deployed frontend
# origins. Keep local development origins available even when the deployment
# environment variable is set, including Ashlesha's frontend on port 8000.
configured_origins = [
    origin.strip()
    for origin in os.getenv("CORS_ALLOWED_ORIGINS", "").split(",")
    if origin.strip()
]
local_dev_origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://localhost:8000",
]
allowed_origins = list(dict.fromkeys(local_dev_origins + configured_origins))

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Saare Routers ko register karna
app.include_router(workers.router, prefix="/workers", tags=["Workers"])
app.include_router(employers.router, prefix="/employers", tags=["Employers"])
app.include_router(jobs.router, prefix="/jobs", tags=["Jobs"])
app.include_router(applications.router, prefix="/applications", tags=["Applications"])
app.include_router(recommendations.router, prefix="/recommend", tags=["Recommendations"])
# Naya Feedback Router
app.include_router(feedback.router, prefix="/feedback", tags=["Feedback & Completion"])
app.include_router(admin.router, prefix="/admin", tags=["Admin Dashboard"])

@app.get("/")
def home():
    return {
        "message": "LabourNearMe Backend is Live! 🚀",
        "status": "Healthy",
        "engine": "AI Matching + ML Ranking Active"
    }
