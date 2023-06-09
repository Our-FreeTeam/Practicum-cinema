from http import HTTPStatus

from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


def test_create_template():
    body = {
        "event": "new_user",
        "instant_event": True,
        "title": "welcome",
        "text": "There is a template"
    }
    response = client.post("/api/v1/template/", json=body)
    assert response.status_code == HTTPStatus.OK
    body["id"] = 1
    assert response.json() == body

    response = client.post("/api/v1/template/", json=body)
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_change_template():
    body = {
        "event": "new_user",
        "instant_event": True,
        "title": "welcome",
        "text": "There is a new template"
    }
    response = client.put("/api/v1/template/new_user", json=body)
    assert response.status_code == HTTPStatus.OK
    body["id"] = 1
    assert response.json() == body
