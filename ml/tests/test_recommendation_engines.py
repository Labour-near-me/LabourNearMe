
"""Offline recommendation-engine characterization tests.

The engines use synthetic in-memory data. refresh_data is replaced per test,
and model inference is stubbed so tests do not need live database data or
download transformer models.
"""

import os

os.environ["DATABASE_URL"] = "sqlite://"

import numpy as np
import pandas as pd
import pytest

from ml.engines import jobForWorkers_RE as job_engine
from ml.engines import skill_taxonomy
from ml.engines import workerForJob_RE as worker_engine


FEATURES = [
    "skill_similarity",
    "experience_bucket",
    "avg_rating",
    "distance_km",
    "budget",
    "worker_cluster",
]


class ConstantModel:
    def __init__(self):
        self.last_input = None

    def predict(self, frame):
        self.last_input = frame.copy()
        return np.zeros(len(frame))


class ConstantClusterModel:
    def predict(self, vectors):
        return np.zeros(len(vectors), dtype=int)


def vector(value=1.0):
    result = np.zeros(384, dtype=float)
    result[0] = value
    return result.tolist()


def worker(worker_id="worker-1", *, rating=4.0, lat=0.0, lng=0.0):
    return {
        "id": worker_id,
        "experience_years": 3,
        "rating": rating,
        "location_lat": lat,
        "location_lng": lng,
    }


def job(
    job_id="job-1",
    *,
    title="Plumbing",
    budget=500.0,
    lat=0.0,
    lng=0.0,
    status="open",
):
    return {
        "id": job_id,
        "title": title,
        "budget": budget,
        "location_lat": lat,
        "location_lng": lng,
        "status": status,
    }


@pytest.fixture
def isolated_engines(monkeypatch):
    """Stub external model/data refresh while preserving real skill rules."""
    models = {}

    for name, engine in (
        ("worker_to_jobs", worker_engine),
        ("job_to_workers", job_engine),
    ):
        model = ConstantModel()
        monkeypatch.setattr(engine, "refresh_data", lambda: None)
        monkeypatch.setattr(engine, "MODEL", model)
        monkeypatch.setattr(engine, "FEATURE_COLUMNS", FEATURES)
        monkeypatch.setattr(engine, "KMEANS_MODEL", ConstantClusterModel())
        models[name] = model

    return models


def install_data(
    monkeypatch,
    *,
    workers,
    jobs,
    worker_skills=None,
    job_skills=None,
    worker_embeddings=None,
    job_embeddings=None,
):
    worker_columns = [
        "id",
        "experience_years",
        "rating",
        "location_lat",
        "location_lng",
        "worker_embedding",
    ]
    job_columns = [
        "id",
        "title",
        "budget",
        "location_lat",
        "location_lng",
        "status",
        "job_embedding",
    ]

    worker_frame = pd.DataFrame(workers, columns=worker_columns[:-1])
    job_frame = pd.DataFrame(jobs, columns=job_columns[:-1])

    if worker_embeddings is None:
        worker_embeddings = [vector() for _ in workers]
    if job_embeddings is None:
        job_embeddings = [vector() for _ in jobs]

    worker_frame["worker_embedding"] = worker_embeddings
    job_frame["job_embedding"] = job_embeddings

    worker_skills = worker_skills or {}
    job_skills = job_skills or {}

    for engine in (worker_engine, job_engine):
        monkeypatch.setattr(engine, "WORKERS_DF", worker_frame.copy())
        monkeypatch.setattr(engine, "JOBS_DF", job_frame.copy())
        monkeypatch.setattr(
            engine,
            "WORKER_VEC",
            engine.convert_embeddings(worker_frame, "worker_embedding"),
        )
        monkeypatch.setattr(
            engine,
            "JOB_VEC",
            engine.convert_embeddings(job_frame, "job_embedding"),
        )
        monkeypatch.setattr(engine, "WORKER_SKILL_MAP", worker_skills)
        monkeypatch.setattr(engine, "JOB_SKILL_MAP", job_skills)


def test_empty_job_candidates_return_empty_list(isolated_engines, monkeypatch):
    install_data(
        monkeypatch,
        workers=[worker()],
        jobs=[],
        worker_skills={"worker-1": {"plumber"}},
    )

    assert worker_engine.recommend_jobs_for_worker("worker-1") == []


def test_empty_worker_candidates_return_empty_list(isolated_engines, monkeypatch):
    install_data(
        monkeypatch,
        workers=[],
        jobs=[job()],
        job_skills={"job-1": {"plumber"}},
    )

    assert job_engine.recommend_workers_for_job("job-1") == []


@pytest.mark.parametrize("direction", ["worker_to_jobs", "job_to_workers"])
def test_exact_skill_match_is_recommended(
    direction, isolated_engines, monkeypatch
):
    install_data(
        monkeypatch,
        workers=[worker()],
        jobs=[job()],
        worker_skills={"worker-1": {"Plumber"}},
        job_skills={"job-1": {"plumber"}},
    )

    if direction == "worker_to_jobs":
        results = worker_engine.recommend_jobs_for_worker("worker-1")
        assert [item["job_id"] for item in results] == ["job-1"]
    else:
        results = job_engine.recommend_workers_for_job("job-1")
        assert [item["worker_id"] for item in results] == ["worker-1"]


@pytest.mark.parametrize("direction", ["worker_to_jobs", "job_to_workers"])
def test_partial_skill_overlap_is_scored_by_fraction(
    direction, isolated_engines, monkeypatch
):
    install_data(
        monkeypatch,
        workers=[worker()],
        jobs=[job()],
        worker_skills={"worker-1": {"plumber"}},
        job_skills={"job-1": {"plumber", "tiling"}},
    )

    if direction == "worker_to_jobs":
        results = worker_engine.recommend_jobs_for_worker("worker-1")
    else:
        results = job_engine.recommend_workers_for_job("job-1")

    assert len(results) == 1
    assert results[0]["skill_similarity"] == 0.5


@pytest.mark.parametrize("direction", ["worker_to_jobs", "job_to_workers"])
def test_electrician_does_not_match_plumber_with_low_semantic_score(
    direction, isolated_engines, monkeypatch
):
    install_data(
        monkeypatch,
        workers=[worker()],
        jobs=[job()],
        worker_skills={"worker-1": {"electrician"}},
        job_skills={"job-1": {"plumber"}},
    )

    assert not skill_taxonomy.skills_match("electrician", "plumber")

    if direction == "worker_to_jobs":
        assert worker_engine.recommend_jobs_for_worker("worker-1") == []
    else:
        assert job_engine.recommend_workers_for_job("job-1") == []


@pytest.mark.parametrize("direction", ["worker_to_jobs", "job_to_workers"])
def test_exactly_50_km_is_included_but_just_over_is_excluded(
    direction, isolated_engines, monkeypatch
):
    if direction == "worker_to_jobs":
        install_data(
            monkeypatch,
            workers=[worker()],
            jobs=[
                job("at-limit", lng=50.0),
                job("over-limit", lng=50.001),
            ],
            worker_skills={"worker-1": {"plumber"}},
            job_skills={
                "at-limit": {"plumber"},
                "over-limit": {"plumber"},
            },
        )
        monkeypatch.setattr(
            worker_engine, "haversine", lambda _a, _b, _c, lng: lng
        )
        results = worker_engine.recommend_jobs_for_worker(
            "worker-1", top_n=10
        )
        assert [item["job_id"] for item in results] == ["at-limit"]
        assert results[0]["distance_km"] == 50.0
    else:
        install_data(
            monkeypatch,
            workers=[
                worker("at-limit", lng=50.0),
                worker("over-limit", lng=50.001),
            ],
            jobs=[job()],
            worker_skills={
                "at-limit": {"plumber"},
                "over-limit": {"plumber"},
            },
            job_skills={"job-1": {"plumber"}},
        )
        monkeypatch.setattr(
            job_engine, "haversine", lambda _a, _b, _c, lng: lng
        )
        results = job_engine.recommend_workers_for_job("job-1", top_n=10)
        assert [item["worker_id"] for item in results] == ["at-limit"]
        assert results[0]["distance_km"] == 50.0


@pytest.mark.parametrize(
    ("direction", "missing_side"),
    [
        ("worker_to_jobs", "worker"),
        ("worker_to_jobs", "job"),
        ("job_to_workers", "worker"),
        ("job_to_workers", "job"),
    ],
)
def test_missing_embeddings_are_zero_vectors_and_excluded(
    direction, missing_side, isolated_engines, monkeypatch
):
    install_data(
        monkeypatch,
        workers=[worker()],
        jobs=[job()],
        worker_skills={"worker-1": {"plumber"}},
        job_skills={"job-1": {"plumber"}},
        worker_embeddings=[None] if missing_side == "worker" else None,
        job_embeddings=[None] if missing_side == "job" else None,
    )

    if direction == "worker_to_jobs":
        assert worker_engine.recommend_jobs_for_worker("worker-1") == []
    else:
        assert job_engine.recommend_workers_for_job("job-1") == []


@pytest.mark.parametrize(
    ("direction", "missing_side"),
    [
        ("worker_to_jobs", "worker"),
        ("worker_to_jobs", "job"),
        ("job_to_workers", "worker"),
        ("job_to_workers", "job"),
    ],
)
def test_missing_coordinates_exclude_candidate(
    direction, missing_side, isolated_engines, monkeypatch
):
    workers = [
        worker(lat=None if missing_side == "worker" else 0.0)
    ]
    jobs = [
        job(lat=None if missing_side == "job" else 0.0)
    ]

    install_data(
        monkeypatch,
        workers=workers,
        jobs=jobs,
        worker_skills={"worker-1": {"plumber"}},
        job_skills={"job-1": {"plumber"}},
    )

    if direction == "worker_to_jobs":
        assert worker_engine.recommend_jobs_for_worker("worker-1") == []
    else:
        assert job_engine.recommend_workers_for_job("job-1") == []


@pytest.mark.parametrize(
    ("direction", "malformed_side"),
    [
        ("worker_to_jobs", "worker"),
        ("worker_to_jobs", "job"),
        ("job_to_workers", "worker"),
        ("job_to_workers", "job"),
    ],
)
def test_malformed_embedding_dimensions_are_skipped_safely(
    direction, malformed_side, isolated_engines, monkeypatch
):
    install_data(
        monkeypatch,
        workers=[worker()],
        jobs=[job()],
        worker_skills={"worker-1": {"plumber"}},
        job_skills={"job-1": {"plumber"}},
        worker_embeddings=(
            [[1.0, 0.0, 0.0]] if malformed_side == "worker" else None
        ),
        job_embeddings=(
            [[1.0, 0.0, 0.0]] if malformed_side == "job" else None
        ),
    )

    if direction == "worker_to_jobs":
        assert worker_engine.recommend_jobs_for_worker("worker-1") == []
    else:
        assert job_engine.recommend_workers_for_job("job-1") == []


@pytest.mark.parametrize("direction", ["worker_to_jobs", "job_to_workers"])
def test_malformed_candidate_is_skipped_without_shifting_candidate_alignment(
    direction, isolated_engines, monkeypatch
):
    if direction == "worker_to_jobs":
        workers = [worker()]
        jobs = [job("malformed"), job("valid")]
        worker_embeddings = None
        job_embeddings = [[1.0, 0.0, 0.0], vector()]
        worker_skills = {"worker-1": {"plumber"}}
        job_skills = {
            "malformed": {"plumber"},
            "valid": {"plumber"},
        }
    else:
        workers = [worker("malformed"), worker("valid")]
        jobs = [job()]
        worker_embeddings = [[1.0, 0.0, 0.0], vector()]
        job_embeddings = None
        worker_skills = {
            "malformed": {"plumber"},
            "valid": {"plumber"},
        }
        job_skills = {"job-1": {"plumber"}}

    install_data(
        monkeypatch,
        workers=workers,
        jobs=jobs,
        worker_skills=worker_skills,
        job_skills=job_skills,
        worker_embeddings=worker_embeddings,
        job_embeddings=job_embeddings,
    )

    if direction == "worker_to_jobs":
        results = worker_engine.recommend_jobs_for_worker(
            "worker-1", top_n=10
        )
        assert [item["job_id"] for item in results] == ["valid"]
    else:
        results = job_engine.recommend_workers_for_job("job-1", top_n=10)
        assert [item["worker_id"] for item in results] == ["valid"]


@pytest.mark.parametrize("direction", ["worker_to_jobs", "job_to_workers"])
def test_null_rating_and_budget_use_zero_defaults(
    direction, isolated_engines, monkeypatch
):
    install_data(
        monkeypatch,
        workers=[worker(rating=None)],
        jobs=[job(budget=None)],
        worker_skills={"worker-1": {"plumber"}},
        job_skills={"job-1": {"plumber"}},
    )

    if direction == "worker_to_jobs":
        results = worker_engine.recommend_jobs_for_worker("worker-1")
        model = isolated_engines["worker_to_jobs"]
        assert len(results) == 1
        assert model.last_input.loc[0, "avg_rating"] == 0
        assert model.last_input.loc[0, "budget"] == 0
    else:
        results = job_engine.recommend_workers_for_job("job-1")
        model = isolated_engines["job_to_workers"]
        assert len(results) == 1
        assert results[0]["rating"] == 0
        assert results[0]["rating_score"] == 0
        assert model.last_input.loc[0, "avg_rating"] == 0
        assert model.last_input.loc[0, "budget"] == 0


def test_worker_to_jobs_are_sorted_and_have_expected_output_fields(
    isolated_engines, monkeypatch
):
    install_data(
        monkeypatch,
        workers=[worker()],
        jobs=[job("near", lat=0.0), job("far", lat=0.2)],
        worker_skills={"worker-1": {"plumber"}},
        job_skills={
            "near": {"plumber"},
            "far": {"plumber"},
        },
    )

    results = worker_engine.recommend_jobs_for_worker("worker-1")

    assert [item["job_id"] for item in results] == ["near", "far"]
    assert all(0 <= item["final_score"] <= 1 for item in results)
    assert set(results[0]) == {
        "job_id",
        "title",
        "final_score",
        "ml_score",
        "similarity",
        "skill_similarity",
        "distance_km",
        "proximity_score",
        "budget",
        "match_type",
    }


def test_job_to_workers_are_sorted_and_have_expected_output_fields(
    isolated_engines, monkeypatch
):
    install_data(
        monkeypatch,
        workers=[
            worker("lower-rated", rating=1.0),
            worker("higher-rated", rating=5.0),
        ],
        jobs=[job()],
        worker_skills={
            "lower-rated": {"plumber"},
            "higher-rated": {"plumber"},
        },
        job_skills={"job-1": {"plumber"}},
    )

    results = job_engine.recommend_workers_for_job("job-1")

    assert [item["worker_id"] for item in results] == [
        "higher-rated",
        "lower-rated",
    ]
    assert all(0 <= item["final_score"] <= 1 for item in results)
    assert set(results[0]) == {
        "worker_id",
        "final_score",
        "ml_score",
        "similarity",
        "skill_similarity",
        "distance_km",
        "proximity_score",
        "rating",
        "rating_score",
        "match_type",
    }


@pytest.mark.parametrize("engine", [worker_engine, job_engine])
def test_database_loader_filters_closed_jobs_without_live_database(
    engine, monkeypatch
):
    queries = []

    def fake_read_sql(query, _connection):
        query_text = str(query)
        queries.append(query_text)

        if "FROM workers" in query_text:
            return pd.DataFrame([worker()])

        return pd.DataFrame([job("open-job", status="open")])

    monkeypatch.setattr(engine.pd, "read_sql", fake_read_sql)
    _workers, jobs = engine.load_data()

    assert len(queries) == 2
    assert "WHERE status = 'open'" in queries[1]
    assert jobs["id"].tolist() == ["open-job"]


def test_closed_job_id_is_not_recommended(isolated_engines, monkeypatch):
    install_data(
        monkeypatch,
        workers=[worker()],
        jobs=[job("open-job")],
        worker_skills={"worker-1": {"plumber"}},
        job_skills={"open-job": {"plumber"}},
    )

    assert job_engine.recommend_workers_for_job("closed-job") == []


def test_unavailable_worker_is_not_recommended_for_job(
    isolated_engines, monkeypatch
):
    install_data(
        monkeypatch,
        workers=[
            worker("available"),
            worker("unavailable"),
            worker("unknown-status"),
        ],
        jobs=[job()],
        worker_skills={
            "available": {"plumber"},
            "unavailable": {"plumber"},
            "unknown-status": {"plumber"},
        },
        job_skills={"job-1": {"plumber"}},
    )

    # install_data has no availability column, so add it for this test only.
    job_engine.WORKERS_DF["availability_status"] = [True, False, None]

    results = job_engine.recommend_workers_for_job("job-1", top_n=10)
    recommended = {item["worker_id"] for item in results}

    assert "unavailable" not in recommended
    assert recommended == {"available", "unknown-status"}
