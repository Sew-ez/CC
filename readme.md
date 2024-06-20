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
<br>

### ORDER

### [ List Jenis Bahan ]

**URL:** `https://api.sewez.shop/order/jenis-bahan`

**Method:** `GET`

**Header:**

- `Authorization` (String) - Bearer

**Response Example:**

```json
{
    "error": false,
    "message": "Fabric type fetch successfully",
    "data": [
        {
            "id": 1,
            "type": "Combed 30s"
        },
        {
            "id": 2,
            "type": "Combed 24s"
        }
    ]
}
```

<br>

### [ List Color ]

**URL:** `https://api.sewez.shop/order/warna`

**Method:** `GET`

**Header:**

- `Authorization` (String) - Bearer

**Response Example:**

```json
{
    "error": false,
    "message": "Color fetch successfully",
    "data": [
        {
            "id": 1,
            "color": "Hitam",
            "hex": "FFFFFF"
        },
        {
            "id": 2,
            "color": "Putih",
            "hex": "000000"
        }
    ]
}
```

<br>