import logging
import sys
from typing import Any

import structlog
from structlog.types import EventDict, WrappedLogger


def add_service_info(
    settings: Any,
) -> structlog.types.Processor:
    """Processor that injects service name and env into every log record."""

    def processor(
        logger: WrappedLogger, method: str, event_dict: EventDict
    ) -> EventDict:
        event_dict["service"] = settings.service_name
        event_dict["env"] = settings.env
        return event_dict

    return processor


def setup_logging(settings: Any) -> None:
    """
    Configure structlog based on settings.

    LOG_FORMAT=text  → human-readable colored console output (development)
    LOG_FORMAT=json  → machine-readable JSON (production/containers)
    LOG_LEVEL        → debug | info | warning | error
    LOG_FILE         → file path or empty for stdout
    """
    level = getattr(logging, settings.log_level.upper(), logging.INFO)

    # Output destination
    if settings.log_file:
        output = open(settings.log_file, "a", encoding="utf-8")  # noqa: WPS515
    else:
        output = sys.stdout

    # Shared processors applied to every log record
    shared_processors: list[structlog.types.Processor] = [
        structlog.contextvars.merge_contextvars,
        add_service_info(settings),
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.CallsiteParameterAdder(
            [
                structlog.processors.CallsiteParameter.FILENAME,
                structlog.processors.CallsiteParameter.FUNC_NAME,
                structlog.processors.CallsiteParameter.LINENO,
            ]
        ),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.ExceptionRenderer(),
    ]

    if settings.log_format == "json":
        renderer = structlog.processors.JSONRenderer()
    else:
        renderer = structlog.dev.ConsoleRenderer(colors=sys.stdout.isatty())

    structlog.configure(
        processors=shared_processors + [renderer],
        wrapper_class=structlog.make_filtering_bound_logger(level),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(file=output),
        cache_logger_on_first_use=True,
    )

    # Also configure stdlib logging so uvicorn/gunicorn logs flow through structlog
    logging.basicConfig(
        format="%(message)s",
        stream=output,
        level=level,
    )
    logging.getLogger("uvicorn.access").handlers = []
    logging.getLogger("uvicorn.access").propagate = False


def get_logger(name: str = __name__) -> structlog.BoundLogger:
    """Get a structlog logger bound to the given name."""
    return structlog.get_logger(name)