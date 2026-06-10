# ── Variables ─────────────────────────────────────────────────────────────────
APP=app.main:app
PORT=8080

# ── Dev commands ──────────────────────────────────────────────────────────────
.PHONY: run
run:
	uv run uvicorn $(APP) --host 0.0.0.0 --port $(PORT) --reload

.PHONY: install
install:
	uv sync

.PHONY: test
test:
	uv run pytest tests/ -v

.PHONY: lint
lint:
	uv run ruff check app/

.PHONY: format
format:
	uv run ruff format app/

# ── Docker commands ───────────────────────────────────────────────────────────
.PHONY: docker-build
docker-build:
	docker build -f docker/Dockerfile -t fastapi-server-boilerplate .

.PHONY: docker-up
docker-up:
	docker compose -f docker/docker-compose.yml up --build -d

.PHONY: docker-down
docker-down:
	docker compose -f docker/docker-compose.yml down

.PHONY: docker-logs
docker-logs:
	docker compose -f docker/docker-compose.yml logs -f app

# ── Helpers ───────────────────────────────────────────────────────────────────
.PHONY: env
env:
	cp .env.example .env
	@echo ".env created from .env.example"

.PHONY: help
help:
	@echo ""
	@echo "  run           Run dev server with reload"
	@echo "  install       Install dependencies"
	@echo "  test          Run tests"
	@echo "  lint          Run ruff linter"
	@echo "  format        Run ruff formatter"
	@echo "  docker-build  Build Docker image"
	@echo "  docker-up     Start full stack"
	@echo "  docker-down   Stop stack"
	@echo "  docker-logs   Tail app logs"
	@echo "  env           Create .env from .env.example"
	@echo ""