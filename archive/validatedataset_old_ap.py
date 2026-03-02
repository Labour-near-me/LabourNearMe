import psycopg2
from collections import Counter

# -----------------------------
# PostgreSQL Connection
# -----------------------------
conn = psycopg2.connect(
    host="aws-1-ap-south-1.pooler.supabase.com",
    database="postgres",
    user="postgres.ihnlpiujpjslpgesqimj",
    password="subArAshii325",
    port="6543"
)
cursor = conn.cursor()

# -----------------------------
# Helper function to fetch all ids from a table
# -----------------------------
def get_ids(table_name, id_column='id'):
    cursor.execute(f'SELECT {id_column} FROM "{table_name}"')
    return set([row[0] for row in cursor.fetchall()])

# -----------------------------
# 1️⃣ Check foreign key integrity
# -----------------------------
print("🔹 Checking foreign key integrity...")

workers_ids = get_ids("workers")
employers_ids = get_ids("Employers")
jobs_ids = get_ids("Jobs")
skills_ids = get_ids("Skill_master")

# applications
cursor.execute('SELECT worker_id, job_id FROM applications')
applications = cursor.fetchall()
invalid_worker_apps = [w for w, j in applications if w not in workers_ids]
invalid_job_apps = [j for w, j in applications if j not in jobs_ids]

print(f"Invalid worker references in applications: {len(invalid_worker_apps)}")
print(f"Invalid job references in applications: {len(invalid_job_apps)}")

# ratings
cursor.execute('SELECT reviewer_id, reviewee_id FROM ratings')
ratings = cursor.fetchall()
invalid_reviewers = [r for r, rev in ratings if r not in employers_ids]
invalid_reviewees = [rev for r, rev in ratings if rev not in workers_ids]

print(f"Invalid reviewer references in ratings: {len(invalid_reviewers)}")
print(f"Invalid reviewee references in ratings: {len(invalid_reviewees)}")

# Job_required_skill
cursor.execute('SELECT skill_id FROM "Job_required_skill"')
job_skills = [row[0] for row in cursor.fetchall()]
invalid_job_skills = [s for s in job_skills if s not in skills_ids]
print(f"Invalid skills in Job_required_skill: {len(invalid_job_skills)}")

# Worker_skills
cursor.execute('SELECT skill_id FROM "Worker_skills"')
worker_skills = [row[0] for row in cursor.fetchall()]
invalid_worker_skills = [s for s in worker_skills if s not in skills_ids]
print(f"Invalid skills in Worker_skills: {len(invalid_worker_skills)}")

# -----------------------------
# 2️⃣ Spot check status distributions
# -----------------------------
cursor.execute('SELECT status, COUNT(*) FROM "Jobs" GROUP BY status')
job_status_counts = cursor.fetchall()
print("\nJob status distribution:")
for status, count in job_status_counts:
    print(f"  {status}: {count}")

cursor.execute('SELECT status, COUNT(*) FROM applications GROUP BY status')
app_status_counts = cursor.fetchall()
print("\nApplication status distribution:")
for status, count in app_status_counts:
    print(f"  {status}: {count}")

# -----------------------------
# 3️⃣ Random spot check: jobs and applicants with skills
# -----------------------------
import random

random_job = random.choice(list(jobs_ids))
print(f"\nRandom job_id selected for inspection: {random_job}")

# Get required skills for this job
cursor.execute('SELECT skill_id FROM "Job_required_skill" WHERE job_id=%s', (random_job,))
job_required_skills = [row[0] for row in cursor.fetchall()]
print(f"Job required skills IDs: {job_required_skills}")

# Get applicants
cursor.execute('SELECT worker_id FROM applications WHERE job_id=%s', (random_job,))
applicants = [row[0] for row in cursor.fetchall()]
print(f"Number of applicants: {len(applicants)}")

# Check applicant skills
for worker_id in applicants[:5]:  # show up to 5 applicants
    cursor.execute('SELECT skill_id FROM "Worker_skills" WHERE worker_id=%s', (worker_id,))
    worker_skills_list = [row[0] for row in cursor.fetchall()]
    match = set(worker_skills_list) & set(job_required_skills)
    print(f"  Worker {worker_id} skills: {worker_skills_list}, matches: {match}")

# -----------------------------
# 4️⃣ Check for orphan jobs (no applicants) & orphan workers (no applications)
# -----------------------------
cursor.execute('SELECT id FROM "Jobs"')
all_jobs = set([row[0] for row in cursor.fetchall()])
cursor.execute('SELECT job_id FROM applications')
jobs_with_apps = set([row[0] for row in cursor.fetchall()])
orphan_jobs = all_jobs - jobs_with_apps
print(f"\nJobs with no applications: {len(orphan_jobs)}")

cursor.execute('SELECT id FROM workers')
all_workers = set([row[0] for row in cursor.fetchall()])
cursor.execute('SELECT worker_id FROM applications')
workers_with_apps = set([row[0] for row in cursor.fetchall()])
orphan_workers = all_workers - workers_with_apps
print(f"Workers who applied to no jobs: {len(orphan_workers)}")

# -----------------------------
# 5️⃣ Close connection
# -----------------------------
cursor.close()
conn.close()
print("\n✅ Full dataset validation complete!")