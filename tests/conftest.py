# conftest.py
import sys
import os
import uuid
import pytest
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

# Adjust sys.path so that tests can import from the src folder
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(BASE_DIR, 'src'))
sys.path.insert(0, BASE_DIR)

from src import create_app
from src.extensions import db as _db
from src.models.user import User

# -------------------------------------------------------------------
# Fixture for creating the Flask app. This fixture is session-scoped
# so the database is created just once per testing session.
# -------------------------------------------------------------------
@pytest.fixture(scope="session")
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    })
    with app.app_context():
        _db.create_all()
        yield app
        _db.drop_all()

# -------------------------------------------------------------------
# Fixture for managing the database session. This fixture is function-scoped,
# opening a nested transaction that is rolled back after each test for isolation.
# -------------------------------------------------------------------
@pytest.fixture(scope="function")
def db(app):
    with app.app_context():
        # Begin a nested transaction
        _db.session.begin_nested()
        yield _db
        _db.session.rollback()
        _db.session.remove()

# -------------------------------------------------------------------
# Fixture to provide a test client which you can use to simulate requests.
# -------------------------------------------------------------------
@pytest.fixture(scope="function")
def client(app):
    return app.test_client()

# -------------------------------------------------------------------
# Fixture for creating a test user. It uses the "db" fixture to ensure the database
# changes are rolled back after the test.
# -------------------------------------------------------------------
@pytest.fixture(scope='function')
def test_user(app, db):
    with app.app_context():
        # Generate a unique email using uuid4
        unique_email = f"test_{uuid.uuid4()}@example.com"
        user = User(
            id=str(uuid.uuid4()),
            email=unique_email,
            api_key=f"test_api_key_{uuid.uuid4()}",
            first_name="Test",
            last_name="User"
        )
        user.set_password("password123")
        db.session.add(user)
        db.session.commit()
        yield user
        # Rollback is handled by the db fixture after the test ends.
