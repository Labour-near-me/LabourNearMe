
import logging

from fastapi import APIRouter, Depends, HTTPException

from backend.database.supabase_client import supabase
from backend.auth import get_authenticated_user

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/register")
def register_employer(data: dict, user=Depends(get_authenticated_user)):
    try:
        auth_user_id = str(user.id)

        # Friendly duplicate check. The database's unique constraint remains
        # the final protection against simultaneous duplicate registrations.
        existing = (
            supabase.table("Profiles")
            .select("id, role")
            .eq("auth_user_id", auth_user_id)
            .execute()
        )

        if existing.data:
            raise HTTPException(
                status_code=409,
                detail="A profile already exists for this account",
            )

        employer_name = str(data.get("employer_name") or "").strip()

        if not employer_name:
            raise HTTPException(
                status_code=422,
                detail="Employer name is required",
            )

        if data.get("location_lat") is None or data.get("location_lng") is None:
            raise HTTPException(
                status_code=422,
                detail="Employer location is required",
            )

        response = supabase.rpc(
            "register_employer_atomic",
            {
                "p_auth_user_id": auth_user_id,
                "p_full_name": data.get("full_name"),
                "p_phone": data.get("phone"),
                "p_employer_name": employer_name,
                "p_description": data.get("description"),
                "p_location_lat": data.get("location_lat"),
                "p_location_lng": data.get("location_lng"),
            },
        ).execute()

        result = response.data

        if isinstance(result, list) and result:
            result = result[0]

        if isinstance(result, str):
            import json
            result = json.loads(result)

        if not isinstance(result, dict) or not result.get("employer_id"):
            logger.error("Atomic employer registration returned an unexpected response")
            raise HTTPException(
                status_code=500,
                detail="Employer registration could not be completed",
            )

        return {
            "status": "success",
            "employer_id": str(result["employer_id"]),
        }

    except HTTPException:
        raise

    except Exception as exc:
        error_text = str(exc).casefold()

        if (
            "profiles_auth_user_id_unique" in error_text
            or "duplicate key" in error_text
            or "23505" in error_text
        ):
            raise HTTPException(
                status_code=409,
                detail="A profile already exists for this account",
            ) from exc

        logger.error(
            "Employer registration failed (exception_type=%s)",
            type(exc).__name__,
        )
        raise HTTPException(
            status_code=500,
            detail="Employer registration could not be completed",
        ) from exc
