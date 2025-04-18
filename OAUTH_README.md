# OAuth Implementation Guide

This guide explains how to set up and use OAuth authentication in the Sustainable Market Backend API.

## Setup Instructions

1. Create Google OAuth Credentials:
   - Go to [Google Cloud Console](https://console.cloud.google.com)
   - Create a new project or select existing one
   - Enable the Google+ API
   - Go to Credentials
   - Create OAuth 2.0 Client ID
   - Add authorized redirect URIs:
     - Development: `http://localhost:5000/api/v1/auth/login/google/callback`
     - Production: `https://your-domain.com/api/v1/auth/login/google/callback`

2. Update Environment Variables:
   ```
   OAUTH_GOOGLE_CLIENT_ID=your_client_id
   OAUTH_GOOGLE_CLIENT_SECRET=your_client_secret
   ```

## Testing OAuth Flow

1. Frontend Implementation:
   ```javascript
   // Redirect to Google login
   window.location.href = '/api/v1/auth/login/google';
   ```

2. Backend Flow:
   - User clicks login button → Redirected to Google
   - Google authenticates → Redirects to callback URL
   - Backend creates/updates user → Returns JWT token
   - Frontend stores token for future requests

3. Using the Token:
   ```javascript
   // Add to all API requests
   headers: {
     'Authorization': `Bearer ${token}`
   }
   ```

## Security Considerations

1. Token Storage:
   - Store JWT in HttpOnly cookies
   - Never store in localStorage
   - Use secure and SameSite flags

2. CSRF Protection:
   - Implemented automatically by Flask
   - Use state parameter in OAuth flow

3. Scope Limitations:
   - Only request necessary permissions
   - Currently using: email, profile

## Testing

1. Manual Testing:
   ```bash
   # Start the server
   python main.py
   
   # Visit in browser
   http://localhost:5000/api/v1/auth/login/google
   ```

2. Automated Tests:
   ```python
   def test_google_oauth_flow(client):
       # Mock OAuth response
       response = client.get('/api/v1/auth/login/google/callback')
       assert response.status_code == 200
       assert 'token' in response.json
   ```

## Troubleshooting

1. Common Issues:
   - Invalid redirect URI
   - Missing environment variables
   - CORS issues with frontend

2. Debug Logs:
   - Check application logs
   - Enable OAuth debug mode
   - Verify Google Console settings

## Best Practices

1. Error Handling:
   - Graceful fallbacks
   - Clear error messages
   - Proper logging

2. User Experience:
   - Smooth login flow
   - Clear success/error states
   - Proper redirect handling

3. Security:
   - Regular token rotation
   - Proper scope usage
   - Secure storage practices