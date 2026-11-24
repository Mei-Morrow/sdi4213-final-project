from uuid import uuid4

import psycopg
import pytest
from fastapi.testclient import TestClient

from app import main


@pytest.fixture
def client():
    with TestClient(main.app) as test_client:
        yield test_client


def test_application_info(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["application"] == "DevOps Task Tracker"


def test_liveness(client):
    response = client.get("/healthz")

    assert response.status_code == 200
    assert response.json() == {"status": "alive"}


def test_readiness_with_database(client):
    response = client.get("/ready")

    assert response.status_code == 200
    assert response.json() == {"status": "ready"}


@pytest.mark.parametrize("title", ["", "   ", "\t\n", "x" * 201, None])
def test_invalid_task_title_is_rejected(client, title):
    response = client.post("/tasks", json={"title": title})

    assert response.status_code == 422


def test_create_and_retrieve_task(client):
    title = f"Automated test {uuid4().hex}"
    task_id = None

    try:
        response = client.post("/tasks", json={"title": title})

        assert response.status_code == 201
        task = response.json()
        task_id = task["id"]

        assert isinstance(task_id, int)
        assert task["title"] == title
        assert task["completed"] is False

        response = client.get("/tasks")

        assert response.status_code == 200
        assert task in response.json()
    finally:
        if task_id is not None:
            with main.connect_db() as connection:
                connection.execute(
                    "DELETE FROM tasks WHERE id = %s",
                    (task_id,),
                )


def test_database_failure_behavior(client, monkeypatch):
    def unavailable_database():
        raise psycopg.OperationalError("Simulated database outage")

    monkeypatch.setattr(main, "connect_db", unavailable_database)

    # The application remains alive when its database is unavailable.
    assert client.get("/healthz").status_code == 200

    # It must stop reporting ready.
    response = client.get("/ready")
    assert response.status_code == 503
    assert response.json() == {"status": "not ready"}

    # Database operations return a safe, useful error.
    response = client.get("/tasks")
    assert response.status_code == 503
    assert response.json() == {
        "detail": "Database temporarily unavailable"
    }

    response = client.post("/tasks", json={"title": "Unavailable"})
    assert response.status_code == 503