from pydantic import BaseModel, Field


class UserAuthScheme(BaseModel):
    username: str = Field(..., min_length=3)
    password: str = Field(..., min_length=5)


class JWTAuthScheme(BaseModel):
    access_token: str
    expires: int


class AuthManagerData(BaseModel):
    user_id: int
