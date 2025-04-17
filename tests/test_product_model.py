import pytest
import uuid
from src.models.product import Product
from src.models.user import User

def test_product_creation(db, test_user):
    # create a product tied to the fixture user
    product = Product(
        id=str(uuid.uuid4()),
        name="Test Product",
        description="Test Description",
        price=10.99,
        user_id=test_user.id
    )
    db.session.add(product)
    db.session.commit()

    fetched = Product.query.filter_by(name="Test Product").first()
    assert fetched is not None
    assert fetched.price == 10.99
    assert fetched.user_id == test_user.id

def test_product_price_validation():
    # valid price stays as-is
    product = Product(
        id=str(uuid.uuid4()),
        name="Valid Product",
        price=5.0,
        user_id="some-user-id"
    )
    assert product.price == 5.0

    # negative price must raise
    with pytest.raises(ValueError):
        product.price = -1

def test_product_name_validation():
    # valid name stays as-is
    product = Product(
        id=str(uuid.uuid4()),
        name="Valid Name",
        price=1.0,
        user_id="some-user-id"
    )
    assert product.name == "Valid Name"

    # empty name must raise
    with pytest.raises(ValueError):
        product.name = ""

def test_to_dict_method():
    product = Product(
        id=str(uuid.uuid4()),
        name="Dict Product",
        description="Some description",
        price=20.0,
        user_id="some-user-id"
    )
    d = product.to_dict()
    assert d["id"] == product.id
    assert d["name"] == "Dict Product"
    assert isinstance(d["price"], float) and d["price"] == 20.0
    assert d["user_id"] == "some-user-id"
    # timestamps ISO formatted or None
    assert ("created_at" in d and "updated_at" in d)
