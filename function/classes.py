from pydantic import BaseModel
from typing import Dict

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

class OrderForm(BaseModel):
    apikey: str
    jenisbahan: int
    warna: int
    ukuran: Dict[str, int]