
import json
import logging
from uuid import UUID

from backend.database.supabase_client import supabase
from backend.services.embedding_service import encode_text


class JobService:
    logger = logging.getLogger(__name__)

    @staticmethod
    def _public_job(job: dict) -> dict:
        """Return the public job representation without internal location text."""
        if not isinstance(job, dict):
            return job

        result = dict(job)
        result.pop("location_text", None)

        for key in ("location_lat", "location_lng"):
            value = result.get(key)
            if isinstance(value, (int, float)):
                result[key] = round(value, 2)

        return result

    @staticmethod
    def normalize_skill(skill: str) -> str:
        return " ".join(str(skill).strip().casefold().split())

    @staticmethod
    def _is_uuid(value: str) -> bool:
        try:
            UUID(str(value).strip())
            return True
        except (ValueError, TypeError, AttributeError):
            return False

    @staticmethod
    def _serialize_embedding(vector) -> str:
        """Serialize the embedding without NumPy's possible ellipsis truncation."""
        values = [float(value) for value in vector]

        if len(values) != 384:
            raise ValueError(
                f"Expected a 384-dimensional embedding, received {len(values)}"
            )

        return json.dumps(values, separators=(",", ":"))

    @staticmethod
    def resolve_skill(skill_value: str) -> dict:
        """
        Resolve an existing skill by UUID or name.
        New skills are created inside the atomic job-creation RPC.
        """
        raw = str(skill_value or "").strip()
        if not raw:
            raise ValueError("Empty skill is not valid")

        if JobService._is_uuid(raw):
            result = (
                supabase.table("Skill_master")
                .select("id, skill_name")
                .eq("id", raw)
                .execute()
            )
            if not result.data:
                raise ValueError("Unknown skill ID")
            return result.data[0]

        normalized = JobService.normalize_skill(raw)

        result = (
            supabase.table("Skill_master")
            .select("id, skill_name")
            .ilike("skill_name", normalized)
            .execute()
        )

        if result.data:
            return result.data[0]

        # Defer new skill creation to the atomic RPC.
        return {"id": None, "skill_name": normalized}

    @staticmethod
    def get_or_create_skill_id(skill_name: str):
        skill = JobService.resolve_skill(skill_name)

        if skill["id"] is None:
            raise RuntimeError(
                "New skills must be created through atomic job creation"
            )

        return skill["id"]

    @staticmethod
    def create_job(data: dict, employer_id: str):
        try:
            employer = (
                supabase.table("Profiles")
                .select("id, role")
                .eq("id", str(employer_id))
                .execute()
            )

            if not employer.data or employer.data[0].get("role") != "employer":
                return {
                    "error": "Employer not found or unauthorized",
                    "status_code": 403,
                }

            submitted_skills = data.get("required_skills") or []

            if isinstance(submitted_skills, str):
                submitted_skills = [submitted_skills]

            if not isinstance(submitted_skills, (list, tuple, set)):
                return {
                    "error": "Required skills must be a list",
                    "status_code": 400,
                }

            unique_skills = []
            seen = set()

            for value in submitted_skills:
                raw = str(value or "").strip()

                if not raw:
                    return {
                        "error": "One or more required skills are invalid",
                        "status_code": 400,
                    }

                key = raw.casefold()
                if key not in seen:
                    seen.add(key)
                    unique_skills.append(raw)

            title = str(data.get("title") or "").strip()
            description = str(data.get("description") or "").strip()

            if not title or not description:
                return {
                    "error": "Job title and description are required",
                    "status_code": 400,
                }

            skill_text = ", ".join(
                JobService.normalize_skill(skill)
                for skill in unique_skills
                if not JobService._is_uuid(skill)
            )

            job_text = f"{title} {skill_text} {skill_text} {description}"
            vector = encode_text(job_text)
            embedding_text = JobService._serialize_embedding(vector)

            response = supabase.rpc(
                "create_job_atomic",
                {
                    "p_employer_id": str(employer_id),
                    "p_title": title,
                    "p_description": description,
                    "p_location_text": data.get("location_text"),
                    "p_location_lat": data.get("location_lat"),
                    "p_location_lng": data.get("location_lng"),
                    "p_budget": data.get("budget", 0),
                    "p_required_skills": unique_skills,
                    "p_embedding_text": embedding_text,
                },
            ).execute()

            result = response.data

            if isinstance(result, list) and result:
                result = result[0]

            if isinstance(result, str):
                result = json.loads(result)

            if not isinstance(result, dict) or not result.get("job_id"):
                JobService.logger.error(
                    "Atomic job creation returned an unexpected response"
                )
                return {
                    "error": "Job could not be created",
                    "status_code": 500,
                }

            return {
                "status": "success",
                "job_id": str(result["job_id"]),
            }

        except ValueError:
            JobService.logger.warning("Job creation rejected invalid input")
            return {
                "error": "One or more required skills or input values are invalid",
                "status_code": 400,
            }
        except Exception as exc:
            JobService.logger.error(
                "Job creation failed (exception_type=%s)",
                type(exc).__name__,
            )
            return {
                "error": "Job could not be created",
                "status_code": 500,
            }

    @staticmethod
    def get_job_details(job_id: str):
        try:
            result = (
                supabase.table("Jobs")
                .select("*")
                .eq("id", job_id)
                .single()
                .execute()
            )

            if not result.data:
                return None

            return JobService._public_job(result.data)

        except Exception as exc:
            JobService.logger.error(
                "Job lookup failed (exception_type=%s)",
                type(exc).__name__,
            )
            return None

    @staticmethod
    def get_jobs_for_employer(employer_id: str):
        """Every job owned by this employer, newest first, without embeddings."""
        result = (
            supabase.table("Jobs")
            .select(
                "id, employer_id, title, description, budget, status, "
                "created_at, location_lat, location_lng"
            )
            .eq("employer_id", str(employer_id))
            .order("created_at", desc=True)
            .execute()
        )
        return [JobService._public_job(job) for job in (result.data or [])]

    @staticmethod
    def get_all_jobs():
        try:
            result = (
                supabase.table("Jobs") \
                    .select("*") \
                    .eq("status", "open") \
                    .order("created_at", desc=True) \
                    .execute()
            )

            return [
                JobService._public_job(job)
                for job in (result.data or [])
            ]

        except Exception as exc:
            JobService.logger.error(
                "Job listing failed (exception_type=%s)",
                type(exc).__name__,
            )
            return []
