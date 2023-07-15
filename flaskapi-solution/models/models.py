from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, validator


def check_password(password: str) -> str:
    if len(password) < 6:
        raise ValueError('Password length must be 6 or more symbols')
    return password


class OnlyLogin(BaseModel):
    user: str


class Login(BaseModel):
    user: str
    password: str

    _validate_password = validator('password', allow_reuse=True)(check_password)


class RegInfo(Login):
    email: EmailStr
    timezone: str


class Token(BaseModel):
    access_token: str
    refresh_token: str


class Session(BaseModel):
    id: str
    time_start: datetime
    ip_address: str


class Role(BaseModel):
    role_name: str


class RoleId(Role):
    id: str


class RoleList(BaseModel):
    roles: list[RoleId]


class RoleIds(BaseModel):
    result: list[RoleId]


class UserRole(BaseModel):
    user_name: str
    role_name: str


class UserIdRole(BaseModel):
    user_id: UUID
    role_name: str


class SessionList(BaseModel):
    sessions: list[Session]


class RoleCheck(BaseModel):
    roles: list[str]


class UserId(BaseModel):
    user_id: str


class BoolResponse(BaseModel):
    result: bool


class StrResponse(BaseModel):
    result: str


class SimpleList(BaseModel):
    roles_list: list


class TokensResp(BoolResponse):
    access_token: str = ""
    refresh_token: str = ""


class ErrorStr(BaseModel):
    error: str = ""
