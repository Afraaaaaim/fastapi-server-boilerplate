import pytest
from fastapi.testclient import TestClient


@pytest.fixture(scope="module")
def client_no_auth():
    from app.main import create_app
    app = create_app()
    return TestClient(app)


@pytest.fixture(scope="module")
def client_with_auth(monkeypatch_module):
    import app.api.deps as deps
    from app.core.security import build_key_set
    deps._hashed_keys = build_key_set(["test-key"])
    from app.main import create_app
    app = create_app()
    return TestClient(app)


def test_healthz(client_no_auth):
    response = client_no_auth.get("/healthz")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "timestamp" in data


def test_readyz(client_no_auth):
    response = client_no_auth.get("/readyz")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ready"
    assert "timestamp" in data


def test_example_no_auth():
    import app.api.deps as deps
    from app.core.security import build_key_set
    from app.main import create_app
    from fastapi.testclient import TestClient

    # Enable auth with a known key
    deps._hashed_keys = build_key_set(["test-key"])

    app = create_app()
    client = TestClient(app)

    response = client.get("/api/v1/example")
    assert response.status_code == 401


def test_example_invalid_key():
    import app.api.deps as deps
    from app.core.security import build_key_set
    from app.main import create_app
    from fastapi.testclient import TestClient

    deps._hashed_keys = build_key_set(["test-key"])

    app = create_app()
    client = TestClient(app)

    response = client.get("/api/v1/example", headers={"X-API-Key": "wrong-key"})
    assert response.status_code == 401


def test_example_valid_key():
    import app.api.deps as deps
    from app.core.security import build_key_set
    from app.main import create_app
    from fastapi.testclient import TestClient

    deps._hashed_keys = build_key_set(["test-key"])

    app = create_app()
    client = TestClient(app)

    response = client.get("/api/v1/example", headers={"X-API-Key": "test-key"})
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "boilerplate is working"
    assert "client_id" in data