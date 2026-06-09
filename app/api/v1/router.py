import structlog
from fastapi import APIRouter

from app.api.v1.endpoints import health, example

logger = structlog.get_logger(__name__)

api_router = APIRouter()

# Register routers and log at startup
_routers = [
    (health.router, "", ["health"]),
    (example.router, "/api/v1", ["example"]),
]

for router, prefix, tags in _routers:
    api_router.include_router(router, prefix=prefix)