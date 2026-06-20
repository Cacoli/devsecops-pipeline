import pytest
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_health(client):
    res = client.get("/health")
    assert res.status_code == 200

def test_get_users(client):
    res = client.get("/users")
    assert res.status_code == 200

def test_login(client):
    res = client.post("/login", json={"username": "Alice"})
    assert res.status_code == 200

def test_login_no_username(client):
    res = client.post("/login", json={})
    assert res.status_code == 400