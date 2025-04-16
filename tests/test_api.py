# import uuid
# import pytest
# from src.models.user import User
# from src.models.product import Product

# def test_health_check(client):
#     response = client.get("/")
#     assert response.status_code == 200
#     assert response.json["status"] == "Healthy"
#     assert "version" in response.json

# def test_user_registration(client):
#     data = {
#         "email": "new@example.com",
#         "password": "password123",
#         "first_name": "New",
#         "last_name": "User"
#     }
#     response = client.post("/api/v1/auth/register", json=data)
#     assert response.status_code == 201
#     assert "api_key" in response.json
#     assert response.json["user"]["email"] == data["email"]

# def test_user_login(client, test_user):
#     data = {
#         "email": "test@example.com",
#         "password": "password123"
#     }
#     response = client.post("/api/v1/auth/login", json=data)
#     assert response.status_code == 200
#     assert "api_key" in response.json
#     assert response.json["user"]["email"] == test_user.email

# def test_get_profile(client, test_user):
#     headers = {"Authorization": test_user.api_key}
#     response = client.get("/api/v1/profile", headers=headers)
#     assert response.status_code == 200
#     assert response.json["email"] == test_user.email

# def test_update_profile(client, test_user):
#     headers = {"Authorization": test_user.api_key}
#     data = {
#         "first_name": "Updated",
#         "last_name": "Name"
#     }
#     response = client.put("/api/v1/profile", json=data, headers=headers)
#     assert response.status_code == 200
#     assert response.json["first_name"] == data["first_name"]
#     assert response.json["last_name"] == data["last_name"]

# def test_get_products(client):
#     response = client.get("/api/v1/products")
#     assert response.status_code == 200
#     assert isinstance(response.json, list)

# def test_create_product(client, test_user):
#     headers = {"Authorization": test_user.api_key}
#     data = {
#         "name": "Test Product",
#         "description": "Test Description",
#         "price": 99.99
#     }
#     response = client.post("/api/v1/products", json=data, headers=headers)
#     assert response.status_code == 201
#     assert response.json["name"] == data["name"]
#     # Use approximate comparison for floating point values
#     assert abs(float(response.json["price"]) - float(data["price"])) < 1e-6

# def test_get_product(client, test_user, db):
#     # Create product directly in the database
#     product = Product(
#         id=str(uuid.uuid4()),
#         name="Test Product",
#         description="Test Description",
#         price=99.99,
#         user_id=test_user.id
#     )
#     with client.application.app_context():
#         db.session.add(product)
#         db.session.commit()

#     response = client.get(f"/api/v1/products/{product.id}")
#     assert response.status_code == 200
#     assert response.json["name"] == product.name
