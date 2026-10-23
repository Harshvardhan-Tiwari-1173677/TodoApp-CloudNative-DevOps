
import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 500
    assert response.get_json()["status"] == "healthy"


def test_get_tasks_returns_list(client):
    response = client.get("/tasks")
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)


def test_add_task(client):
    response = client.post("/tasks", json={"title": "CI test task"})
    assert response.status_code == 201
    assert response.get_json()["title"] == "CI test task"


def test_add_task_rejects_empty_title(client):
    response = client.post("/tasks", json={"title": "   "})
    assert response.status_code == 400


def test_delete_missing_task(client):
    response = client.delete("/tasks/999999")
    assert response.status_code == 404
