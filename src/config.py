import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
    
    # Security
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-key-please-change")
    
    # API
    JSON_SORT_KEYS = False
    
    # Development
    DEBUG = os.getenv("FLASK_DEBUG", "0") == "1"