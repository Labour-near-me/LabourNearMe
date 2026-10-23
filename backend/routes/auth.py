
"""Authenticated user identity endpoint."""

from fastapi import APIRouter, Depends, HTTPException
from backend.auth import get_authenticated_user
from backend.database.supabase_client import supabase

router = APIRouter()


@router.get("/me")
def get_me(user=Depends(get_authenticated_user)):
    """Return the authenticated Supabase user and their application profile."""

    try:
        response = (
            supabase.table("Profiles")
            .select("id, role, full_name, phone")
            .eq("auth_user_id", str(user.id))
            .execute()
        )
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Unable to retrieve user profile",
        )

    profiles = response.data or []

    if len(profiles) > 1:
        raise HTTPException(
            status_code=409,
            detail="Multiple profiles are linked to this account",
        )

    if not profiles:
        return {
            "user_id": str(user.id),
            "email": getattr(user, "email", None),
            "profile": None,
            "profile_status": "missing",
            "needs_registration": True,
        }

    return {
        "user_id": str(user.id),
        "email": getattr(user, "email", None),
        "profile": profiles[0],
        "profile_status": "complete",
        "needs_registration": False,
    }
