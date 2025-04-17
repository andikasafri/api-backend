import json
import uuid
import pytest
from src.models.product import Product

BASE = "/api/v1"

@pytest.fixture
def product_payload():
    return {
        "name": "Integration Widget",
        "description": "Full-stack test",
        "price": 42.42
    }

def test_get_products_empty(client):
    resp = client.get(f"{BASE}/products")
    assert resp.status_code == 200
    data = resp.get_json()
    assert isinstance(data["products"], list)
    assert data["total"] == 0
    assert data["page"] == 1
    assert data["per_page"] == 20

def test_create_and_get_product(client, test_user, product_payload):
    headers = {"Authorization": f"Bearer {test_user.api_key}"}

    # CREATE
    resp = client.post(
        f"{BASE}/products",
        headers=headers,
        json=product_payload
    )
    assert resp.status_code == 201
    created = resp.get_json()
    assert created["name"] == product_payload["name"]
    assert created["price"] == product_payload["price"]
    pid = created["id"]

    # GET single
    resp2 = client.get(f"{BASE}/products/{pid}")
    assert resp2.status_code == 200
    fetched = resp2.get_json()
    assert fetched["id"] == pid
    assert fetched["description"] == product_payload["description"]

def test_unauthorized_create(client, product_payload):
    resp = client.post(f"{BASE}/products", json=product_payload)
    # your decorator should return 401 on missing/invalid token
    assert resp.status_code == 401

def test_update_product(client, test_user, product_payload, db):
    headers = {"Authorization": f"Bearer {test_user.api_key}"}
    # seed one via model
    prod = Product(
        id=str(uuid.uuid4()),
        name="ToBeUpdated",
        price=9.99,
        user_id=test_user.id
    )
    db.session.add(prod)
    db.session.commit()

    update_data = {"price": 19.99, "name": "Updated Name"}
    resp = client.put(
        f"{BASE}/products/{prod.id}",
        headers=headers,
        json=update_data
    )
    assert resp.status_code == 200
    body = resp.get_json()
    assert body["price"] == 19.99
    assert body["name"] == "Updated Name"

def test_delete_product(client, test_user, db):
    headers = {"Authorization": f"Bearer {test_user.api_key}"}
    # seed one via model
    prod = Product(
        id=str(uuid.uuid4()),
        name="ToBeDeleted",
        price=1.23,
        user_id=test_user.id
    )
    db.session.add(prod)
    db.session.commit()

    resp = client.delete(f"{BASE}/products/{prod.id}", headers=headers)
    assert resp.status_code == 200
    assert resp.get_json()["message"] == "Product deleted successfully"
    # ensure gone
    assert Product.query.get(prod.id) is None
