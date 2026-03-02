import psycopg2
import random
from datetime import datetime
import uuid

# -----------------------------
# CONFIG: PostgreSQL Connection
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
# PARAMETERS
# -----------------------------
NUM_WORKERS = 500
NUM_EMPLOYERS = 50
NUM_JOBS = 2000
MAX_SKILLS_PER_WORKER = 5
MAX_SKILLS_PER_JOB = 3
CITY_LAT_RANGE = (23.1500, 23.2000)
CITY_LNG_RANGE = (75.7500, 75.8500)
ALLOWED_JOB_STATUS = ['open', 'assigned', 'completed', 'cancelled']
JOB_STATUS_WEIGHTS = [0.5, 0.2, 0.2, 0.1]  # matches 4 statuses

# -----------------------------
# CLEAN EXISTING DATA
# -----------------------------
tables_to_clear = [
    "applications", "ratings", "Job_required_skill", "Jobs",
]

for table in tables_to_clear:
    try:
        cursor.execute(f'DELETE FROM "{table}"')
        conn.commit()
        print(f"🧹 Cleared table: {table}")
    except Exception as e:
        print(f"❌ Failed to clear table {table}: {e}")
        conn.rollback()

# -----------------------------
# FETCH SKILLS
# -----------------------------
cursor.execute('SELECT id, skill_name FROM "Skill_master"')
skill_master = cursor.fetchall()
print(f"✅ Fetched {len(skill_master)} skills from Skill_master")

def pick_random_skills(skill_list, min_skills, max_skills):
    count = random.randint(min_skills, max_skills)
    return random.sample(skill_list, count)
# -----------------------------
# FETCH EXISTING EMPLOYERS
# -----------------------------
cursor.execute('SELECT id, employer_name FROM "Employers"')
employers_db = cursor.fetchall()
employers = [{'id': e[0], 'name': e[1]} for e in employers_db]

# -----------------------------
# FETCH EXISTING WORKERS
# -----------------------------
cursor.execute('SELECT id, rating FROM "workers"')
workers_db = cursor.fetchall()
workers = []

for w_id, w_rating in workers_db:
    # fetch worker skills
    cursor.execute('SELECT skill_id FROM "Worker_skills" WHERE worker_id=%s', (w_id,))
    skills = [s[0] for s in cursor.fetchall()]
    workers.append({'id': w_id, 'skills': skills, 'rating': w_rating})
# -----------------------------
# SKILL → CATEGORY MAPPING
# -----------------------------
skill_category_map = {
    "Gate Monitoring": "Security Guarding",
    "Car Engine Repair": "Mechanic",
    "Wood Polishing": "Carpentry",
    "Harvesting": "Agricultural Labor",
    "Night Patrolling": "Security Guarding",
    "Crowd Assistance": "Event Support",
    "Housekeeping": "Domestic Help",
    "Blouse Designing": "Tailor and Sewers",
    "General Pest Spraying": "Pest Control",
    "Rodent Control": "Pest Control",
    "Inventory Assistance": "Shopper Assistant",
    "Sofa Shampooing": "Deep Cleaning",
    "Microwave Repair": "Appliance Repair",
    "Brick Carrying": "Masonry Helper",
    "Switchboard Repair": "Electrical",
    "RO Installation": "Technician",
    "Unloading Goods": "Moving and Packing",
    "Basic Cooking": "Domestic Help",
    "Indian Cooking": "Cook/Chef",
    "Modular Kitchen Fitting": "Carpentry",
    "Interior Cleaning": "Car Washing",
    "Cement Mixing": "Masonry Helper",
    "Furniture Assembly": "Carpentry",
    "Oil Change Service": "Mechanic",
    "Termite Treatment": "Pest Control",
    "Fan Installation": "Electrical",
    "Exterior Painting": "Painting",
    "Garden Landscaping": "Gardening",
    "Irrigation Setup": "Agricultural Labor",
    "Cabinet Making": "Carpentry",
    "Grocery Picking": "Shopper Assistant",
    "Kitchen Management": "Cook/Chef",
    "Alterations": "Tailor and Sewers",
    "Exterior Car Wash": "Car Washing",
    "Washing Machine Repair": "Appliance Repair",
    "Interior Painting": "Painting",
    "Arc Welding": "Welder",
    "Utensil Washing": "Domestic Help",
    "Equipment Arrangement": "Event Support",
    "Tile Scrubbing": "Deep Cleaning",
    "Route Navigation": "Driver",
    "Ironing": "Laundry",
    "Visitor Log Management": "Security Guarding",
    "Water Tank Installation": "Plumbing",
    "Floor Polishing": "Marble Mistries",
    "Plant Pruning": "Gardening",
    "Gas Welding": "Welder",
    "AC Installation": "Technician",
    "Car Polishing": "Car Washing",
    "Truck Loading": "Loading",
    "Drain Cleaning": "Plumbing",
    "Inverter Installation": "Electrical",
    "Commercial Driving": "Driver",
    "Patient Assistance": "Elder Care",
    "Child Supervision": "Babysitter",
    "Site Assistance": "Masonry Helper",
    "Stitching": "Tailor and Sewers",
    "South Indian Cooking": "Cook/Chef",
    "Stage Setup": "Event Support",
    "Lawn Maintenance": "Gardening",
    "Office Cleaning": "Cleaning",
    "House Cleaning": "Cleaning",
    "Wall Putty": "Painting",
    "Crop Planting": "Agricultural Labor",
    "Lighting Setup": "Electrical",
    "Material Shifting": "Loading",
    "Refrigerator Repair": "Appliance Repair",
    "Waterproof Coating": "Painting",
    "Medicine Reminders": "Elder Care",
    "Car Driving": "Driver",
    "Loading Furniture": "Moving and Packing",
    "Bathroom Cleaning": "Cleaning",
    "Homework Assistance": "Babysitter",
    "CCTV Setup": "Technician",
    "Bulk Cooking": "Cook/Chef",
    "Pipe Fitting": "Plumbing",
    "Kitchen Deep Cleaning": "Deep Cleaning",
    "Marble Cutting": "Marble Mistries",
    "Metal Fabrication": "Welder",
    "Door Installation": "Carpentry",
    "Two Wheeler Repair": "Mechanic",
    "Clothes Washing": "Laundry",
    "TV Repair": "Appliance Repair",
    "Bathroom Installation": "Plumbing",
    "Wiring Installation": "Electrical",
    "Warehouse Loading": "Loading",
    "Customer Help Desk": "Shopper Assistant",
    "Floor Scrubbing": "Cleaning",
    "Leak Repair": "Plumbing",
    "Infant Care": "Babysitter",
    "Packing Household Items": "Moving and Packing",
    "Tile Laying": "Marble Mistries",
    "Mobility Support": "Elder Care",
    "Dry Cleaning Handling": "Laundry"
}

job_templates = [
    "We need a skilled {skill} to handle {category} tasks professionally.",
    "Looking for an experienced {skill} for {category} work.",
    "Job requires a {skill} expert to perform {category} efficiently."
]

feedback_templates = [
    "Worker performed {skill} exceptionally well. Communication was {quality}.",
    "Excellent work on {skill}, timely completion and attention to detail.",
    "{skill} task was completed successfully. {quality} during the process."
]

qualities = ["excellent", "good", "average", "poor"]

def generate_job_description(skill_name):
    category = skill_category_map.get(skill_name, "General")
    return random.choice(job_templates).format(skill=skill_name, category=category.lower())

def generate_feedback(skill_name):
    return random.choice(feedback_templates).format(skill=skill_name, quality=random.choice(qualities))

# -----------------------------
# GENERATE JOBS & JOB_REQUIRED_SKILL
# -----------------------------
jobs = []
for i in range(NUM_JOBS):
    job_id = str(uuid.uuid4())
    employer = random.choice(employers)
    skill_name = random.choice([s[1] for s in skill_master])
    title = f"{skill_category_map.get(skill_name, 'General')} Job {i+1} - {skill_name}"
    description = generate_job_description(skill_name)
    required_skills = pick_random_skills(skill_master, 1, MAX_SKILLS_PER_JOB)
    budget = round(500 + len(required_skills)*200 + random.randint(-50,50),2)
    status = random.choices(ALLOWED_JOB_STATUS, weights=JOB_STATUS_WEIGHTS, k=1)[0]
    lat = round(random.uniform(*CITY_LAT_RANGE),6)
    lng = round(random.uniform(*CITY_LNG_RANGE),6)

    # Insert Jobs
    cursor.execute("""
        INSERT INTO "Jobs" (id, employer_id, title, description, budget, status, created_at, location_lat, location_lng)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, (job_id, employer['id'], title, description, budget, status, datetime.now(), lat, lng))

    # Insert Job_required_skill
    for skill_id, _ in required_skills:
        cursor.execute("""
            INSERT INTO "Job_required_skill" (job_id, skill_id) VALUES (%s,%s)
        """, (job_id, skill_id))

    jobs.append({
        'id': job_id,
        'skills': [s[0] for s in required_skills],
        'status': status,
        'employer': employer['id'],
        'task': skill_name
    })

conn.commit()
print(f"✅ Created {len(jobs)} Jobs and Job_required_skill entries")

# -----------------------------
# GENERATE APPLICATIONS & RATINGS
# -----------------------------
app_count = 0
rating_count = 0
for job in jobs:
    for worker in random.sample(workers, k=10):
        try:
            if set(worker['skills']) & set(job['skills']):
                status = random.choices(['pending','accepted','shortlisted','rejected'], weights=[0.4,0.3,0.2,0.1], k=1)[0]
                cursor.execute("""
                    INSERT INTO "applications" (id, job_id, worker_id, status, applied_at)
                    VALUES (%s,%s,%s,%s,%s)
                """, (str(uuid.uuid4()), job['id'], worker['id'], status, datetime.now()))
                app_count += 1

                if job['status']=='completed' and status in ['accepted','shortlisted']:
                    rating_value = round(min(5,max(1,worker['rating']+random.uniform(-1,1))),0)
                    cursor.execute("""
                        INSERT INTO "ratings" (id, job_id, reviewer_id, reviewee_id, rating_value, feedbck, created_at)
                        VALUES (%s,%s,%s,%s,%s,%s,%s)
                    """, (str(uuid.uuid4()), job['id'], job['employer'], worker['id'], rating_value, generate_feedback(job['task']), datetime.now()))
                    rating_count += 1
        except Exception as e:
            print(f"❌ Error creating application/rating: {e}")
            conn.rollback()

conn.commit()
print(f"✅ Created {app_count} applications and {rating_count} ratings")

# -----------------------------
# UPDATE EMPLOYER RATINGS
# -----------------------------
for employer in employers:
    cursor.execute("""
        SELECT AVG(rating_value) FROM ratings r
        JOIN "Jobs" j ON j.id = r.job_id
        WHERE j.employer_id=%s
    """, (employer['id'],))
    avg_rating = cursor.fetchone()[0]
    if avg_rating:
        cursor.execute("""
            UPDATE "Employers" SET rating=%s WHERE id=%s
        """, (round(avg_rating,2), employer['id']))

conn.commit()
print("🎉 Jobs, Applications, Ratings generation complete and Employer ratings updated!")