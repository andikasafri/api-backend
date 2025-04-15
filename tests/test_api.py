import pytest
import uuid
from src import create_app
from src.models.user import User
from src.models.product import Product
from src.extensions import db as _db

@pytest.fixture(scope='session')
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"
    })
    
    with app.app_context():
        _db.create_all()
        yield app
        _db.drop_all()

@pytest.fixture(scope='function')
def client(app):
    return app.test_client()

@pytest.fixture(scope='function')
def test_user(app):
    with app.app_context():
        user = User(
            id=str(uuid.uuid4()),
            email="test@example.com",
            api_key="test_api_key_123",
            first_name="Test",
            last_name="User"
        )
        user.set_password("password123")
        _db.session.add(user)
        _db.session.commit()
        return user

def test_health_check(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json == {"status": "Healthy", "version": "1.0"}

def test_user_registration(client):
    data = {
        "email": "new@example.com",
        "password": "password123",
        "first_name": "New",
        "last_name": "User"
    }
    response = client.post("/api/v1/auth/register", json=data)
    assert response.status_code == 201
    assert "api_key" in response.json
    assert response.json["user"]["email"] == data["email"]

def test_user_login(client, test_user):
    data = {
        "email": "test@example.com",
        "password": "password123"
    }
    response = client.post("/api/v1/auth/login", json=data)
    assert response.status_code == 200
    assert "api_key" in response.json
    assert response.json["user"]["email"] == test_user.email

def test_get_profile(client, test_user):
    headers = {"Authorization": test_user.api_key}
    response = client.get("/api/v1/profile", headers=headers)
    assert response.status_code == 200
    assert response.json["email"] == test_user.email

def test_update_profile(client, test_user):
    headers = {"Authorization": test_user.api_key}
    data = {
        "first_name": "Updated",
        "last_name": "Name"
    }
    response = client.put("/api/v1/profile", json=data, headers=headers)
    assert response.status_code == 200
    assert response.json["first_name"] == data["first_name"]
    assert response.json["last_name"] == data["last_name"]

def test_get_products(client):
    response = client.get("/api/v1/products")
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_create_product(client, test_user):
    headers = {"Authorization": test_user.api_key}
    data = {
        "name": "Test Product",
        "description": "Test Description",
        "price": 99.99
    }
    
    response = client.post("/api/v1/products", 
                         json=data,
                         headers=headers)
    
    assert response.status_code == 201
    assert response.json["name"] == data["name"]
    assert response.json["price"] == data["price"]

def test_get_product(client, test_user):
    # First create a product
    product = Product(
        id=str(uuid.uuid4()),
        name="Test Product",
        description="Test Description",
        price=99.99,
        user_id=test_user.id
    )
    
    with client.application.app_context():
        _db.session.add(product)
        _db.session.commit()
        
        response = client.get(f"/api/v1/products/{product.id}")
        assert response.status_code == 200
        assert response.json["name"] == product.name