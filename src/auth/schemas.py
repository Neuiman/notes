from datetime import datetime

from pydantic import BaseModel, EmailStr

from src.auth.enums import Rights


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str

    class Config:
        from_attributes = True


class UserRegisterSchema(BaseModel):
    name: str
    email: EmailStr
    password: str
    status: Rights


class UserRegisterHashedSchema(BaseModel):
    name: str
    email: EmailStr
    hashed_password: str
    status: Rights


class UserSchema(BaseModel):
    id: int
    name: str
    email: EmailStr
    hashed_password: str
    created_at: datetime
    status: Rights


