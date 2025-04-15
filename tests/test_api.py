import pytest
from src import create_app
from src.models.user import User
from src.extensions import db as _db

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

@pytest.fixture(scope='session')
def app():
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"  # Use in-memory DB for tests
    with app.app_context():
        _db.create_all()
        yield app
    _db.drop_all()

@pytest.fixture(scope='function')
def client(app):
    return app.test_client()

def test_health_check(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json == {"status": "Healthy", "version": "1.0"}

def test_protected_route_without_token(client):
    response = client.get("/api/v1/users")
    assert response.status_code == 401
    assert response.json["error"] == "Missing token"

def test_protected_route_with_invalid_token(client):
    headers = {"Authorization": "Bearer invalid-token"}
    response = client.get("/api/v1/users", headers=headers)
    assert response.status_code == 401
    assert response.json["error"] == "Invalid token"