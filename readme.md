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

### [ List Jenis Bahan Logo ]

**URL:** `https://api.sewez.shop/order/jenis-bahan-logo`

**Method:** `GET`

**Header:**

- `Authorization` (String) - Bearer

**Response Example:**

```json
{
    "error": false,
    "message": "Logo type fetch successfully",
    "data": [
        {
            "id": 1,
            "type": "DTF"
        },
        {
            "id": 2,
            "type": "Rubber"
        },
        {
            "id": 3,
            "type": "Plastisol"
        }
    ]
}
```

<br>

### [ Push Order ]

**URL:** `https://api.sewez.shop/order/submit`

**Method:** `POST`

**Header:**

- `Authorization` (String) - Bearer

**Body (form-data):**

- `jenisproduk` (int) - id of product (1: tshirt, 2: jacket, 3:Tote - Bag)
- `jenisbahan` (int) - id from jenis-bahan api
- `warna` (int) - id from warna api
- `jenislogo` (int) - id of jenis-bahan-logo api
- `s` (int) - number of S-size order
- `m` (int) - number of S-size order
- `l` (int) - number of S-size order
- `xl` (int) - number of S-size order
- `xxl` (int) - number of S-size order
- `image` (file) - mockup image, must be type image/jpeg

**Response Example:**

```json
{
    "error": false,
    "message": "Order added successfully",
    "data": {
        "jenisbahan": "Combed 30s",
        "warna": "Hitam",
        "jenislogo": "DTF",
        "xxl": 0,
        "xl": 100,
        "l": 120,
        "m": 30,
        "s": 57,
        "image": "https://{host}/{PATH}/image.jpg"
    }
}
```