from fastapi import Depends, HTTPException, Security, status
from fastapi.security import APIKeyHeader, APIKeyQuery

from app.core.config import get_settings, Settings
from app.core.security import build_key_set, verify_key, extract_client_id

# Accept key from header or query param
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)
api_key_query = APIKeyQuery(name="api_key", auto_error=False)

# Pre-hash valid keys once at startup
_settings = get_settings()
_hashed_keys = build_key_set(_settings.api_keys)


async def verify_api_key(
    header_key: str | None = Security(api_key_header),
    query_key: str | None = Security(api_key_query),
    settings: Settings = Depends(get_settings),
) -> str:
    """
    FastAPI dependency that validates API key auth.
    Returns the client_id (safe hash prefix) on success.
    Raises 401 if auth is enabled and key is missing or invalid.
    Skips validation entirely if no API keys are configured.
    """
    # Auth disabled
    if not settings.auth_enabled:
        return "anonymous"

    raw_key = header_key or query_key
    if not raw_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "code": "UNAUTHORIZED",
                "message": "missing API key",
            },
            headers={"WWW-Authenticate": "ApiKey"},
        )

    if not verify_key(raw_key, _hashed_keys):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "code": "UNAUTHORIZED",
                "message": "invalid API key",
            },
            headers={"WWW-Authenticate": "ApiKey"},
        )

    return extract_client_id(raw_key)