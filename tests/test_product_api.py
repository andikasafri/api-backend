import uuid
import pytest
from src.models.product import Product

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
    response = client.post("/api/v1/products", json=data, headers=headers)
    # Expecting 201 if created successfully
    assert response.status_code == 201, response.json
    assert response.json["name"] == data["name"]
    # Using approximate comparison for floating point values
    assert abs(float(response.json["price"]) - float(data["price"])) < 1e-6

def test_get_product(client, test_user, db):
    product = Product(
        id=str(uuid.uuid4()),
        name="Test Product",
        description="Test Description",
        price=99.99,
        user_id=test_user.id
    )
    with client.application.app_context():
        db.session.add(product)
        db.session.commit()  # Ensure the product is committed to the session
    product_id = product.id
    product_name = product.name
    response = client.get(f"/api/v1/products/{product_id}")
    assert response.status_code == 200
    assert response.json["name"] == product_name

def test_update_product(client, test_user, db):
    product = Product(
        id=str(uuid.uuid4()),
        name="Old Name",
        description="Old Description",
        price=50.0,
        user_id=test_user.id
    )
    with client.application.app_context():
        db.session.add(product)
        db.session.commit()  # Ensure the product is committed to the session

    headers = {"Authorization": test_user.api_key}
    data = {
        "name": "New Name",
        "description": "New Description",
        "price": 75.0
    }
    product_id = product.id
    response = client.put(f"/api/v1/products/{product_id}", json=data, headers=headers)
    assert response.status_code == 200, response.json
    assert response.json["name"] == data["name"]
    assert abs(float(response.json["price"]) - data["price"]) < 1e-6

def test_delete_product(client, test_user, db):
    product = Product(
        id=str(uuid.uuid4()),
        name="Delete Product",
        description="To be deleted",
        price=10.0,
        user_id=test_user.id
    )
    with client.application.app_context():
        db.session.add(product)
        db.session.commit()  # Ensure the product is committed to the session

    headers = {"Authorization": test_user.api_key}
    product_id = product.id
    response = client.delete(f"/api/v1/products/{product_id}", headers=headers)
    assert response.status_code == 200, response.json
    assert response.json["message"] == "Product deleted successfully"