# tests/test_supabase.py
import pytest
from src import create_app
from src.models.user import User
from src.extensions import db as _db

def test_supabase_connection(app):
    with app.app_context():
        # Insert a test user
        test_user = User(email="test@example.com", api_key="test123")
        _db.session.add(test_user)
        _db.session.commit()
        
        # Fetch user via Supabase client
        data = supabase.table("users").select("*").eq("id", test_user.id).execute()
        assert len(data.data) == 1