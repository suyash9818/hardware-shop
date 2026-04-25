# API Auth Examples (JWT + Token)

## JWT (recommended)
### Obtain token
POST /api/auth/token/
Content-Type: application/json

{
  "username": "test",
  "password": "YOUR_PASSWORD"
}

### Refresh token
POST /api/auth/token/refresh/
Content-Type: application/json

{
  "refresh": "REFRESH_TOKEN"
}

### Call an authenticated endpoint
GET /api/auth/me/
Authorization: Bearer ACCESS_TOKEN

## DRF Token (optional)
POST /api/auth/token-auth/
Content-Type: application/x-www-form-urlencoded

username=test&password=YOUR_PASSWORD
