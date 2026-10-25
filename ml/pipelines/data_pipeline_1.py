import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

# =========================
# 1️⃣ LOAD ENV VARIABLES
# =========================

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


def get_db_connection():
    if not DATABASE_URL:
        raise RuntimeError(
            "DATABASE_URL is missing. Check your .env configuration."
        )

    return create_engine(DATABASE_URL)

# =========================
# 2️⃣ EXTRACT TABLES
# =========================

def load_workers(engine):
    return pd.read_sql("SELECT * FROM workers;", engine)

def load_jobs(engine):
    return pd.read_sql('SELECT * FROM "Jobs";', engine)

def load_applications(engine):
    return pd.read_sql("SELECT * FROM applications;", engine)

def load_ratings(engine):
    return pd.read_sql("SELECT * FROM ratings;", engine)

def load_worker_skills(engine):
    return pd.read_sql('SELECT * FROM "Worker_skills";', engine)

def load_job_skills(engine):
    return pd.read_sql('SELECT * FROM "Job_required_skill";', engine)

def load_skill_master(engine):
    return pd.read_sql('SELECT * FROM "Skill_master";', engine)


# =========================
# 3️⃣ MAIN PIPELINE
# =========================

def build_dataframes(save_csv=False):

    engine = get_db_connection()

    print("🔹 Loading tables...")

    workers_df = load_workers(engine)
    jobs_df = load_jobs(engine)
    applications_df = load_applications(engine)
    ratings_df = load_ratings(engine)
    worker_skills_df = load_worker_skills(engine)
    job_skills_df = load_job_skills(engine)
    skill_master_df = load_skill_master(engine)

    print("✅ Tables loaded successfully.")

    # =========================
    # 4️⃣ BASIC CLEANING
    # =========================

    workers_df.drop_duplicates(inplace=True)
    jobs_df.drop_duplicates(inplace=True)
    applications_df.drop_duplicates(inplace=True)
    ratings_df.drop_duplicates(inplace=True)

    # Clean text columns only
    for col in workers_df.select_dtypes(include="object"):
        workers_df[col] = workers_df[col].fillna("").astype(str).str.strip()

    for col in jobs_df.select_dtypes(include="object"):
        jobs_df[col] = jobs_df[col].fillna("").astype(str).str.strip()

    # =========================
    # 5️⃣ FIX UUID ID COLUMNS
    # =========================

    if "id" in workers_df.columns:
        workers_df["id"] = workers_df["id"].astype(str)

    if "id" in jobs_df.columns:
        jobs_df["id"] = jobs_df["id"].astype(str)

    if "worker_id" in worker_skills_df.columns:
        worker_skills_df["worker_id"] = worker_skills_df["worker_id"].astype(str)

    if "job_id" in job_skills_df.columns:
        job_skills_df["job_id"] = job_skills_df["job_id"].astype(str)

    # =========================
    # 6️⃣ SANITY CHECKS
    # =========================

    if workers_df["id"].isnull().any():
        raise ValueError("❌ Workers table contains NULL IDs")

    if jobs_df["id"].isnull().any():
        raise ValueError("❌ Jobs table contains NULL IDs")

    print("✅ ID columns verified.")

    # =========================
    # 7️⃣ SAVE CSV FILES
    # =========================

    if save_csv:
        print("💾 Saving CSV files...")

        workers_df.to_csv("workers_df.csv", index=False)
        jobs_df.to_csv("jobs_df.csv", index=False)
        applications_df.to_csv("applications_df.csv", index=False)
        ratings_df.to_csv("ratings_df.csv", index=False)
        worker_skills_df.to_csv("worker_skills_df.csv", index=False)
        job_skills_df.to_csv("job_skills_df.csv", index=False)
        skill_master_df.to_csv("skill_master_df.csv", index=False)

        print("✅ CSV export completed.")

    return {
        "workers_df": workers_df,
        "jobs_df": jobs_df,
        "applications_df": applications_df,
        "ratings_df": ratings_df,
        "worker_skills_df": worker_skills_df,
        "job_skills_df": job_skills_df,
        "skill_master_df": skill_master_df
    }


# =========================
# 8️⃣ RUN PIPELINE
# =========================

if __name__ == "__main__":

    data = build_dataframes(save_csv=True)

    print("\n📊 Dataset Summary:")
    for name, df in data.items():
        print(f"{name}: {df.shape}")