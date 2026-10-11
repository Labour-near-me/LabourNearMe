"""Authentication and profile dependencies for protected API routes."""

from typing import Any, Callable

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from backend.database.supabase_client import supabase


_bearer_scheme = HTTPBearer(auto_error=False)


def get_authenticated_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer_scheme),
) -> Any:
    """Validate a Supabase access token and return its authenticated user."""
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="A valid sign-in token is required",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        response = supabase.auth.get_user(credentials.credentials)
        user = response.user
    except Exception:
        user = None

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="The sign-in token is invalid or expired",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


def get_current_profile(user: Any = Depends(get_authenticated_user)) -> dict:
    """Resolve the authenticated Supabase user to its application profile."""
    profile = (
        supabase.table("Profiles")
        .select("id, role, full_name, phone")
        .eq("auth_user_id", str(user.id))
        .execute()
    )

    if not profile.data:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Complete worker or employer profile registration first",
        )

    return profile.data[0]


def require_role(role: str) -> Callable:
    """Build a dependency that requires a profile with the requested role."""
    def _require_role(profile: dict = Depends(get_current_profile)) -> dict:
        if profile.get("role") != role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"A {role} account is required for this action",
            )
        return profile

    return _require_role
