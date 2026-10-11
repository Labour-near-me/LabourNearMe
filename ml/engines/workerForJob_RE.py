"""
ml/engines/jobForWorkers_RE.py

Worker -> Job recommendation engine.

Responsibilities:
- Load workers and open jobs from Supabase
- Load live worker/job skill mappings from Supabase
- Calculate embedding similarity
- Enforce required skill overlap
- Calculate location distance
- Prioritize nearby jobs
- Calculate live worker cluster using KMeans
- Generate ML-based recommendation score
- Combine skill, proximity, semantic similarity and ML signals
- Return transparent matching information
"""

import os
import ast
import pickle
from threading import Lock
from time import monotonic

import numpy as np
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sklearn.metrics.pairwise import cosine_similarity
from ml.engines.skill_taxonomy import (
    matched_required_skills,
    normalize_skill_name,
    prepare_skill_embeddings,
)


# ============================================================
# CONFIG
# ============================================================

SIMILARITY_THRESHOLD = 0.15
MIN_SKILL_OVERLAP = 1
MAX_DISTANCE_KM = 50
DATA_REFRESH_INTERVAL_SECONDS = 15

_DATA_REFRESH_LOCK = Lock()
_DATA_LAST_REFRESHED_AT = 0.0

# Explicit ranking weights.
#
# Skill compatibility is the strongest signal.
# Proximity is the second strongest signal.
# Semantic similarity and the trained ML model remain
# supporting signals.
SKILL_WEIGHT = 0.40
PROXIMITY_WEIGHT = 0.25
SEMANTIC_WEIGHT = 0.20
ML_WEIGHT = 0.15


# ============================================================
# DATABASE
# ============================================================

load_dotenv()

engine = create_engine(
    os.getenv("DATABASE_URL")
)


# ============================================================
# MODEL PATHS
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "predictive_model.pkl"
)

FEATURE_PATH = os.path.join(
    BASE_DIR,
    "models",
    "feature_columns.pkl"
)

KMEANS_PATH = os.path.join(
    BASE_DIR,
    "models",
    "kmeans_model.pkl"
)


# ============================================================
# LOAD MODELS
# ============================================================

with open(MODEL_PATH, "rb") as f:
    MODEL = pickle.load(f)

with open(FEATURE_PATH, "rb") as f:
    FEATURE_COLUMNS = pickle.load(f)

with open(KMEANS_PATH, "rb") as f:
    KMEANS_MODEL = pickle.load(f)


# ============================================================
# GLOBAL DATA
# ============================================================

WORKERS_DF = pd.DataFrame()
JOBS_DF = pd.DataFrame()

WORKER_VEC = np.array([])
JOB_VEC = np.array([])

JOB_SKILL_MAP = {}
WORKER_SKILL_MAP = {}


# ============================================================
# SAFE FLOAT
# ============================================================

def safe_float(value, default=0.0):
    try:
        if value is None:
            return default

        value = float(value)

        if np.isnan(value) or np.isinf(value):
            return default

        return value

    except Exception:
        return default


# ============================================================
# LOAD JOB SKILLS
# ============================================================

def load_job_skills():
    """
    Load live job -> skill mappings from Supabase.

    Returns:
        {
            "job_uuid": {"skill_uuid", "skill_uuid", ...}
        }
    """

    df = pd.read_sql(
        '''SELECT jrs.job_id,
                  COALESCE(intended_skill.skill_name, sm.skill_name) AS skill_name
           FROM "Job_required_skill" AS jrs
           JOIN "Skill_master" AS sm ON sm.id = jrs.skill_id
           LEFT JOIN "Skill_master" AS intended_skill
             ON intended_skill.id::text = sm.skill_name''',
        engine
    )

    job_skill_map = {}

    for _, row in df.iterrows():

        job_id = str(row["job_id"])
        skill_name = normalize_skill_name(row["skill_name"])

        job_skill_map.setdefault(
            job_id,
            set()
        ).add(skill_name)

    return job_skill_map


# ============================================================
# LOAD WORKER SKILLS
# ============================================================

def load_worker_skills():
    """
    Load live worker -> skill mappings from Supabase.

    Returns:
        {
            "worker_uuid": {"skill_uuid", "skill_uuid", ...}
        }
    """

    df = pd.read_sql(
        '''SELECT ws.worker_id, sm.skill_name
           FROM "Worker_skills" AS ws
           JOIN "Skill_master" AS sm ON sm.id = ws.skill_id''',
        engine
    )

    worker_skill_map = {}

    for _, row in df.iterrows():

        worker_id = str(row["worker_id"])
        skill_name = normalize_skill_name(row["skill_name"])

        worker_skill_map.setdefault(
            worker_id,
            set()
        ).add(skill_name)

    return worker_skill_map


# ============================================================
# INITIAL SKILL MAPS
# ============================================================

JOB_SKILL_MAP = {}
WORKER_SKILL_MAP = {}


# ============================================================
# GET WORKER SKILLS
# ============================================================

def get_worker_skills(worker_id):
    """
    Return worker skill IDs from the live skill map.
    """

    return WORKER_SKILL_MAP.get(
        str(worker_id),
        set()
    )


# ============================================================
# LOAD WORKERS + OPEN JOBS
# ============================================================

def load_data():

    with engine.connect() as conn:

        workers = pd.read_sql(
            "SELECT * FROM workers",
            conn
        )

        jobs = pd.read_sql(
            'SELECT * FROM "Jobs" WHERE status = \'open\'',
            conn
        )

    workers["id"] = workers["id"].astype(str)
    jobs["id"] = jobs["id"].astype(str)

    workers["rating"] = workers["rating"].fillna(0)
    jobs["budget"] = jobs["budget"].fillna(0)

    return workers, jobs


# ============================================================
# EMBEDDING CONVERSION
# ============================================================

def convert_embeddings(df, column):

    vectors = []

    for value in df[column]:

        try:

            if isinstance(value, str):

                vectors.append(
                    np.array(
                        ast.literal_eval(value)
                    )
                )

            elif isinstance(value, list):

                vectors.append(
                    np.array(value)
                )

            else:

                vectors.append(
                    np.zeros(384)
                )

        except Exception:

            vectors.append(
                np.zeros(384)
            )

    return np.array(vectors)


# ============================================================
# REFRESH DATA
# ============================================================

def refresh_data(force=False):

    global WORKERS_DF
    global JOBS_DF
    global WORKER_VEC
    global JOB_VEC
    global JOB_SKILL_MAP
    global WORKER_SKILL_MAP
    global _DATA_LAST_REFRESHED_AT

    with _DATA_REFRESH_LOCK:
        if (
            not force
            and _DATA_LAST_REFRESHED_AT
            and monotonic() - _DATA_LAST_REFRESHED_AT < DATA_REFRESH_INTERVAL_SECONDS
        ):
            return

        WORKERS_DF, JOBS_DF = load_data()

        WORKER_VEC = convert_embeddings(
            WORKERS_DF,
            "worker_embedding"
        )

        JOB_VEC = convert_embeddings(
            JOBS_DF,
            "job_embedding"
        )

        # Refresh live skill mappings whenever recommendation data is refreshed.
        JOB_SKILL_MAP = load_job_skills()
        WORKER_SKILL_MAP = load_worker_skills()
        prepare_skill_embeddings(
            set().union(*JOB_SKILL_MAP.values(), *WORKER_SKILL_MAP.values())
            if JOB_SKILL_MAP or WORKER_SKILL_MAP
            else set()
        )
        _DATA_LAST_REFRESHED_AT = monotonic()


# ============================================================
# INITIAL LOAD
# ============================================================

# Data is refreshed by the recommendation function when first needed, rather
# than during API module import. This keeps ordinary API startup lightweight.


# ============================================================
# HAVERSINE DISTANCE
# ============================================================

def haversine(
    lat1,
    lon1,
    lat2,
    lon2
):

    try:

        R = 6371

        lat1, lon1, lat2, lon2 = map(
            np.radians,
            [
                lat1,
                lon1,
                lat2,
                lon2
            ]
        )

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = (
            np.sin(dlat / 2) ** 2
            +
            np.cos(lat1)
            * np.cos(lat2)
            * np.sin(dlon / 2) ** 2
        )

        distance = (
            R
            * 2
            * np.arcsin(
                np.sqrt(a)
            )
        )

        return safe_float(
            distance,
            999
        )

    except Exception:

        return 999


# ============================================================
# PROXIMITY SCORE
# ============================================================

def calculate_proximity_score(distance_km):
    """
    Convert distance into a 0-1 proximity score.

    0 km  -> 1.0
    25 km -> 0.5
    50 km -> 0.0

    Candidates above MAX_DISTANCE_KM are not eligible and
    should already have been filtered out.
    """

    distance_km = safe_float(
        distance_km,
        MAX_DISTANCE_KM
    )

    if distance_km >= MAX_DISTANCE_KM:
        return 0.0

    if distance_km <= 0:
        return 1.0

    score = (
        1
        - (
            distance_km
            / MAX_DISTANCE_KM
        )
    )

    return max(
        0.0,
        min(1.0, score)
    )


# ============================================================
# NORMALIZE ML SCORES
# ============================================================

def normalize_ml_scores(scores):
    """
    Normalize ML scores for the current recommendation set
    into the 0-1 range.

    This prevents raw ML score magnitude from overpowering
    the explicit skill/proximity/semantic signals.
    """

    if not scores:
        return []

    values = np.array(
        [
            safe_float(score)
            for score in scores
        ],
        dtype=float
    )

    min_value = np.min(values)
    max_value = np.max(values)

    if np.isclose(
        max_value,
        min_value
    ):
        return [
            0.5
            for _ in values
        ]

    normalized = (
        (values - min_value)
        /
        (max_value - min_value)
    )

    return [
        safe_float(value)
        for value in normalized
    ]


# ============================================================
# FINAL RANKING SCORE
# ============================================================

def calculate_final_score(
    skill_similarity,
    proximity_score,
    semantic_similarity,
    normalized_ml_score
):

    score = (
        SKILL_WEIGHT
        * skill_similarity
        +
        PROXIMITY_WEIGHT
        * proximity_score
        +
        SEMANTIC_WEIGHT
        * semantic_similarity
        +
        ML_WEIGHT
        * normalized_ml_score
    )

    return safe_float(
        max(
            0.0,
            min(1.0, score)
        )
    )


# ============================================================
# WORKER CLUSTER
# ============================================================

def get_worker_cluster(worker_vector):

    try:

        return int(
            KMEANS_MODEL.predict(
                worker_vector.reshape(
                    1,
                    -1
                )
            )[0]
        )

    except Exception:

        return -1


# ============================================================
# MAIN RECOMMENDATION FUNCTION
# ============================================================

def recommend_jobs_for_worker(
    worker_id,
    top_n=5
):

    refresh_data()

    worker_id = str(worker_id)

    worker_match = WORKERS_DF[
        WORKERS_DF["id"] == worker_id
    ]

    if worker_match.empty:
        return []

    worker_row = worker_match.iloc[0]

    worker_indices = WORKERS_DF.index[
        WORKERS_DF["id"] == worker_id
    ]

    worker_idx = worker_indices[0]

    worker_vector = WORKER_VEC[
        worker_idx
    ].reshape(1, -1)

    similarities = cosine_similarity(
        worker_vector,
        JOB_VEC
    )[0]

    worker_skills = get_worker_skills(
        worker_id
    )

    worker_cluster = get_worker_cluster(
        WORKER_VEC[worker_idx]
    )

    eligible_candidates = []

    # ========================================================
    # FIRST PASS:
    # Apply hard eligibility filters and calculate ML scores.
    # ========================================================

    for i, job in JOBS_DF.iterrows():

        job_id = str(job["id"])

        job_skills = JOB_SKILL_MAP.get(
            job_id,
            set()
        )

        matched_skills = matched_required_skills(
            worker_skills,
            job_skills
        )

        # ----------------------------------------------------
        # REQUIRED SKILL RULE
        # ----------------------------------------------------
        #
        # Jobs without a required-skill mapping are excluded.
        #
        # This prevents unrelated semantic-only jobs such as
        # Electrician from being recommended to a worker who
        # has no matching skill.
        # ----------------------------------------------------

        if not job_skills:
            continue

        if len(matched_skills) < MIN_SKILL_OVERLAP:
            continue

        skill_similarity_score = (
            len(matched_skills)
            /
            max(
                len(job_skills),
                1
            )
        )

        # ----------------------------------------------------
        # EMBEDDING SIMILARITY
        # ----------------------------------------------------

        similarity = safe_float(
            similarities[i]
        )

        similarity = max(
            0,
            min(1, similarity)
        )

        if similarity < SIMILARITY_THRESHOLD:
            continue

        # ----------------------------------------------------
        # DISTANCE
        # ----------------------------------------------------

        distance = haversine(
            worker_row["location_lat"],
            worker_row["location_lng"],
            job["location_lat"],
            job["location_lng"]
        )

        if distance > MAX_DISTANCE_KM:
            continue

        proximity = calculate_proximity_score(
            distance
        )

        # ----------------------------------------------------
        # FEATURES FOR TRAINED ML MODEL
        # ----------------------------------------------------

        experience = safe_float(
            worker_row.get(
                "experience_years",
                0
            )
        )

        rating = safe_float(
            worker_row.get(
                "rating",
                0
            )
        )

        budget = safe_float(
            job.get(
                "budget",
                0
            )
        )

        features = {

            "skill_similarity":
                skill_similarity_score,

            "experience_bucket":
                0
                if experience <= 2
                else (
                    1
                    if experience <= 5
                    else 2
                ),

            "avg_rating":
                rating,

            "distance_km":
                distance,

            "budget":
                budget,

            "worker_cluster":
                worker_cluster,
        }

        # ----------------------------------------------------
        # COMPLETE FEATURE VECTOR
        # ----------------------------------------------------

        for column in FEATURE_COLUMNS:

            if column not in features:
                features[column] = 0

        X = pd.DataFrame(
            [features]
        )[FEATURE_COLUMNS]

        # ----------------------------------------------------
        # ML SCORE
        # ----------------------------------------------------

        try:

            ml_score = safe_float(
                MODEL.predict(X)[0]
            )

        except Exception:

            ml_score = 0.0

        eligible_candidates.append({

            "job_id":
                job_id,

            "title":
                job["title"],

            "similarity":
                similarity,

            "skill_similarity":
                skill_similarity_score,

            "distance_km":
                distance,

            "proximity_score":
                proximity,

            "budget":
                budget,

            "ml_score":
                ml_score,

        })

    # ========================================================
    # NORMALIZE ML SCORES
    # ========================================================

    ml_scores = [
        candidate["ml_score"]
        for candidate in eligible_candidates
    ]

    normalized_ml_scores = normalize_ml_scores(
        ml_scores
    )

    # ========================================================
    # FINAL RANKING
    # ========================================================

    recommendations = []

    for candidate, normalized_ml in zip(
        eligible_candidates,
        normalized_ml_scores
    ):

        final_score = calculate_final_score(
            skill_similarity=
                candidate["skill_similarity"],

            proximity_score=
                candidate["proximity_score"],

            semantic_similarity=
                candidate["similarity"],

            normalized_ml_score=
                normalized_ml
        )

        recommendations.append({

            "job_id":
                candidate["job_id"],

            "title":
                candidate["title"],

            "final_score":
                round(
                    final_score,
                    3
                ),

            "ml_score":
                round(
                    candidate["ml_score"],
                    3
                ),

            "similarity":
                round(
                    candidate["similarity"],
                    3
                ),

            "skill_similarity":
                round(
                    candidate["skill_similarity"],
                    3
                ),

            "distance_km":
                round(
                    candidate["distance_km"],
                    2
                ),

            "proximity_score":
                round(
                    candidate["proximity_score"],
                    3
                ),

            "budget":
                candidate["budget"],

            "match_type":
                "skill_matched",

        })

    return sorted(
        recommendations,
        key=lambda x: x["final_score"],
        reverse=True
    )[:top_n]
