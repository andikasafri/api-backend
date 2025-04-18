# Manual Testing Guide for Sustainable Market API

This guide provides step-by-step instructions for testing all API endpoints and features.

## Prerequisites

1. Install required tools:
   - cURL or Postman for API testing
   - Web browser for OAuth testing

2. Set up environment variables in `.env`:
```
SUPABASE_URL=your_supabase_url
SECRET_KEY=your_secret_key
FLASK_DEBUG=1
OAUTH_GOOGLE_CLIENT_ID=your_google_client_id
OAUTH_GOOGLE_CLIENT_SECRET=your_google_client_secret
```

3. Start the server:
```bash
python main.py
```

## 1. Authentication Testing

### 1.1 Regular Registration and Login

1. Register a new user:
```bash
curl -X POST http://localhost:5000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123",
    "first_name": "Test",
    "last_name": "User"
  }'
```

Expected response:
```json
{
  "message": "User registered successfully",
  "user": {
    "email": "test@example.com",
    "first_name": "Test",
    "last_name": "User",
    "role": "user"
  },
  "api_key": "your_api_key"
}
```

2. Login with credentials:
```bash
curl -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'
```

### 1.2 OAuth Authentication

1. Start OAuth Flow:
   - Open in browser: `http://localhost:5000/api/v1/auth/login/google`
   - Complete Google login
   - Note the returned JWT token

2. Test OAuth Callback:
   - Callback URL will be: `http://localhost:5000/api/v1/auth/login/google/callback`
   - Should receive JWT token and user info

3. Use OAuth Token:
```bash
curl http://localhost:5000/api/v1/profile \
  -H "Authorization: Bearer YOUR_OAUTH_TOKEN"
```

## 2. User Management

### 2.1 Profile Operations

1. Get Profile:
```bash
curl http://localhost:5000/api/v1/profile \
  -H "Authorization: Bearer YOUR_TOKEN"
```

2. Update Profile:
```bash
curl -X PUT http://localhost:5000/api/v1/profile \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Updated",
    "last_name": "Name"
  }'
```

### 2.2 Role-Based Access

1. Test Admin Access:
```bash
# Only works with admin token
curl http://localhost:5000/api/v1/users \
  -H "Authorization: Bearer ADMIN_TOKEN"
```

2. Test Seller Access:
```bash
# Works with seller or admin token
curl http://localhost:5000/api/v1/products \
  -H "Authorization: Bearer SELLER_TOKEN"
```

## 3. Product Management

### 3.1 Create Product (Seller/Admin only)
```bash
curl -X POST http://localhost:5000/api/v1/products \
  -H "Authorization: Bearer SELLER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Product",
    "description": "Test Description",
    "price": 99.99
  }'
```

### 3.2 Get Products
```bash
# Public endpoint
curl http://localhost:5000/api/v1/products

# Filter by user
curl "http://localhost:5000/api/v1/products?user_only=true" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 3.3 Update Product (Owner only)
```bash
curl -X PUT http://localhost:5000/api/v1/products/PRODUCT_ID \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "price": 199.99
  }'
```

### 3.4 Delete Product (Owner only)
```bash
curl -X DELETE http://localhost:5000/api/v1/products/PRODUCT_ID \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## 4. Transaction Management

### 4.1 Create Transaction
```bash
curl -X POST http://localhost:5000/api/v1/transactions \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "items": [
      {
        "product_id": "PRODUCT_ID",
        "quantity": 2
      }
    ]
  }'
```

### 4.2 Get Transactions
```bash
curl http://localhost:5000/api/v1/transactions \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 4.3 Update Transaction Status
```bash
curl -X PUT http://localhost:5000/api/v1/transactions/TRANSACTION_ID/status \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "completed"
  }'
```

## Testing Checklist

### Authentication
- [ ] Regular user registration
- [ ] User login with credentials
- [ ] OAuth Google login
- [ ] OAuth callback handling
- [ ] Token validation
- [ ] API key authentication

### User Management
- [ ] Profile retrieval
- [ ] Profile updates
- [ ] Role-based access control
- [ ] Admin access to user list
- [ ] Seller privileges

### Product Management
- [ ] Product creation (seller/admin)
- [ ] Product listing (public)
- [ ] Product filtering by user
- [ ] Product updates (owner only)
- [ ] Product deletion (owner only)

### Transaction Management
- [ ] Transaction creation
- [ ] Transaction listing
- [ ] Transaction status updates
- [ ] Transaction validation

### Error Handling
- [ ] Invalid credentials
- [ ] Missing tokens
- [ ] Insufficient permissions
- [ ] Invalid input data
- [ ] Resource not found
- [ ] Rate limiting

## Common HTTP Status Codes

- 200: Success
- 201: Created
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 429: Too Many Requests
- 500: Internal Server Error

## Testing Tips

1. Save tokens and IDs from responses for subsequent requests
2. Test both successful and error cases
3. Verify role-based access control
4. Check validation error messages
5. Test pagination and filtering
6. Verify data persistence
7. Test rate limiting
8. Check error handling