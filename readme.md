# SEWEZ BACKEND

## Specification

- Language: Python🐍
- Framework: FastAPI

## Documentation

### AUTHENTICATION

<br>

### [ Login Endpoint ]

**URL:** `https://api.sewez.shop/auth/login`

**Method:** `POST`

**Body:**

- `email` (String) - Must be unique
- `password` (String) - Minimum of 8 characters long 

<br>

### [ Logout Endpoint ]

**URL:** `https://api.sewez.shop/auth/logout`

**Method:** `POST`

**Body:**

- `token` (String) 

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
