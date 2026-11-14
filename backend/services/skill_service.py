
import logging

from backend.database.supabase_client import supabase


class SkillService:
    logger = logging.getLogger(__name__)

    @staticmethod
    def get_all_skills() -> list[dict]:
        """
        Retrieve the complete Skill Master catalogue.

        Returns:
            A list containing skill ID, skill name and category.
            Empty or NULL categories are normalized to None.
        """
        try:
            response = (
                supabase.table("Skill_master")
                .select("id, skill_name, category")
                .order("category")
                .order("skill_name")
                .execute()
            )

            skills = []

            for record in response.data or []:
                category = record.get("category")

                if isinstance(category, str):
                    category = category.strip() or None

                skills.append({
                    "id": str(record["id"]),
                    "skill_name": record["skill_name"],
                    "category": category,
                })

            return skills

        except Exception as exc:
            SkillService.logger.error(
                "Skill catalogue retrieval failed (exception_type=%s)",
                type(exc).__name__,
            )
            raise RuntimeError(
                "Skill catalogue could not be retrieved"
            ) from exc
