"""
ml/test_RS.py

Diagnostic and validation test for the LabourNearMe
recommendation system.

Tests:
1. Proximity scoring
2. Ranking score range
3. Job -> Workers
4. Worker -> Jobs
5. Skill filtering
6. Rating influence
7. Ranking order
8. Top-N behavior
"""

from ml.engines import workerForJob_RE as worker_engine
from ml.engines import jobForWorkers_RE as job_engine

import pandas as pd


# ============================================================
# LOAD SKILL MASTER
# ============================================================

skill_master = pd.read_csv(
    "data/raw/skill_master_df.csv",
    dtype=str
)

skill_master["id"] = (
    skill_master["id"]
    .astype(str)
)

skill_master["skill_name"] = (
    skill_master["skill_name"]
    .astype(str)
)

skill_map = dict(
    zip(
        skill_master["id"],
        skill_master["skill_name"]
    )
)


# ============================================================
# HELPERS
# ============================================================

def skill_names(skill_ids):

    names = []

    for skill_id in sorted(
        skill_ids
    ):

        names.append(
            skill_map.get(
                str(skill_id),
                f"Unknown skill ({skill_id})"
            )
        )

    return names


def print_skills(
    label,
    skill_ids
):

    names = skill_names(
        skill_ids
    )

    print(label)

    if names:

        print(
            ", ".join(names)
        )

    else:

        print(
            "No skills found"
        )


def validate_job_results(workers):

    for worker in workers:

        assert (
            worker["match_type"]
            ==
            "skill_matched"
        ), (
            "A semantic-only worker "
            "was returned."
        )

        assert (
            worker["skill_similarity"]
            > 0
        ), (
            "Worker with zero skill "
            "overlap was returned."
        )

        assert (
            worker["distance_km"]
            <= job_engine.MAX_DISTANCE_KM
        ), (
            "Worker beyond maximum "
            "distance was returned."
        )

        assert (
            worker["similarity"]
            >= job_engine.SIMILARITY_THRESHOLD
        ), (
            "Worker below semantic "
            "similarity threshold "
            "was returned."
        )

        assert (
            0
            <= worker["final_score"]
            <= 1
        ), (
            "Worker final score is "
            "outside 0-1 range."
        )

        assert (
            0
            <= worker["rating_score"]
            <= 1
        ), (
            "Rating score is outside "
            "0-1 range."
        )


def validate_worker_results(jobs):

    for job in jobs:

        assert (
            job["match_type"]
            ==
            "skill_matched"
        ), (
            "A semantic-only job "
            "was returned."
        )

        assert (
            job["skill_similarity"]
            > 0
        ), (
            "Job with zero skill "
            "overlap was returned."
        )

        assert (
            job["distance_km"]
            <= worker_engine.MAX_DISTANCE_KM
        ), (
            "Job beyond maximum "
            "distance was returned."
        )

        assert (
            job["similarity"]
            >= worker_engine.SIMILARITY_THRESHOLD
        ), (
            "Job below semantic "
            "similarity threshold "
            "was returned."
        )

        assert (
            0
            <= job["final_score"]
            <= 1
        ), (
            "Job final score is "
            "outside 0-1 range."
        )


def assert_descending(results):

    scores = [
        result["final_score"]
        for result in results
    ]

    assert scores == sorted(
        scores,
        reverse=True
    ), (
        "Results are not sorted "
        "by final score."
    )


# ============================================================
# REFRESH BOTH ENGINES
# ============================================================

print(
    "\nRefreshing recommendation data..."
)

job_engine.refresh_data()
worker_engine.refresh_data()

print(
    "Data refresh: PASS"
)


# ============================================================
# TEST 0
# PROXIMITY SCORE
# ============================================================

print(
    "\n=============================="
)

print(
    "TEST 0: PROXIMITY SCORING"
)

print(
    "=============================="
)

proximity_tests = {
    0: 1.0,
    5: 0.9,
    25: 0.5,
    50: 0.0,
}

for distance, expected in proximity_tests.items():

    actual = job_engine.calculate_proximity_score(
        distance
    )

    assert abs(
        actual - expected
    ) < 0.0001, (
        f"Proximity score failed "
        f"for {distance} km: "
        f"expected {expected}, "
        f"got {actual}"
    )

    print(
        f"{distance:>2} km -> "
        f"{actual:.3f} PASS"
    )

print(
    "\nProximity scoring: PASS"
)


# ============================================================
# TEST 1
# JOB -> WORKER SCORE RANGE
# ============================================================

print(
    "\n=============================="
)

print(
    "TEST 1: JOB -> WORKER SCORE"
)

print(
    "=============================="
)

score = job_engine.calculate_final_score(
    skill_similarity=1.0,
    proximity_score=1.0,
    rating_score=1.0,
    semantic_similarity=1.0,
    normalized_ml_score=1.0,
)

assert 0.0 <= score <= 1.0

print(
    f"Maximum possible score: "
    f"{score:.3f} PASS"
)


score = job_engine.calculate_final_score(
    skill_similarity=0.0,
    proximity_score=0.0,
    rating_score=0.0,
    semantic_similarity=0.0,
    normalized_ml_score=0.0,
)

assert 0.0 <= score <= 1.0

print(
    f"Minimum possible score: "
    f"{score:.3f} PASS"
)


# ============================================================
# TEST 2
# PRIORITY LOGIC
# ============================================================

print(
    "\n=============================="
)

print(
    "TEST 2: PRIORITY LOGIC"
)

print(
    "=============================="
)


# Higher skill similarity should improve score.

low_skill_score = job_engine.calculate_final_score(
    skill_similarity=0.5,
    proximity_score=1.0,
    rating_score=1.0,
    semantic_similarity=1.0,
    normalized_ml_score=0.5,
)

high_skill_score = job_engine.calculate_final_score(
    skill_similarity=1.0,
    proximity_score=1.0,
    rating_score=1.0,
    semantic_similarity=1.0,
    normalized_ml_score=0.5,
)

assert high_skill_score > low_skill_score

print(
    "Higher skill similarity -> higher score: PASS"
)


# Closer distance should improve score.

near_score = job_engine.calculate_final_score(
    skill_similarity=1.0,
    proximity_score=1.0,
    rating_score=1.0,
    semantic_similarity=1.0,
    normalized_ml_score=0.5,
)

far_score = job_engine.calculate_final_score(
    skill_similarity=1.0,
    proximity_score=0.0,
    rating_score=1.0,
    semantic_similarity=1.0,
    normalized_ml_score=0.5,
)

assert near_score > far_score

print(
    "Closer worker -> higher score: PASS"
)


# Higher rating should improve score.

low_rating_score = job_engine.calculate_final_score(
    skill_similarity=1.0,
    proximity_score=1.0,
    rating_score=0.0,
    semantic_similarity=1.0,
    normalized_ml_score=0.5,
)

high_rating_score = job_engine.calculate_final_score(
    skill_similarity=1.0,
    proximity_score=1.0,
    rating_score=1.0,
    semantic_similarity=1.0,
    normalized_ml_score=0.5,
)

assert high_rating_score > low_rating_score

print(
    "Higher worker rating -> higher score: PASS"
)


# ============================================================
# TEST 3
# JOB -> WORKERS
# ============================================================

print(
    "\n=============================="
)

print(
    "TEST 3: WORKERS FOR A JOB"
)

print(
    "=============================="
)


job_engine.refresh_data()

if job_engine.JOBS_DF.empty:

    print(
        "\nNo open jobs found."
    )

else:

    # Find an open job which actually has skills.
    selected_job = None

    for _, candidate_job in (
        job_engine.JOBS_DF.iterrows()
    ):

        candidate_id = str(
            candidate_job["id"]
        )

        candidate_skills = (
            job_engine.JOB_SKILL_MAP.get(
                candidate_id,
                set()
            )
        )

        if candidate_skills:

            selected_job = candidate_job
            break

    if selected_job is None:

        print(
            "\nNo open job with required "
            "skills was found."
        )

    else:

        job_id = str(
            selected_job["id"]
        )

        job_title = selected_job["title"]

        print(
            f"\nJob Selected: {job_title}"
        )

        job_skill_ids = (
            job_engine.JOB_SKILL_MAP.get(
                job_id,
                set()
            )
        )

        print()

        print_skills(
            "Required Skills:",
            job_skill_ids
        )

        workers = (
            job_engine.recommend_workers_for_job(
                job_id,
                top_n=5
            )
        )

        print(
            "\nRecommended Workers:\n"
        )

        if not workers:

            print(
                "No workers matched the "
                "current skill/similarity/"
                "distance filters."
            )

        else:

            validate_job_results(
                workers
            )

            assert_descending(
                workers
            )

            for i, worker in enumerate(
                workers,
                1
            ):

                worker_id = str(
                    worker["worker_id"]
                )

                worker_skill_ids = (
                    job_engine.WORKER_SKILL_MAP.get(
                        worker_id,
                        set()
                    )
                )

                print(
                    f"{i}. Worker ID: "
                    f"{worker_id}"
                )

                print(
                    "   Skills:",
                    (
                        ", ".join(
                            skill_names(
                                worker_skill_ids
                            )
                        )
                        if worker_skill_ids
                        else
                        "No skills found"
                    )
                )

                print(
                    f"   Distance: "
                    f"{float(worker['distance_km']):.2f} km"
                )

                print(
                    f"   Proximity Score: "
                    f"{float(worker['proximity_score']):.3f}"
                )

                print(
                    f"   Rating: "
                    f"{float(worker['rating']):.2f}"
                )

                print(
                    f"   Rating Score: "
                    f"{float(worker['rating_score']):.3f}"
                )

                print(
                    f"   Embedding Similarity: "
                    f"{float(worker['similarity']):.3f}"
                )

                print(
                    f"   Skill Similarity: "
                    f"{float(worker['skill_similarity']):.3f}"
                )

                print(
                    f"   ML Score: "
                    f"{float(worker['ml_score']):.3f}"
                )

                print(
                    f"   Final Score: "
                    f"{float(worker['final_score']):.3f}"
                )

                print(
                    f"   Match Type: "
                    f"{worker['match_type']}"
                )

                print()


# ============================================================
# TEST 4
# WORKER -> JOBS
# ============================================================

print(
    "\n=============================="
)

print(
    "TEST 4: JOBS FOR A WORKER"
)

print(
    "=============================="
)


worker_engine.refresh_data()

if worker_engine.WORKERS_DF.empty:

    print(
        "\nNo workers found."
    )

else:

    # Find a worker with at least one skill.
    selected_worker = None

    for _, candidate_worker in (
        worker_engine.WORKERS_DF.iterrows()
    ):

        candidate_id = str(
            candidate_worker["id"]
        )

        candidate_skills = (
            worker_engine.WORKER_SKILL_MAP.get(
                candidate_id,
                set()
            )
        )

        if candidate_skills:

            selected_worker = candidate_worker
            break

    if selected_worker is None:

        print(
            "\nNo worker with skills found."
        )

    else:

        worker_id = str(
            selected_worker["id"]
        )

        print(
            f"\nWorker Selected: {worker_id}"
        )

        worker_skill_ids = (
            worker_engine.WORKER_SKILL_MAP.get(
                worker_id,
                set()
            )
        )

        print()

        print_skills(
            "Worker Skills:",
            worker_skill_ids
        )

        jobs = (
            worker_engine.recommend_jobs_for_worker(
                worker_id,
                top_n=5
            )
        )

        print(
            "\nRecommended Jobs:\n"
        )

        if not jobs:

            print(
                "No jobs matched the "
                "current skill/similarity/"
                "distance filters."
            )

        else:

            validate_worker_results(
                jobs
            )

            assert_descending(
                jobs
            )

            for i, job in enumerate(
                jobs,
                1
            ):

                job_id = str(
                    job["job_id"]
                )

                job_skill_ids = (
                    worker_engine.JOB_SKILL_MAP.get(
                        job_id,
                        set()
                    )
                )

                print(
                    f"{i}. {job['title']}"
                )

                print(
                    "   Required Skills:",
                    (
                        ", ".join(
                            skill_names(
                                job_skill_ids
                            )
                        )
                        if job_skill_ids
                        else
                        "No skills found"
                    )
                )

                print(
                    f"   Distance: "
                    f"{float(job['distance_km']):.2f} km"
                )

                print(
                    f"   Proximity Score: "
                    f"{float(job['proximity_score']):.3f}"
                )

                print(
                    f"   Embedding Similarity: "
                    f"{float(job['similarity']):.3f}"
                )

                print(
                    f"   Skill Similarity: "
                    f"{float(job['skill_similarity']):.3f}"
                )

                print(
                    f"   ML Score: "
                    f"{float(job['ml_score']):.3f}"
                )

                print(
                    f"   Final Score: "
                    f"{float(job['final_score']):.3f}"
                )

                print(
                    f"   Match Type: "
                    f"{job['match_type']}"
                )

                print()


# ============================================================
# TEST 5
# TOP-N VALIDATION
# ============================================================

print(
    "\n=============================="
)

print(
    "TEST 5: TOP-N VALIDATION"
)

print(
    "=============================="
)


if not job_engine.JOBS_DF.empty:

    selected_job_id = None

    for _, candidate_job in (
        job_engine.JOBS_DF.iterrows()
    ):

        candidate_id = str(
            candidate_job["id"]
        )

        if job_engine.JOB_SKILL_MAP.get(
            candidate_id,
            set()
        ):

            selected_job_id = candidate_id
            break

    if selected_job_id:

        workers = (
            job_engine.recommend_workers_for_job(
                selected_job_id,
                top_n=3
            )
        )

        assert len(workers) <= 3

        print(
            f"Job -> Worker top_n=3: "
            f"{len(workers)} results PASS"
        )


if not worker_engine.WORKERS_DF.empty:

    selected_worker_id = None

    for _, candidate_worker in (
        worker_engine.WORKERS_DF.iterrows()
    ):

        candidate_id = str(
            candidate_worker["id"]
        )

        if worker_engine.WORKER_SKILL_MAP.get(
            candidate_id,
            set()
        ):

            selected_worker_id = candidate_id
            break

    if selected_worker_id:

        jobs = (
            worker_engine.recommend_jobs_for_worker(
                selected_worker_id,
                top_n=3
            )
        )

        assert len(jobs) <= 3

        print(
            f"Worker -> Job top_n=3: "
            f"{len(jobs)} results PASS"
        )


# ============================================================
# FINAL RESULT
# ============================================================

print(
    "\n=============================="
)

print(
    "ALL AUTOMATED VALIDATIONS PASSED"
)

print(
    "=============================="
)

print(
    "\nRanking priorities:"
)

print(
    "Job -> Worker:"
)

print(
    "  Skill similarity = 40%"
)

print(
    "  Proximity        = 25%"
)

print(
    "  Worker rating    = 20%"
)

print(
    "  Semantic match   = 10%"
)

print(
    "  ML score         = 5%"
)

print(
    "\nWorker -> Job:"
)

print(
    "  Uses the existing "
    "skill/proximity/semantic/ML ranking."
)

print(
    "\nZero-skill-overlap and semantic-only "
    "recommendations are rejected."
)