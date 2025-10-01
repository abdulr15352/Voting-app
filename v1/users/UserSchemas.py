from pydantic import BaseModel, EmailStr, SecretStr
from typing import Optional

class UserSchema(BaseModel):
    name: str
    email: EmailStr
    password: SecretStr
    hashed_password: Optional[str] = None
    is_active: bool = True

class UserLoginSchema(BaseModel):
    email: EmailStr
    password: SecretStr