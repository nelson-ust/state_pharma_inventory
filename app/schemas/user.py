# Placeholder for app/schemas/user.py
# app/schemas/user.py

from pydantic import BaseModel
from typing import Optional

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class User(BaseModel):
    username: str
    email: Optional[str] = None
    is_active: bool

    class Config:
        orm_mode = True
