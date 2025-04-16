# tests/test_supabase.py
import uuid
import pytest
from src.models.user import User

try:
    from src.utils.supabase import supabase
except ImportError:
    supabase = None

@pytest.mark.skipif(supabase is None, reason="Supabase client not available")
def test_supabase_connection(app, db):
    with app.app_context():
        # Create a unique test user for each test run
        uid = str(uuid.uuid4())
        test_user = User(
            id=uid,
            email=f"test_{uid}@example.com",
            api_key=f"api_{uid}"
        )
        db.session.add(test_user)
        db.session.commit()
        
        # This assumes the supabase client is configured to talk to the same actual DB.
        data = supabase.table("users").select("*").eq("id", test_user.id).execute()
        # Verify that the returned data contains the new test user
        assert any(item["id"] == test_user.id for item in data.data)
