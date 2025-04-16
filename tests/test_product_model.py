import pytest
import uuid
from src.models.product import Product
from src.models.user import User

import uuid

def test_product_creation(db):
    from src.models.user import User
    from src.models.product import Product
    import uuid

    user = User(
        id=str(uuid.uuid4()),
        email=f"owner_{uuid.uuid4()}@example.com",
        api_key=f"api_key_{uuid.uuid4()}"
    )
    user.set_password("password123")
    db.session.add(user)
    db.session.commit()

    # Fetch user again to ensure committed
    fetched_user = User.query.filter_by(email="owner@example.com").first()
    assert fetched_user is not None

    product = Product(
        id=str(uuid.uuid4()),
        name="Test Product",
        description="Test Description",
        price=10.99,
        user_id=fetched_user.id
    )
    db.session.add(product)
    db.session.commit()

    fetched_product = Product.query.filter_by(name="Test Product").first()
    assert fetched_product is not None
    assert fetched_product.price == 10.99
    assert fetched_product.user_id == fetched_user.id

def test_product_price_validation():
    product = Product(id=str(uuid.uuid4()), name="Valid Product", price=5.0, user_id="user_id")
    assert product.price == 5.0

    with pytest.raises(ValueError):
        product.price = -1

def test_product_name_validation():
    product = Product(id=str(uuid.uuid4()), name="Valid Name", price=1.0, user_id="user_id")
    assert product.name == "Valid Name"

    with pytest.raises(ValueError):
        product.name = ""

def test_to_dict_method():
    product = Product(
        id=str(uuid.uuid4()),
        name="Dict Product",
        description="Description",
        price=20.0,
        user_id="user_id"
    )
    product_dict = product.to_dict()
    assert product_dict["name"] == "Dict Product"
    assert product_dict["price"] == 20.0
    assert product_dict["user_id"] == "user_id"
