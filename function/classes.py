from pydantic import BaseModel
from typing import Dict
from fastapi import UploadFile

class RegistrationForm(BaseModel):
    name:str
    email:str
    password:str

class LoginForm(BaseModel):
    email:str
    password:str

class LogoutForm(BaseModel):
    token:str

class Ukuran(BaseModel):
    s: int
    m: int

class CartForm(BaseModel):
    token: str
    product_type: int
    product_fabric: int
    product_color: int
    product_size: Dict[str, int]
    photo: UploadFile

class OrderForm(BaseModel):
    token: str
    cart: int