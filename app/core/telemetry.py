from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource, SERVICE_NAME, DEPLOYMENT_ENVIRONMENT
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.propagate import set_global_textmap
from opentelemetry.propagators.composite import CompositePropagator
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
from opentelemetry.baggage.propagation import W3CBaggagePropagator

from app.core.logging import get_logger

logger = get_logger(__name__)


def setup_telemetry(settings) -> TracerProvider:
    """
    Configure OTel tracer provider.
    If OTLP_ENDPOINT is empty, no exporter is added — traces are
    collected but silently dropped (safe no-op behavior).
    """
    resource = Resource(
        attributes={
            SERVICE_NAME: settings.service_name,
            DEPLOYMENT_ENVIRONMENT: settings.env,
        }
    )

    provider = TracerProvider(resource=resource)

    if settings.otlp_enabled:
        exporter = OTLPSpanExporter(
            endpoint=settings.otlp_endpoint,
            insecure=True,
        )
        provider.add_span_processor(BatchSpanProcessor(exporter))
        logger.info(
            "otlp tracing enabled",
            endpoint=settings.otlp_endpoint,
        )
    else:
        logger.info("otlp tracing disabled")

    trace.set_tracer_provider(provider)

    # W3C TraceContext + Baggage — current OTel standard
    set_global_textmap(
        CompositePropagator([
            TraceContextTextMapPropagator(),
            W3CBaggagePropagator(),
        ])
    )

    return provider


def shutdown_telemetry(provider: TracerProvider) -> None:
    """Flush and stop the tracer provider cleanly on shutdown."""
    provider.shutdown()