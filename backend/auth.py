"""Authentication and profile dependencies for protected API routes."""

import logging
from typing import Any, Callable

import httpx
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

try:
    from gotrue.errors import AuthApiError, AuthRetryableError
except ImportError:  # newer Supabase packages renamed gotrue
    from supabase_auth.errors import AuthApiError, AuthRetryableError

from backend.database.supabase_client import supabase


logger = logging.getLogger(__name__)

_bearer_scheme = HTTPBearer(auto_error=False)


def _is_auth_service_failure(exc: Exception) -> bool:
    """True when Supabase could not be reached or failed on its side.

    These are NOT problems with the user's token, so they must not be
    reported as invalid credentials. Everything else is rejected (fail closed).
    """
    if isinstance(exc, (AuthRetryableError, httpx.HTTPError)):
        return True

    if isinstance(exc, AuthApiError):
        status_code = getattr(exc, "status", None)
        return isinstance(status_code, int) and status_code >= 500

    return False


def get_authenticated_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer_scheme),
) -> Any:
    """Validate a Supabase access token and return its authenticated user.

    Works for any Supabase sign-in method (phone OTP, Google, ...) because
    the token is always a Supabase-issued access token.
    """
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="A valid sign-in token is required",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        response = supabase.auth.get_user(credentials.credentials)
        user = response.user
    except Exception as exc:
        if _is_auth_service_failure(exc):
            # Log only the exception type, never the token.
            logger.error(
                "Supabase auth service unavailable (exception_type=%s)",
                type(exc).__name__,
            )
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Sign-in service is temporarily unavailable. Please try again.",
            ) from exc
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