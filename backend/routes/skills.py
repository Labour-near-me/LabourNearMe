
import logging

from fastapi import APIRouter, HTTPException

from backend.services.skill_service import SkillService

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/")
def get_all_skills():
    """
    Retrieve the complete Skill Master catalogue.
    """
    try:
        skills = SkillService.get_all_skills()
        return {"skills": skills}

    except RuntimeError:
        logger.error("Unable to retrieve Skill Master catalogue")
        raise HTTPException(
            status_code=500,
            detail="Skill catalogue could not be retrieved",
        )
