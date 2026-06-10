# ── Stage 1: Runtime ──────────────────────────────────────────────────────────
FROM python:3.14-slim

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

COPY pyproject.toml uv.lock* ./
COPY app/ ./app/
COPY main.py .

RUN uv sync --frozen --no-dev

ENV PYTHONPATH="/app"

EXPOSE 8080

CMD ["uv", "run", "main.py"]