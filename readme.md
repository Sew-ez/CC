# SEWEZ BACKEND

## Specification

- Language: Python🐍
- Framework: FastAPI

## Documentation

### AUTHENTICATION

### [ Login Endpoint ]

**URL:** `https://api.sewez.shop/auth/login`

**Method:** `POST`

**Body:**

- `email` (String) - Must be unique
- `password` (String) - Minimum of 8 characters long
  **Request Example:**

```json
{
  "email": "email@example.com",
  "password": "securepassword"
}
```

**Response Example:**

```json
{
  "error": false,
  "message": "Success",
  "loginResult": {
    "userId": 1,
    "name": "John Doe",
    "token": "17f80f81-319f-41b5-b2fa-a1fa69d8b849"
  }
}
```

<br>

### [ Logout Endpoint ]

**URL:** `https://api.sewez.shop/auth/logout`

**Method:** `POST`

**Body:**

- `token` (String)
  **Request Example:**

```json
{
  "token": "17f80f81-319f-41b5-b2fa-a1fa69d8b849"
}
```

**Response Example:**

```json
{
  "error": false,
  "message": "Successfully logged out"
}
```

<br>

### [ Register Endpoint ]

**URL:** `https://api.sewez.shop/auth/register`

**Method:** `POST`

**Body:**

- `name` (String)
- `email` (String) - Must be unique
- `password` (String) - Minimum of 8 characters long

**Request Example:**

```json
{
  "name": "John Doe",
  "email": "email@example.com",
  "password": "securepassword"
}
```

**Response Example:**

```json
{
  "error": false,
  "message": "Successfully registered"
}
```
