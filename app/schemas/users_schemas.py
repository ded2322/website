from pydantic import BaseModel, EmailStr
from typing import Optional


class SUserAuth(BaseModel):
    username: str
    password: str
    email: Optional[EmailStr] = None


class SUserLogin(BaseModel):
    username: str
    password: str


class SUserUpdateData(BaseModel):
    user: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
