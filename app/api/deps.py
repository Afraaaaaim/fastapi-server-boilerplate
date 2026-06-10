from fastapi import Depends, HTTPException, Security, status
from fastapi.security import APIKeyHeader, APIKeyQuery

from app.core.config import get_settings, Settings
from app.core.security import build_key_set, verify_key, extract_client_id

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)
api_key_query = APIKeyQuery(name="api_key", auto_error=False)

_settings = get_settings()
_hashed_keys = build_key_set(_settings.api_keys)


async def verify_api_key(
    header_key: str | None = Security(api_key_header),
    query_key: str | None = Security(api_key_query),
) -> str:
    # Auth disabled — no keys configured
    if not _hashed_keys:
        return "anonymous"

    raw_key = header_key or query_key
    if not raw_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"code": "UNAUTHORIZED", "message": "missing API key"},
            headers={"WWW-Authenticate": "ApiKey"},
        )

    if not verify_key(raw_key, _hashed_keys):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"code": "UNAUTHORIZED", "message": "invalid API key"},
            headers={"WWW-Authenticate": "ApiKey"},
        )

    return extract_client_id(raw_key)