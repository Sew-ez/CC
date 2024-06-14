# SEWEZ BACKEND

## Specification

- Language: Python🐍
- Framework: FastAPI

## Documentation

### Authentication

#### [Login]

- URL : https://api.sewez.shop/auth/login
- Method : POST
- Request Body : email, password

[Logout]
URL : https://api.sewez.shop/auth/logout
Method : POST
Body : token

#### Register Endpoint

**URL:** `https://api.sewez.shop/auth/register`

**Method:** `POST`

**Body:**

- `name` (String)
- `email` (String) - Must be unique
- `password` (String) - Minimum of 8 characters long

**Example of request JSON:**

```json
{
  "name": "John Doe",
  "email": "email@example.com",
  "password": "securepassword"
}
```
