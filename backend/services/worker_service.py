
import json
import logging
from uuid import UUID

from backend.database.supabase_client import supabase
from backend.services.embedding_service import encode_text


class WorkerService:
    logger = logging.getLogger(__name__)

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
        """Serialize a 384-dimensional embedding without NumPy truncation."""
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
        New skills are created inside the atomic registration RPC.
        """
        raw = str(skill_value or "").strip()
        if not raw:
            raise ValueError("Empty skill is not valid")

        if WorkerService._is_uuid(raw):
            result = (
                supabase.table("Skill_master")
                .select("id, skill_name")
                .eq("id", raw)
                .execute()
            )
            if not result.data:
                raise ValueError("Unknown skill ID")
            return result.data[0]

        normalized = WorkerService.normalize_skill(raw)
        result = (
            supabase.table("Skill_master")
            .select("id, skill_name")
            .ilike("skill_name", normalized)
            .execute()
        )

        if result.data:
            return result.data[0]

        # Defer creation until the atomic RPC so a failed registration
        # cannot leave behind an orphan Skill_master row.
        return {"id": None, "skill_name": normalized}

    @staticmethod
    def get_or_create_skill_id(skill_name: str):
        skill = WorkerService.resolve_skill(skill_name)
        if skill["id"] is None:
            raise RuntimeError(
                "New skills must be created through atomic worker registration"
            )
        return skill["id"]

    @staticmethod
    def register_new_worker(data: dict, auth_user_id: str):
        try:
            category = str(data.get("category") or "General").strip()
            submitted_skills = data.get("skills") or []
            experience = data.get("experience_years", 0)

            if isinstance(submitted_skills, str):
                submitted_skills = [submitted_skills]

            if not isinstance(submitted_skills, (list, tuple, set)):
                return {
                    "error": "Skills must be a list",
                    "status_code": 400,
                }

            # Normalize and deduplicate submitted skill names/IDs.
            unique_skills = []
            seen = set()

            for value in submitted_skills:
                raw = str(value or "").strip()
                if not raw:
                    return {
                        "error": "One or more selected skills are invalid",
                        "status_code": 400,
                    }

                key = raw.casefold()
                if key not in seen:
                    seen.add(key)
                    unique_skills.append(raw)

            # Use submitted names in the embedding text. Skill creation and
            # linking itself happen within the database transaction.
            embedding_skill_names = []
            for skill_value in unique_skills:
                if WorkerService._is_uuid(skill_value):
                    resolved = WorkerService.resolve_skill(skill_value)
                    embedding_skill_names.append(resolved["skill_name"])
                else:
                    embedding_skill_names.append(
                        WorkerService.normalize_skill(skill_value)
                    )

            skill_text = ", ".join(embedding_skill_names)
            text = (
                f"{category} {skill_text} {skill_text} "
                f"Experience {experience} years {category} work"
            ).strip()

            vector = encode_text(text)
            embedding_text = WorkerService._serialize_embedding(vector)

            response = supabase.rpc(
                "register_worker_atomic",
                {
                    "p_auth_user_id": str(auth_user_id),
                    "p_full_name": data.get("full_name"),
                    "p_phone": data.get("phone"),
                    "p_experience_years": experience,
                    "p_expected_wage": data.get("expected_wage"),
                    "p_location_lat": data.get("location_lat"),
                    "p_location_lng": data.get("location_lng"),
                    "p_category": category,
                    "p_skills": unique_skills,
                    "p_embedding_text": embedding_text,
                },
            ).execute()

            result = response.data

            # PostgREST may return a JSON object directly or wrapped in a list.
            if isinstance(result, list) and result:
                result = result[0]

            if isinstance(result, str):
                result = json.loads(result)

            if not isinstance(result, dict) or not result.get("worker_id"):
                WorkerService.logger.error(
                    "Atomic worker registration returned an unexpected response"
                )
                return {
                    "error": "Worker registration could not be completed",
                    "status_code": 500,
                }

            return {
                "status": "success",
                "worker_id": str(result["worker_id"]),
            }

        except ValueError:
            WorkerService.logger.warning(
                "Worker registration rejected invalid input"
            )
            return {
                "error": "One or more selected skills or input values are invalid",
                "status_code": 400,
            }
        except Exception as exc:
            WorkerService.logger.error(
                "Worker registration failed (exception_type=%s)",
                type(exc).__name__,
            )

            # Unique auth_user_id constraint can reject duplicate registrations.
            error_text = str(exc).casefold()
            if (
                "profiles_auth_user_id_unique" in error_text
                or "duplicate key" in error_text
                or "23505" in error_text
            ):
                return {
                    "error": "A profile already exists for this account",
                    "status_code": 409,
                }

            return {
                "error": "Worker registration could not be completed",
                "status_code": 500,
            }

    @staticmethod
    def get_worker_details(worker_id: str):
        try:
            result = (
                supabase.table("Profiles")
                .select(
                    "id, full_name, phone, role, "
                    "workers(id, experience_years, expected_wage, "
                    "location_lat, location_lng, availability_status, rating)"
                )
                .eq("id", worker_id)
                .single()
                .execute()
            )
            return result.data
        except Exception as exc:
            WorkerService.logger.error(
                "Worker profile lookup failed (exception_type=%s)",
                type(exc).__name__,
            )
            return None
