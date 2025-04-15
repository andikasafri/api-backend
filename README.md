# Sustainable Market Backend API

A Flask-based REST API backend for the Sustainable Market platform, featuring user authentication, product management, and Supabase integration.

## Features

- User Authentication (Register, Login, Profile Management)
- Product Management (CRUD operations)
- Supabase Database Integration
- API Key Authentication
- Comprehensive Test Suite
- Docker Support

## Project Structure

```
├── migrations/              # Database migrations
│   ├── versions/           # Migration version files
│   ├── env.py             # Migration environment configuration
│   └── alembic.ini        # Alembic configuration
├── src/                    # Source code
│   ├── api/               # API endpoints
│   │   └── v1/           # API version 1
│   ├── models/           # Database models
│   ├── utils/            # Utility functions
│   ├── __init__.py       # Application factory
│   ├── config.py         # Configuration
│   └── extensions.py     # Flask extensions
├── tests/                 # Test suite
├── .env                   # Environment variables
├── Dockerfile            # Docker configuration
└── pyproject.toml        # Project dependencies
```

## Prerequisites

- Python 3.11+
- UV package manager
- Supabase account and database

## Environment Variables

Create a `.env` file in the root directory with:

```
SUPABASE_URL=your-supabase-url
SECRET_KEY=your-secret-key
```

## Local Development Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   uv sync
   ```

3. Initialize the database:
   ```bash
   flask db upgrade
   ```

4. Run the development server:
   ```bash
   flask run
   ```

## API Endpoints

### Authentication
- POST `/api/v1/auth/register` - Register new user
- POST `/api/v1/auth/login` - User login

### Users
- GET `/api/v1/users` - List all users (requires authentication)
- GET `/api/v1/users/<user_id>` - Get specific user
- GET `/api/v1/profile` - Get current user profile
- PUT `/api/v1/profile` - Update current user profile

### Products
- GET `/api/v1/products` - List all products
- POST `/api/v1/products` - Create new product (requires authentication)
- GET `/api/v1/products/<product_id>` - Get specific product

## Testing

Run tests using pytest:
```bash
pytest
```

## Docker Support

Build the Docker image:
```bash
docker build -t sustainable-market-backend .
```

Run the container:
```bash
docker run -p 8000:8000 sustainable-market-backend
```