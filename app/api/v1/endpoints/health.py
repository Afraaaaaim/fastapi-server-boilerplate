from datetime import datetime, timezone

from fastapi import APIRouter

router = APIRouter()


@router.get("/healthz", tags=["health"])
async def healthz():
    """Liveness probe — confirms the process is alive."""
    return {
        "status": "ok",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@router.get("/readyz", tags=["health"])
async def readyz():
    """
    Readiness probe — confirms the service is ready to serve traffic.
    Add dependency checks here (DB ping, cache, etc) as you extend the boilerplate.
    Return 503 if any critical dependency is unavailable.
    """
    return {
        "status": "ready",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }