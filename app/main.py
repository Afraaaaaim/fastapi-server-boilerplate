from contextlib import asynccontextmanager

import structlog
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from app.api.v1.router import api_router
from app.core.config import get_settings
from app.core.logging import setup_logging
from app.core.telemetry import setup_telemetry, shutdown_telemetry
from app.middleware.logging import RequestLoggingMiddleware

logger = structlog.get_logger(__name__)


def create_app() -> FastAPI:
    settings = get_settings()

    # 1. Logging must be first
    setup_logging(settings)

    # 2. Rate limiter setup
    limiter = Limiter(
        key_func=get_remote_address,
        default_limits=[settings.rate_limit],
    )

    # 3. Create FastAPI app
    app = FastAPI(
        title=settings.service_name,
        version="0.1.0",
        docs_url="/docs" if settings.docs_enabled else None,
        redoc_url="/redoc" if settings.docs_enabled else None,
        openapi_url="/openapi.json" if settings.docs_enabled else None,
    )

    # 4. Attach rate limiter to app state
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    # 5. Middleware (order matters — first added = outermost = last to run)
    app.add_middleware(RequestLoggingMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 6. Lifespan for startup/shutdown
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        # Startup
        tp = setup_telemetry(settings)

        logger.info(
            "startup complete",
            service=settings.service_name,
            env=settings.env,
            log_level=settings.log_level,
            log_format=settings.log_format,
            docs_enabled=settings.docs_enabled,
            auth_enabled=settings.auth_enabled,
        )

        yield

        # Shutdown
        shutdown_telemetry(tp)
        logger.info("shutdown complete")

    app.router.lifespan_context = lifespan

    # 7. Include routers — log each registered route
    for route in api_router.routes:
        methods = getattr(route, "methods", {"GET"})
        logger.info(
            "route registered",
            method="|".join(sorted(methods)),
            path=route.path,
        )

    app.include_router(api_router)

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn

    settings = get_settings()

    uvicorn.run(
        "app.main:app",  # adjust module path if needed
        host=settings.host,
        port=settings.port,
        reload=settings.env == "development",
        log_level=settings.log_level.lower(),
    )