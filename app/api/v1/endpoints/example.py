import structlog
from fastapi import APIRouter, Depends

from app.api.deps import verify_api_key

router = APIRouter()
logger = structlog.get_logger(__name__)


@router.get("/example", tags=["example"])
async def example(client_id: str = Depends(verify_api_key)):
    """
    Example protected endpoint.
    Requires a valid API key via X-API-Key header or ?api_key= query param.
    Replace or delete this once you add real domain endpoints.
    """
    logger.info("example endpoint called", client_id=client_id)
    return {
        "message": "boilerplate is working",
        "client_id": client_id,
    }