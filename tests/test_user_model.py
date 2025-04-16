import pytest
import uuid
from src.models.user import User

import uuid

def test_user_creation(db):
    user = User(
        id=str(uuid.uuid4()),
        email=f"user_{uuid.uuid4()}@example.com",
        api_key=f"api_key_{uuid.uuid4()}",
        first_name="First",
        last_name="Last"
    )
    user.set_password("password123")
    db.session.add(user)
    db.session.commit()

    fetched_user = User.query.filter_by(email="user@example.com").first()
    assert fetched_user is not None
    assert fetched_user.email == "user@example.com"
    assert fetched_user.check_password("password123")
    assert not fetched_user.check_password("wrongpassword")

def test_user_email_validation():
    user = User(id=str(uuid.uuid4()), email="valid@example.com", api_key="key")
    user.set_password("password123")
    assert user.email == "valid@example.com"

    with pytest.raises(ValueError):
        user.email = "invalid-email"

def test_password_length_validation():
    user = User(id=str(uuid.uuid4()), email="test2@example.com", api_key="key")
    with pytest.raises(ValueError):
        user.set_password("short")

def test_to_dict_method():
    user = User(
        id=str(uuid.uuid4()),
        email="dict@example.com",
        api_key="key",
        first_name="First",
        last_name="Last"
    )
    user.set_password("password123")
    user_dict = user.to_dict()
    assert user_dict["email"] == "dict@example.com"
    assert "password_hash" not in user_dict
    assert "api_key" not in user_dict
