# fastapi-server-boilerplate

A production-ready FastAPI server template.

## What's included

- [FastAPI](https://fastapi.tiangolo.com/) with auto-generated Swagger docs (`/docs`)
- Structured logging with [structlog](https://www.structlog.org/) and OpenTelemetry bridge
- API key authentication via FastAPI dependency injection
- Rate limiting with [slowapi](https://github.com/laurentS/slowapi)
- Standardized JSON error responses
- Request ID propagation
- Docker + Docker Compose (app, Redis, OTel Collector, Jaeger)
- API versioning (`/api/v1/`)

## Quick start

```bash
cp .env.example .env
# edit .env and add your API keys
uv run main.py
```

## Environment variables

| Variable | Default | Description |
|---|---|---|
| `PORT` | `8080` | Server port |
| `ENV` | `development` | `development` `staging` `production` |
| `WORKERS` | `1` | Uvicorn worker count |
| `LOG_LEVEL` | `info` | `debug` `info` `warning` `error` |
| `LOG_FORMAT` | `text` | `text` or `json` |
| `LOG_FILE` | stdout | File path for logs |
| `API_KEYS` | — | Comma-separated valid API keys |
| `RATE_LIMIT` | `100/minute` | slowapi format e.g. `100/minute` `10/second` |
| `OTLP_ENDPOINT` | disabled | OTel collector endpoint e.g. `localhost:4317` |
| `SERVICE_NAME` | `fastapi-server-boilerplate` | Service name in traces/logs |
| `DOCS_ENABLED` | `true` | Set `false` to disable Swagger UI in production |

## Endpoints

| Method | Path | Auth | Description |
|---|---|---|---|
| GET | `/healthz` | No | Liveness probe |
| GET | `/readyz` | No | Readiness probe |
| GET | `/api/v1/example` | Yes | Example protected route |
| GET | `/docs` | No | Swagger UI (if enabled) |

## Auth

Pass your API key in either of these ways:

```
X-API-Key: your-key
?api_key=your-key
```

## Adding a new endpoint

1. Create `app/api/v1/endpoints/your_module.py` with an `APIRouter`
2. Add it to `app/api/v1/router.py`:

```python
from app.api.v1.endpoints import health, example, your_module

_routers = [
    (health.router, "", ["health"]),
    (example.router, "/api/v1", ["example"]),
    (your_module.router, "/api/v1", ["your_module"]),  # add this
]
```

That's it — routes auto-log at startup and appear in Swagger docs automatically.

## Run with Docker

```bash
docker compose -f docker/docker-compose.yml up --build -d
```

Jaeger UI at `http://localhost:16686`
Swagger UI at `http://localhost:8080/docs`

## Make targets

```
make run          run dev server with reload
make install      install dependencies
make test         run tests
make lint         run ruff linter
make format       run ruff formatter
make docker-up    start full stack
make docker-down  stop stack
make docker-logs  tail app logs
```