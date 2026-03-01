import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

# =========================
# 1️⃣ LOAD ENV VARIABLES
# =========================

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")


def get_db_connection():
    connection_string = (
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    engine = create_engine(connection_string)
    return engine

# =========================
# 2️⃣ EXTRACT TABLES
# =========================

def load_workers(engine):
    query = "SELECT * FROM workers;"
    return pd.read_sql(query, engine)


def load_jobs(engine):
    query = "SELECT * FROM \"Jobs\";"
    return pd.read_sql(query, engine)


def load_applications(engine):
    query = "SELECT * FROM applications;"
    return pd.read_sql(query, engine)


def load_ratings(engine):
    query = "SELECT * FROM ratings;"
    return pd.read_sql(query, engine)


def load_worker_skills(engine):
    query = "SELECT * FROM \"Worker_skills\";"
    return pd.read_sql(query, engine)


def load_job_skills(engine):
    query = "SELECT * FROM \"Job_required_skill\";"
    return pd.read_sql(query, engine)


def load_skill_master(engine):
    query = "SELECT * FROM \"Skill_master\";"
    return pd.read_sql(query, engine)


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
    # 4️⃣ OPTIONAL: CLEANING
    # =========================

    # Remove duplicates
    workers_df = workers_df.drop_duplicates()
    jobs_df = jobs_df.drop_duplicates()
    applications_df = applications_df.drop_duplicates()
    ratings_df = ratings_df.drop_duplicates()

    # Fill missing values (basic handling)
    workers_df.fillna("", inplace=True)
    jobs_df.fillna("", inplace=True)

    # =========================
    # 5️⃣ SAVE IF REQUIRED
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

    return {
        "workers_df": workers_df,
        "jobs_df": jobs_df,
        "applications_df": applications_df,
        "ratings_df": ratings_df,
        "worker_skills_df": worker_skills_df,
        "job_skills_df": job_skills_df,
        "skill_master_df": skill_master_df
    }


if __name__ == "__main__":
    data = build_dataframes(save_csv=True)

    print("\n📊 Dataset Summary:")
    for name, df in data.items():
        print(f"{name}: {df.shape}")