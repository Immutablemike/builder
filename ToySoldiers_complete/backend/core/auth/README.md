# Auth Service

Authentication and authorization service for the Toy Soldiers platform.

## Features

- User signup with email/password
- Login and JWT token management
- Profile management
- Role-based access control (Creator, Fan, Admin)
- Supabase Auth integration
- PostHog analytics tracking

## Endpoints

### POST /auth/signup
Create a new user account.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123",
  "role": "creator"
}
```

**Response:**
```json
{
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "role": "creator",
    "created_at": "2024-01-01T00:00:00Z"
  },
  "message": "Account created successfully"
}
```

### POST /auth/login
Authenticate user and get access tokens.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response:**
```json
{
  "access_token": "jwt_token",
  "refresh_token": "refresh_token",
  "user": { ... },
  "message": "Login successful"
}
```

### GET /auth/profile
Get current user profile (requires authentication).

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response:**
```json
{
  "id": "uuid",
  "email": "user@example.com",
  "role": "creator",
  "created_at": "2024-01-01T00:00:00Z",
  "creator_profile": { ... }
}
```

## Running Tests

```bash
pytest
```

## Environment Variables

- `SUPABASE_URL`: Supabase project URL
- `SUPABASE_SERVICE_ROLE_KEY`: Supabase service role key
- `JWT_SECRET_KEY`: Secret key for JWT signing
- `POSTHOG_API_KEY`: PostHog project API key
