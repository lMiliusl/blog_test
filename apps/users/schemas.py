from ninja import Schema
from typing import Optional

class UserRegisterSchema(Schema):
    username: str
    password: str
    email: Optional[str] = None
    first_name: Optional[str] = ''
    last_name: Optional[str] = ''


class UserLoginSchema(Schema):
    username: str
    password: str

class UserOutSchema(Schema):
    id: int
    username: str
    email: str
    first_name: str
    last_name: str
    token: Optional[str] = None
    registered_at: str

class TokenSchema(Schema):
    token: str
    user: UserOutSchema