# Sustainable Market Backend API

A Flask-based REST API backend for the Sustainable Market platform, featuring user authentication, product management, transaction processing, and Supabase integration.

## Features

- User Authentication
  - OAuth Integration
  - JWT Token Support
  - API Key Authentication
  - Profile Management
- Product Management (CRUD operations)
- Transaction Processing
  - Order Creation
  - Payment Status Tracking
  - Order History
- Security Features
  - Rate Limiting
  - CORS Protection
  - Content Security Policy
  - HTTPS Enforcement
  - Request Logging
  - Error Tracking
- Performance Optimizations
  - Response Compression
  - Database Connection Pooling
- Supabase Database Integration
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
│   ├── middleware/       # Application middleware
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
FLASK_DEBUG=1
OAUTH_GOOGLE_CLIENT_ID=your-google-client-id
OAUTH_GOOGLE_CLIENT_SECRET=your-google-client-secret
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
   python main.py
   ```

## API Endpoints

### Authentication

- POST `/api/v1/auth/register` - Register new user
- POST `/api/v1/auth/login` - User login
- POST `/api/v1/auth/oauth/google` - Google OAuth login

### Users

- GET `/api/v1/users` - List all users (requires authentication)
- GET `/api/v1/users/<user_id>` - Get specific user
- GET `/api/v1/profile` - Get current user profile
- PUT `/api/v1/profile` - Update current user profile

### Products

- GET `/api/v1/products` - List all products
- POST `/api/v1/products` - Create new product (requires authentication)
- GET `/api/v1/products/<product_id>` - Get specific product
- PUT `/api/v1/products/<product_id>` - Update product
- DELETE `/api/v1/products/<product_id>` - Delete product

### Transactions

- GET `/api/v1/transactions` - List user's transactions
- POST `/api/v1/transactions` - Create new transaction
- GET `/api/v1/transactions/<transaction_id>` - Get specific transaction
- PUT `/api/v1/transactions/<transaction_id>/status` - Update transaction status

## Design Considerations

1. Authentication Strategy
   - Multiple authentication methods (JWT, API keys, OAuth)
   - JWT for web clients
   - API keys for service-to-service communication
   - OAuth support for social login
   - Secure session management

2. Security Implementation
   - Rate limiting to prevent abuse
   - Content Security Policy (CSP)
   - HTTPS enforcement
   - Secure cookie configuration
   - Request logging and monitoring
   - Comprehensive error handling

3. Database Schema
   - Normalized design with proper relationships
   - UUID for distributed system compatibility
   - Soft deletion support
   - Optimized indexes

4. API Design
   - RESTful architecture
   - Consistent error responses
   - Request validation
   - Pagination support
   - Comprehensive documentation

5. Performance Optimization
   - Response compression
   - Database connection pooling
   - Efficient query design
   - Caching headers

## Testing

Run tests using pytest:

```bash
pytest
```

For coverage report:

```bash
pytest --cov=src
```

## Docker Support

Build the Docker image:

```bash
docker build -t sustainable-market-backend .
```

Run the container:

```bash
docker run -p 8000:5000 sustainable-market-backend
```

Note: The Flask app runs on port 5000 inside the container, mapped to 8000 on the host.