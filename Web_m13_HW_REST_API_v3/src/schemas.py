from datetime import datetime, date
from pydantic import BaseModel, EmailStr, Field

from src.database.models import Role


class ClientModel(BaseModel):
    # first_name: str = Field(default="test_f_n")
    first_name: str
    last_name: str
    email: EmailStr
    mobile: str
    birthday: date
    add_info: str


class ClientResponse(BaseModel):
    id: int = 1
    first_name: str
    last_name: str
    email: EmailStr
    mobile: str
    birthday: date
    add_info: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class UserModel(BaseModel):
    username: str = Field(min_length=6, max_length=12)
    email: EmailStr
    password: str = Field(min_length=6, max_length=8)


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    avatar: str
    roles: Role

    class Config:
        orm_mode = True


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RequestEmail(BaseModel):
    email: EmailStr
