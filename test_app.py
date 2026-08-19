import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200


def test_add_page(client):
    response = client.post("/add", data={"name": "Test Item"})
    assert response.status_code == 200
