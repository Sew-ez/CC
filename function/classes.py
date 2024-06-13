from pydantic import BaseModel
from typing import Dict

class registrationForm(BaseModel):
    profilename: str
    username:str
    password:str

class ukuran(BaseModel):
    s: int
    m: int

class orderForm(BaseModel):
    apikey: str
    jenisbahan: int
    warna: int
    ukuran: Dict[str, int]