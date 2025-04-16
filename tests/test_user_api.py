import pytest
from src.models.user import User

import uuid

def test_user_registration(client):
    unique_email = f"newuser_{uuid.uuid4()}@example.com"
    data = {
        "email": unique_email,
        "password": "password123",
        "first_name": "New",
        "last_name": "User"
    }
    response = client.post("/api/v1/auth/register", json=data)
    assert response.status_code == 201
    assert "api_key" in response.json
    assert response.json["user"]["email"] == data["email"]

import uuid

def test_user_login(client, test_user):
    data = {
        "email": test_user.email,
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

def test_get_users(client, test_user):
    headers = {"Authorization": test_user.api_key}
    response = client.get("/api/v1/users", headers=headers)
    assert response.status_code == 200
    assert any(user["email"] == test_user.email for user in response.json)
