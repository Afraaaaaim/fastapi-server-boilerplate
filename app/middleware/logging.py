import time
import uuid
from typing import Callable

import structlog
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

logger = structlog.get_logger(__name__)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    Logs every request with method, path, status, latency, and request ID.
    Also injects request_id into structlog context so all logs within
    a request automatically carry it.
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Respect existing request ID from upstream proxy, or generate one
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        start = time.perf_counter()

        # Bind request_id to structlog context for this request
        # All logs within this request will automatically include it
        structlog.contextvars.clear_contextvars()
        structlog.contextvars.bind_contextvars(request_id=request_id)

        response = await call_next(request)

        latency_ms = round((time.perf_counter() - start) * 1000, 2)
        status = response.status_code

        log_method = logger.info
        if status >= 500:
            log_method = logger.error
        elif status >= 400:
            log_method = logger.warning

        log_method(
            "request completed",
            method=request.method,
            path=request.url.path,
            status=status,
            latency_ms=latency_ms,
            client_ip=request.client.host if request.client else None,
            user_agent=request.headers.get("user-agent"),
        )

        response.headers["X-Request-ID"] = request_id
        return response