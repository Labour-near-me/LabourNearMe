"""Isolated route tests backed by an in-memory Supabase-shaped fake.

These tests replace the Supabase client module before importing the FastAPI
application. They exercise route/dependency behavior, not Supabase or SQL RPC
integration behavior.
"""

import json
import sys
import types
import unittest
from types import SimpleNamespace
from unittest.mock import patch


class FakeResponse:
    def __init__(self, data=None, count=None):
        self.data = data if data is not None else []
        self.count = count


class FakeAuth:
    def __init__(self):
        self.users = {}

    def get_user(self, token):
        if token not in self.users:
            raise ValueError("invalid test token")
        return SimpleNamespace(user=self.users[token])


class FakeQuery:
    def __init__(self, client, table):
        self.client = client
        self.table_name = table
        self.action = "select"
        self.payload = None
        self.filters = []
        self.limit_value = None
        self.order_column = None
        self.order_desc = False
        self.single_result = False
        self.count_requested = False

    def select(self, _columns="*", count=None):
        self.count_requested = count == "exact"
        return self

    def eq(self, key, value):
        self.filters.append(("eq", key, value))
        return self

    def in_(self, key, values):
        self.filters.append(("in", key, values))
        return self

    def ilike(self, key, value):
        self.filters.append(("ilike", key, value))
        return self

    def limit(self, value):
        self.limit_value = value
        return self

    def order(self, column, desc=False, **kwargs):
        self.order_column = column
        self.order_desc = desc
        return self

    def single(self):
        self.single_result = True
        return self

    def insert(self, payload):
        self.action = "insert"
        self.payload = payload
        return self

    def update(self, payload):
        self.action = "update"
        self.payload = payload
        return self

    def execute(self):
        return self.client.execute_query(self)


class FakeRpc:
    def __init__(self, client, name, params):
        self.client = client
        self.name = name
        self.params = params

    def execute(self):
        self.client.rpc_calls.append((self.name, self.params))

        if self.client.fail_rpc == self.name:
            raise RuntimeError("simulated RPC failure")

        if self.name == "register_worker_atomic":
            return self._register_worker()

        if self.name == "register_employer_atomic":
            return self._register_employer()

        if self.name == "create_job_atomic":
            return self._create_job()

        if self.name == "hire_application_for_job":
            app_id = self.params["p_application_id"]
            application = next(
                (
                    row for row in self.client.tables["applications"]
                    if row["id"] == app_id
                ),
                None,
            )
            if application is None:
                return FakeResponse([])
            application["status"] = "hired"
            return FakeResponse([application.copy()])

        if self.name == "complete_and_rate_job":
            rating = {
                "id": "rating-1",
                "job_id": self.params["p_job_id"],
                "reviewer_id": self.params["p_employer_id"],
                "reviewee_id": self.params["p_worker_id"],
                "rating_value": self.params["p_rating_value"],
                "feedback": self.params["p_feedback"],
            }
            self.client.tables["ratings"].append(rating)

            for job in self.client.tables["Jobs"]:
                if job["id"] == self.params["p_job_id"]:
                    job["status"] = "completed"

            return FakeResponse(rating)

        raise AssertionError(f"Unexpected RPC: {self.name}")

    @staticmethod
    def _as_list(value):
        if value is None:
            return []
        if isinstance(value, str):
            value = json.loads(value)
        if not isinstance(value, list):
            raise ValueError("Expected a list for JSONB RPC parameter")
        return value

    def _next_id(self):
        value = f"record-{self.client.next_id}"
        self.client.next_id += 1
        return value

    def _get_or_create_skills(self, skill_items):
        result = []

        for item in skill_items:
            if isinstance(item, str):
                skill_name = item.strip()
                supplied_id = None
            elif isinstance(item, dict):
                skill_name = str(item.get("skill_name") or "").strip()
                supplied_id = item.get("id")
            else:
                raise ValueError("Invalid skill item")

            if supplied_id:
                existing = next(
                    (
                        row for row in self.client.tables["Skill_master"]
                        if str(row["id"]) == str(supplied_id)
                    ),
                    None,
                )
                if existing is None:
                    raise ValueError("Unknown skill ID")
                result.append(existing)
                continue

            if not skill_name:
                raise ValueError("Skill name cannot be empty")

            existing = next(
                (
                    row for row in self.client.tables["Skill_master"]
                    if row["skill_name"].casefold() == skill_name.casefold()
                ),
                None,
            )

            if existing is None:
                existing = {
                    "id": self._next_id(),
                    "skill_name": skill_name,
                }
                self.client.tables["Skill_master"].append(existing)

            result.append(existing)

        return result

    def _register_worker(self):
        p = self.params
        auth_id = str(p["p_auth_user_id"])

        if any(
            str(row.get("auth_user_id")) == auth_id
            for row in self.client.tables["Profiles"]
        ):
            raise RuntimeError("23505 profiles_auth_user_id_unique")

        # Stage changes first; publish them only when the operation succeeds.
        profile_id = self._next_id()
        worker_id = profile_id

        profile = {
            "id": profile_id,
            "auth_user_id": auth_id,
            "full_name": p.get("p_full_name"),
            "phone": p.get("p_phone"),
            "role": "worker",
        }

        worker = {
            "id": worker_id,
            "experience_years": p.get("p_experience_years"),
            "expected_wage": p.get("p_expected_wage"),
            "location_lat": p.get("p_location_lat"),
            "location_lng": p.get("p_location_lng"),
            "worker_embedding": [0.0] * 384,
        }

        # Simulate a transactional failure BEFORE creating any skill rows.
        if self.client.fail_on == ("Worker_skills", "insert"):
            raise RuntimeError("simulated database write failure")

        skill_items = self._as_list(p.get("p_skills"))
        skills = self._get_or_create_skills(skill_items)

        worker_links = [
            {
                "worker_id": worker_id,
                "skill_id": skill["id"],
            }
            for skill in skills
        ]

        self.client.tables["Profiles"].append(profile)
        self.client.tables["workers"].append(worker)
        self.client.tables["Worker_skills"].extend(worker_links)

        return FakeResponse({"worker_id": worker_id})

    def _register_employer(self):
        p = self.params
        auth_id = str(p["p_auth_user_id"])

        if any(
            str(row.get("auth_user_id")) == auth_id
            for row in self.client.tables["Profiles"]
        ):
            raise RuntimeError("23505 profiles_auth_user_id_unique")

        profile_id = self._next_id()

        profile = {
            "id": profile_id,
            "auth_user_id": auth_id,
            "full_name": p.get("p_full_name"),
            "phone": p.get("p_phone"),
            "role": "employer",
        }

        employer = {
            "id": profile_id,
            "employer_name": p.get("p_employer_name"),
            "description": p.get("p_description"),
            "location_lat": p.get("p_location_lat"),
            "location_lng": p.get("p_location_lng"),
        }

        if self.client.fail_on == ("Employers", "insert"):
            raise RuntimeError("simulated database write failure")

        self.client.tables["Profiles"].append(profile)
        self.client.tables["Employers"].append(employer)

        return FakeResponse({"employer_id": profile_id})

    def _create_job(self):
        p = self.params
        employer_id = str(p["p_employer_id"])

        profile = next(
            (
                row for row in self.client.tables["Profiles"]
                if str(row.get("id")) == employer_id
                and row.get("role") == "employer"
            ),
            None,
        )
        if profile is None:
            raise RuntimeError("Employer profile not found")

        employer = next(
            (
                row for row in self.client.tables["Employers"]
                if str(row.get("id")) == employer_id
            ),
            None,
        )
        if employer is None:
            raise RuntimeError("Employer record not found")

        job_id = self._next_id()
        job = {
            "id": job_id,
            "employer_id": employer_id,
            "title": p.get("p_title"),
            "description": p.get("p_description"),
            "location_text": p.get("p_location_text"),
            "location_lat": p.get("p_location_lat"),
            "location_lng": p.get("p_location_lng"),
            "budget": p.get("p_budget"),
            "status": "open",
            "job_embedding": [0.0] * 384,
        }

        # Simulate failure before creating any skill rows.
        if self.client.fail_on == ("Job_required_skill", "insert"):
            raise RuntimeError("simulated database write failure")

        skill_items = self._as_list(p.get("p_required_skills"))
        skills = self._get_or_create_skills(skill_items)

        links = [
            {"job_id": job_id, "skill_id": skill["id"]}
            for skill in skills
        ]

        self.client.tables["Jobs"].append(job)
        self.client.tables["Job_required_skill"].extend(links)

        return FakeResponse({"job_id": job_id})


class FakeSupabase:
    TABLES = (
        "Profiles", "workers", "Employers", "Jobs", "Skill_master",
        "Worker_skills", "Job_required_skill", "applications", "ratings",
    )

    def __init__(self):
        self.auth = FakeAuth()
        self.reset()

    def reset(self):
        self.tables = {name: [] for name in self.TABLES}
        self.next_id = 1
        self.fail_on = None
        self.fail_rpc = None
        self.rpc_calls = []
        self.query_calls = []

    def table(self, name):
        if name not in self.tables:
            self.tables[name] = []
        return FakeQuery(self, name)

    def rpc(self, name, params):
        return FakeRpc(self, name, params)

    def execute_query(self, query):
        self.query_calls.append((query.table_name, query.action))

        if self.fail_on == (query.table_name, query.action):
            raise RuntimeError("simulated database write failure")

        rows = self.tables[query.table_name]

        if query.action == "insert":
            payloads = (
                query.payload
                if isinstance(query.payload, list)
                else [query.payload]
            )
            inserted = []

            for payload in payloads:
                row = dict(payload)
                if "id" not in row:
                    row["id"] = f"record-{self.next_id}"
                    self.next_id += 1
                rows.append(row)
                inserted.append(row.copy())

            return FakeResponse(inserted)

        selected = [
            row for row in rows
            if self._matches(row, query.filters)
        ]

        if query.order_column:
            selected.sort(
                key=lambda row: (
                    row.get(query.order_column) is None,
                    row.get(query.order_column),
                ),
                reverse=query.order_desc,
            )

        if query.limit_value is not None:
            selected = selected[:query.limit_value]

        if query.action == "update":
            for row in selected:
                row.update(query.payload)
            return FakeResponse([row.copy() for row in selected])

        if query.single_result:
            return FakeResponse(selected[0].copy() if selected else None)

        return FakeResponse(
            [row.copy() for row in selected],
            count=len(selected),
        )

    @staticmethod
    def _matches(row, filters):
        for kind, key, expected in filters:
            actual = row.get(key)

            if kind == "eq" and str(actual) != str(expected):
                return False

            if kind == "in" and actual not in expected:
                return False

            if kind == "ilike" and str(actual).casefold() != str(expected).casefold():
                return False

        return True


# Install a fake database module before importing application code.
fake_supabase = FakeSupabase()
supabase_module = types.ModuleType("backend.database.supabase_client")
supabase_module.supabase = fake_supabase
sys.modules["backend.database.supabase_client"] = supabase_module

from fastapi.testclient import TestClient  # noqa: E402

import backend.app as app_module  # noqa: E402
from backend.services import application_service, job_service, worker_service  # noqa: E402
from backend.services.recommendation_service import RecommendationService  # noqa: E402


class BackendWorkflowTests(unittest.TestCase):
    def setUp(self):
        fake_supabase.reset()
        fake_supabase.auth.users = {
            "worker-token": SimpleNamespace(
                id="auth-worker", email="worker@example.test"
            ),
            "employer-token": SimpleNamespace(
                id="auth-employer", email="employer@example.test"
            ),
            "other-employer-token": SimpleNamespace(
                id="auth-other", email="other@example.test"
            ),
            "unregistered-token": SimpleNamespace(
                id="auth-new", email="new@example.test"
            ),
        }
        self.client = TestClient(app_module.app)

    @staticmethod
    def headers(token):
        return {"Authorization": f"Bearer {token}"}

    def seed_profile(self, profile_id, auth_id, role):
        fake_supabase.tables["Profiles"].append({
            "id": profile_id,
            "auth_user_id": auth_id,
            "role": role,
            "full_name": profile_id,
            "phone": "0000000000",
        })

        if role == "employer":
            fake_supabase.tables["Employers"].append({
                "id": profile_id,
                "employer_name": profile_id,
            })

    def seed_job(self, job_id="job-1", employer_id="employer-1", status="open"):
        fake_supabase.tables["Jobs"].append({
            "id": job_id,
            "employer_id": employer_id,
            "status": status,
            "title": "Synthetic job",
            "description": "Synthetic description",
            "location_lat": 0.0,
            "location_lng": 0.0,
        })

    def seed_worker(self, worker_id="worker-1"):
        fake_supabase.tables["workers"].append({"id": worker_id})

    def seed_application(
        self, app_id="app-1", job_id="job-1",
        worker_id="worker-1", status="pending",
    ):
        fake_supabase.tables["applications"].append({
            "id": app_id,
            "job_id": job_id,
            "worker_id": worker_id,
            "status": status,
        })

    def authenticated_profiles(self):
        self.seed_profile("worker-1", "auth-worker", "worker")
        self.seed_profile("employer-1", "auth-employer", "employer")
        self.seed_profile("employer-2", "auth-other", "employer")


class AuthenticationTests(BackendWorkflowTests):
    def test_missing_and_invalid_tokens_are_rejected(self):
        self.assertEqual(self.client.get("/auth/me").status_code, 401)
        response = self.client.get(
            "/auth/me", headers=self.headers("bad-token")
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.json()["detail"],
            "The sign-in token is invalid or expired",
        )

    def test_authenticated_user_without_profile_gets_registration_state(self):
        response = self.client.get(
            "/auth/me", headers=self.headers("unregistered-token")
        )
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.json()["profile"])
        self.assertTrue(response.json()["needs_registration"])

    def test_missing_profile_and_wrong_role_are_forbidden(self):
        no_profile = self.client.post(
            "/applications/apply",
            json={"job_id": "job-1"},
            headers=self.headers("unregistered-token"),
        )
        self.assertEqual(no_profile.status_code, 403)

        self.seed_profile("employer-1", "auth-employer", "employer")
        wrong_role = self.client.post(
            "/applications/apply",
            json={"job_id": "job-1"},
            headers=self.headers("employer-token"),
        )
        self.assertEqual(wrong_role.status_code, 403)


class ApplicationTests(BackendWorkflowTests):
    def setUp(self):
        super().setUp()
        self.authenticated_profiles()
        self.seed_job()

    def test_open_job_application_uses_authenticated_worker_identity(self):
        response = self.client.post(
            "/applications/apply",
            json={"job_id": "job-1", "worker_id": "attacker-chosen-id"},
            headers=self.headers("worker-token"),
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(fake_supabase.tables["applications"], [])

        response = self.client.post(
            "/applications/apply",
            json={"job_id": "job-1"},
            headers=self.headers("worker-token"),
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["application"]["worker_id"], "worker-1")

    def test_closed_missing_and_duplicate_job_applications(self):
        self.seed_job("closed-job", status="closed")

        closed = self.client.post(
            "/applications/apply",
            json={"job_id": "closed-job"},
            headers=self.headers("worker-token"),
        )
        missing = self.client.post(
            "/applications/apply",
            json={"job_id": "missing"},
            headers=self.headers("worker-token"),
        )

        self.assertEqual(closed.status_code, 400)
        self.assertEqual(missing.status_code, 404)

        self.seed_application()
        duplicate = self.client.post(
            "/applications/apply",
            json={"job_id": "job-1"},
            headers=self.headers("worker-token"),
        )
        self.assertEqual(duplicate.status_code, 409)

    def test_application_database_failure_returns_generic_error(self):
        fake_supabase.fail_on = ("Jobs", "select")
        response = self.client.post(
            "/applications/apply",
            json={"job_id": "job-1"},
            headers=self.headers("worker-token"),
        )
        self.assertEqual(response.status_code, 500)
        self.assertEqual(
            response.json()["detail"], "Application could not be submitted"
        )
        self.assertNotIn("simulated database write failure", response.text)

    def test_status_update_database_failure_returns_generic_error(self):
        fake_supabase.fail_on = ("applications", "select")
        response = self.client.post(
            "/applications/status-update",
            json={"application_id": "app-1", "new_status": "hired"},
            headers=self.headers("employer-token"),
        )
        self.assertEqual(response.status_code, 500)
        self.assertEqual(
            response.json()["detail"], "Application status could not be updated"
        )

    def test_application_history_database_failure_returns_generic_error(self):
        fake_supabase.fail_on = ("applications", "select")
        response = self.client.get(
            "/applications/my-applications/worker-1",
            headers=self.headers("worker-token"),
        )
        self.assertEqual(response.status_code, 500)
        self.assertEqual(
            response.json()["detail"], "Application history could not be retrieved"
        )

    def test_applicant_list_database_failure_returns_generic_error(self):
        fake_supabase.fail_on = ("applications", "select")
        response = self.client.get(
            "/applications/job/job-1",
            headers=self.headers("employer-token"),
        )
        self.assertEqual(response.status_code, 500)
        self.assertEqual(
            response.json()["detail"], "Applicants could not be retrieved"
        )

    def test_legacy_application_helpers_do_not_return_database_errors(self):
        fake_supabase.fail_on = ("applications", "select")
        apply_result = application_service.apply_job("worker-1", "job-1")
        hire_result = application_service.hire_worker(
            "worker-1", "job-1", "employer-1"
        )

        fake_supabase.fail_on = None
        fake_supabase.fail_rpc = "complete_and_rate_job"
        rating_result = application_service.rate_worker(
            "job-1", "employer-1", "worker-1", 5, "synthetic"
        )

        self.assertEqual(
            apply_result["error"], "Application could not be submitted"
        )
        self.assertEqual(
            hire_result["error"], "Application status could not be updated"
        )
        self.assertEqual(
            rating_result["error"], "Job completion and rating could not be saved"
        )


class WorkerProfileAuthorizationTests(BackendWorkflowTests):
    def setUp(self):
        super().setUp()
        fake_supabase.auth.users["other-worker-token"] = SimpleNamespace(
            id="auth-other-worker",
            email="other-worker@example.test",
        )
        self.seed_profile("worker-1", "auth-worker", "worker")
        self.seed_profile("worker-2", "auth-other-worker", "worker")
        self.seed_profile("employer-1", "auth-employer", "employer")
        self.seed_profile("employer-2", "auth-other", "employer")
        self.seed_job("job-1", "employer-1")
        self.seed_job("job-2", "employer-2")
        self.seed_application(job_id="job-1", worker_id="worker-1")

    def test_phone_is_available_to_worker_and_related_employer_only(self):
        own = self.client.get(
            "/workers/worker-1", headers=self.headers("worker-token")
        )
        related_employer = self.client.get(
            "/workers/worker-1", headers=self.headers("employer-token")
        )
        unrelated_employer = self.client.get(
            "/workers/worker-1", headers=self.headers("other-employer-token")
        )
        unrelated_worker = self.client.get(
            "/workers/worker-1", headers=self.headers("other-worker-token")
        )
        anonymous = self.client.get("/workers/worker-1")

        self.assertEqual(own.status_code, 200)
        self.assertEqual(own.json()["phone"], "0000000000")
        self.assertEqual(related_employer.status_code, 200)
        self.assertEqual(related_employer.json()["phone"], "0000000000")
        self.assertEqual(unrelated_employer.status_code, 403)
        self.assertEqual(unrelated_worker.status_code, 403)
        self.assertEqual(anonymous.status_code, 401)


class PublicJobLocationTests(BackendWorkflowTests):
    def setUp(self):
        super().setUp()
        self.seed_job()
        fake_supabase.tables["Jobs"][0]["created_at"] = (
            "2026-01-01T00:00:00+00:00"
        )
        fake_supabase.tables["Jobs"][0].update({
            "location_lat": 12.34567,
            "location_lng": 77.12345,
            "location_text": "Synthetic exact street address",
        })

    def test_public_job_list_and_detail_return_approximate_coordinates(self):
        listing = self.client.get("/jobs/")
        detail = self.client.get("/jobs/job-1")

        self.assertEqual(listing.status_code, 200)
        self.assertEqual(detail.status_code, 200)

        for job in (listing.json()[0], detail.json()):
            self.assertEqual(job["location_lat"], 12.35)
            self.assertEqual(job["location_lng"], 77.12)
            self.assertNotIn("location_text", job)
            self.assertNotIn("Synthetic exact street address", str(job))


class HiringAndApplicantTests(BackendWorkflowTests):
    def setUp(self):
        super().setUp()
        self.authenticated_profiles()
        self.seed_job()
        self.seed_application()

    def test_foreign_employer_cannot_update_application(self):
        response = self.client.post(
            "/applications/status-update",
            json={"application_id": "app-1", "new_status": "hired"},
            headers=self.headers("other-employer-token"),
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(fake_supabase.rpc_calls, [])

    def test_only_pending_application_can_be_hired_and_hiring_uses_rpc(self):
        response = self.client.post(
            "/applications/status-update",
            json={"application_id": "app-1", "new_status": "hired"},
            headers=self.headers("employer-token"),
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            fake_supabase.rpc_calls[0][0], "hire_application_for_job"
        )

        stale = self.client.post(
            "/applications/status-update",
            json={"application_id": "app-1", "new_status": "rejected"},
            headers=self.headers("employer-token"),
        )
        self.assertEqual(stale.status_code, 409)

    def test_hiring_closed_job_is_rejected_without_rpc(self):
        fake_supabase.tables["Jobs"][0]["status"] = "closed"

        response = self.client.post(
            "/applications/status-update",
            json={"application_id": "app-1", "new_status": "hired"},
            headers=self.headers("employer-token"),
        )

        self.assertEqual(response.status_code, 409)
        self.assertEqual(
            response.json()["detail"], "This job is no longer open for hiring"
        )
        self.assertEqual(fake_supabase.rpc_calls, [])

    def test_rejection_updates_only_pending_application(self):
        response = self.client.post(
            "/applications/status-update",
            json={"application_id": "app-1", "new_status": "rejected"},
            headers=self.headers("employer-token"),
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            fake_supabase.tables["applications"][0]["status"], "rejected"
        )

    def test_applicants_are_visible_only_to_job_owner(self):
        own = self.client.get(
            "/applications/job/job-1",
            headers=self.headers("employer-token"),
        )
        foreign = self.client.get(
            "/applications/job/job-1",
            headers=self.headers("other-employer-token"),
        )

        self.assertEqual(own.status_code, 200)
        self.assertEqual(len(own.json()), 1)
        self.assertEqual(foreign.status_code, 403)


class RecommendationRouteTests(BackendWorkflowTests):
    def setUp(self):
        super().setUp()
        self.authenticated_profiles()
        self.seed_job()

    def test_employer_recommendations_require_job_ownership_and_filter_fields(self):
        internal = [{
            "worker_id": "worker-1",
            "full_name": "Synthetic worker",
            "final_score": 0.8,
            "similarity": 0.9,
            "skill_similarity": 1.0,
            "distance_km": 2.0,
            "rating": 4.5,
            "match_type": "hybrid",
            "ml_score": 0.99,
            "embedding": "private-vector",
        }]

        with patch.object(
            RecommendationService,
            "get_workers_for_job",
            return_value=internal,
        ):
            own = self.client.get(
                "/recommend/workers/job-1",
                headers=self.headers("employer-token"),
            )
            foreign = self.client.get(
                "/recommend/workers/job-1",
                headers=self.headers("other-employer-token"),
            )

        self.assertEqual(own.status_code, 200)
        self.assertNotIn("ml_score", own.json()["recommendations"][0])
        self.assertNotIn("embedding", own.json()["recommendations"][0])
        self.assertEqual(foreign.status_code, 403)

    def test_worker_recommendations_are_limited_to_signed_in_worker(self):
        with patch.object(
            RecommendationService,
            "get_jobs_for_worker",
            return_value=[],
        ):
            own = self.client.get(
                "/recommend/jobs/worker-1",
                headers=self.headers("worker-token"),
            )
            another = self.client.get(
                "/recommend/jobs/someone-else",
                headers=self.headers("worker-token"),
            )

        self.assertEqual(own.status_code, 200)
        self.assertEqual(another.status_code, 403)

    def test_recommendation_failure_returns_generic_response(self):
        with patch.object(
            RecommendationService,
            "get_jobs_for_worker",
            side_effect=RuntimeError("synthetic database detail"),
        ):
            response = self.client.get(
                "/recommend/jobs/worker-1",
                headers=self.headers("worker-token"),
            )

        self.assertEqual(response.status_code, 500)
        self.assertEqual(
            response.json()["detail"],
            "Job recommendations could not be generated",
        )
        self.assertNotIn("synthetic database detail", response.text)


class CompletionAndRatingTests(BackendWorkflowTests):
    def setUp(self):
        super().setUp()
        self.authenticated_profiles()
        self.seed_job(status="closed")
        self.seed_worker()
        self.seed_application(status="hired")

    def payload(self, rating=5, **updates):
        body = {
            "job_id": "job-1",
            "reviewee_id": "worker-1",
            "rating_value": rating,
            "feedback": "Synthetic feedback",
        }
        body.update(updates)
        return body

    def test_wrong_employer_cannot_submit_rating(self):
        response = self.client.post(
            "/feedback/complete-and-rate",
            json=self.payload(),
            headers=self.headers("other-employer-token"),
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(fake_supabase.rpc_calls, [])

    def test_open_job_and_non_hired_worker_cannot_be_rated(self):
        fake_supabase.tables["Jobs"][0]["status"] = "open"
        open_job = self.client.post(
            "/feedback/complete-and-rate",
            json=self.payload(),
            headers=self.headers("employer-token"),
        )
        self.assertEqual(open_job.status_code, 409)

        fake_supabase.tables["Jobs"][0]["status"] = "closed"
        fake_supabase.tables["applications"][0]["status"] = "rejected"
        not_hired = self.client.post(
            "/feedback/complete-and-rate",
            json=self.payload(),
            headers=self.headers("employer-token"),
        )
        self.assertEqual(not_hired.status_code, 409)

    def test_rating_boundaries_and_successful_rpc_dispatch(self):
        for rating in (0, 6):
            response = self.client.post(
                "/feedback/complete-and-rate",
                json=self.payload(rating),
                headers=self.headers("employer-token"),
            )
            self.assertEqual(response.status_code, 400)

        valid = self.client.post(
            "/feedback/complete-and-rate",
            json=self.payload(5),
            headers=self.headers("employer-token"),
        )
        self.assertEqual(valid.status_code, 200)
        self.assertEqual(
            fake_supabase.rpc_calls[0][0], "complete_and_rate_job"
        )

    def test_duplicate_rating_is_rejected_without_second_rpc(self):
        first = self.client.post(
            "/feedback/complete-and-rate",
            json=self.payload(5),
            headers=self.headers("employer-token"),
        )
        self.assertEqual(first.status_code, 200)
        self.assertEqual(len(fake_supabase.rpc_calls), 1)

        fake_supabase.tables["Jobs"][0]["status"] = "closed"
        duplicate = self.client.post(
            "/feedback/complete-and-rate",
            json=self.payload(5),
            headers=self.headers("employer-token"),
        )

        self.assertEqual(duplicate.status_code, 409)
        self.assertEqual(
            duplicate.json()["detail"],
            "This worker has already been rated for this job",
        )
        self.assertEqual(len(fake_supabase.rpc_calls), 1)

    def test_rating_rpc_failure_returns_generic_response(self):
        fake_supabase.fail_rpc = "complete_and_rate_job"
        response = self.client.post(
            "/feedback/complete-and-rate",
            json=self.payload(5),
            headers=self.headers("employer-token"),
        )
        self.assertEqual(response.status_code, 500)
        self.assertEqual(
            response.json()["detail"],
            "Job completion and rating could not be saved",
        )
        self.assertNotIn("simulated RPC failure", response.text)


class AdminAuthorizationTests(BackendWorkflowTests):
    def test_admin_endpoint_requires_admin_role_and_hides_database_errors(self):
        self.seed_profile("worker-1", "auth-worker", "worker")
        worker_response = self.client.get(
            "/admin/dashboard-stats",
            headers=self.headers("worker-token"),
        )
        self.assertEqual(worker_response.status_code, 403)

        fake_supabase.auth.users["admin-token"] = SimpleNamespace(
            id="auth-admin", email="admin@example.test"
        )
        self.seed_profile("admin-1", "auth-admin", "admin")
        fake_supabase.fail_on = ("workers", "select")

        admin_response = self.client.get(
            "/admin/dashboard-stats",
            headers=self.headers("admin-token"),
        )
        self.assertEqual(admin_response.status_code, 500)
        self.assertEqual(
            admin_response.json()["detail"],
            "Admin dashboard data could not be retrieved",
        )
        self.assertNotIn("simulated database write failure", admin_response.text)


class RegistrationAndJobTests(BackendWorkflowTests):
    def setUp(self):
        super().setUp()

    def test_worker_registration_success_and_duplicate(self):
        with patch.object(
            worker_service, "encode_text", return_value=[0.0] * 384
        ):
            payload = {
                "full_name": "Synthetic Worker",
                "phone": "0000000000",
                "experience_years": 2,
                "expected_wage": 500,
                "location_lat": 0.0,
                "location_lng": 0.0,
                "category": "Plumbing",
                "skills": ["plumber"],
            }
            response = self.client.post(
                "/workers/",
                json=payload,
                headers=self.headers("worker-token"),
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(fake_supabase.tables["workers"]), 1)

        duplicate = self.client.post(
            "/workers/",
            json=payload,
            headers=self.headers("worker-token"),
        )
        self.assertEqual(duplicate.status_code, 409)

    def test_worker_registration_links_skills_and_rolls_back_on_failure(self):
        payload = {
            "full_name": "Synthetic Worker",
            "phone": "0000000000",
            "experience_years": 2,
            "expected_wage": 500,
            "location_lat": 0.0,
            "location_lng": 0.0,
            "category": "Plumbing",
            "skills": ["plumber", "pipe fitting"],
        }

        with patch.object(
            worker_service, "encode_text", return_value=[0.0] * 384
        ):
            success = self.client.post(
                "/workers/",
                json=payload,
                headers=self.headers("worker-token"),
            )

        self.assertEqual(success.status_code, 200)
        self.assertEqual(
            fake_supabase.rpc_calls[-1][0], "register_worker_atomic"
        )

        worker_id = success.json()["worker_id"]
        skill_ids_by_name = {
            row["skill_name"]: row["id"]
            for row in fake_supabase.tables["Skill_master"]
        }
        actual_links = {
            (row["worker_id"], row["skill_id"])
            for row in fake_supabase.tables["Worker_skills"]
        }

        self.assertEqual(
            actual_links,
            {
                (worker_id, skill_ids_by_name["plumber"]),
                (worker_id, skill_ids_by_name["pipe fitting"]),
            },
        )

        fake_supabase.reset()
        fake_supabase.auth.users = {
            "worker-token": SimpleNamespace(
                id="auth-worker", email="worker@example.test"
            ),
        }
        fake_supabase.fail_on = ("Worker_skills", "insert")

        with patch.object(
            worker_service, "encode_text", return_value=[0.0] * 384
        ):
            failed = self.client.post(
                "/workers/",
                json=payload,
                headers=self.headers("worker-token"),
            )

        self.assertEqual(failed.status_code, 500)
        self.assertEqual(
            failed.json()["detail"],
            "Worker registration could not be completed",
        )
        self.assertNotIn("simulated database write failure", failed.text)
        self.assertEqual(fake_supabase.tables["Profiles"], [])
        self.assertEqual(fake_supabase.tables["workers"], [])
        self.assertEqual(fake_supabase.tables["Skill_master"], [])
        self.assertEqual(fake_supabase.tables["Worker_skills"], [])

    def test_employer_registration_success_and_atomic_failure(self):
        payload = {
            "full_name": "Synthetic Employer",
            "phone": "0000000000",
            "employer_name": "Synthetic Co",
            "description": "Test",
            "location_lat": 0.0,
            "location_lng": 0.0,
        }

        success = self.client.post(
            "/employers/register",
            json=payload,
            headers=self.headers("unregistered-token"),
        )
        self.assertEqual(success.status_code, 200)
        self.assertEqual(
            fake_supabase.rpc_calls[-1][0], "register_employer_atomic"
        )
        self.assertEqual(len(fake_supabase.tables["Employers"]), 1)

        fake_supabase.reset()
        fake_supabase.auth.users = {
            "unregistered-token": SimpleNamespace(
                id="auth-new", email="new@example.test"
            ),
        }
        fake_supabase.fail_rpc = "register_employer_atomic"

        failed = self.client.post(
            "/employers/register",
            json=payload,
            headers=self.headers("unregistered-token"),
        )

        self.assertEqual(failed.status_code, 500)
        self.assertEqual(
            failed.json()["detail"],
            "Employer registration could not be completed",
        )
        self.assertNotIn("simulated RPC failure", failed.text)
        self.assertEqual(fake_supabase.tables["Profiles"], [])
        self.assertEqual(fake_supabase.tables["Employers"], [])

    def test_job_creation_and_atomic_failure(self):
        payload = {
            "title": "Synthetic job",
            "description": "Synthetic description",
            "location_text": "Test",
            "location_lat": 0.0,
            "location_lng": 0.0,
            "required_skills": ["plumber"],
            "budget": 500,
        }
        self.seed_profile("employer-1", "auth-employer", "employer")

        success = self.client.post(
            "/jobs/",
            json=payload,
            headers=self.headers("employer-token"),
        )
        self.assertEqual(success.status_code, 200)
        self.assertEqual(
            fake_supabase.rpc_calls[-1][0], "create_job_atomic"
        )
        self.assertEqual(len(fake_supabase.tables["Job_required_skill"]), 1)

        fake_supabase.reset()
        fake_supabase.auth.users = {
            "employer-token": SimpleNamespace(
                id="auth-employer", email="employer@example.test"
            ),
        }
        self.seed_profile("employer-1", "auth-employer", "employer")
        fake_supabase.fail_on = ("Job_required_skill", "insert")

        failed = self.client.post(
            "/jobs/",
            json=payload,
            headers=self.headers("employer-token"),
        )

        self.assertEqual(failed.status_code, 500)
        self.assertEqual(failed.json()["detail"], "Job could not be created")
        self.assertNotIn("simulated database write failure", failed.text)
        self.assertEqual(fake_supabase.tables["Jobs"], [])
        self.assertEqual(fake_supabase.tables["Job_required_skill"], [])


class EmployerOwnJobsTests(BackendWorkflowTests):
    def setUp(self):
        super().setUp()
        self.authenticated_profiles()
        self.seed_job("mine-open", "employer-1", "open")
        self.seed_job("mine-closed", "employer-1", "closed")
        self.seed_job("theirs", "employer-2", "open")
        for index, job in enumerate(fake_supabase.tables["Jobs"]):
            job["created_at"] = f"2026-01-0{index + 1}T00:00:00+00:00"

    def test_employer_sees_only_own_jobs_including_closed(self):
        response = self.client.get(
            "/jobs/mine", headers=self.headers("employer-token")
        )
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(body["count"], 2)
        self.assertEqual(
            {job["id"] for job in body["jobs"]},
            {"mine-open", "mine-closed"},
        )

    def test_my_jobs_requires_employer_login(self):
        self.assertEqual(self.client.get("/jobs/mine").status_code, 401)
        worker = self.client.get(
            "/jobs/mine", headers=self.headers("worker-token")
        )
        self.assertEqual(worker.status_code, 403)


if __name__ == "__main__":
    unittest.main()