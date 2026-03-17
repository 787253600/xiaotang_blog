"""认证 Pydantic 模式"""

from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    username: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserInfo(BaseModel):
    id: int
    username: str
    email: str

    model_config = {"from_attributes": True}


class ChangePasswordRequest(BaseModel):
    current_password: str = Field(..., min_length=1)
    new_password: str = Field(..., min_length=8, max_length=100)
