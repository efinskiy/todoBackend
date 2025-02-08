from datetime import timedelta

from fastapi.params import Security
from fastapi_jwt import JwtAuthorizationCredentials, JwtAccessBearer, JwtRefreshBearer
from passlib.context import CryptContext

from app.config import config
from app.entities.auth import AuthManagerData

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
access_security = JwtAccessBearer(
    secret_key=config.JWT_SECRET_KEY,
    auto_error=True,
    access_expires_delta=timedelta(days=1),
)
refresh_security = JwtRefreshBearer(secret_key=config.JWT_SECRET_KEY, auto_error=True)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


class AuthManager:
    def __init__(self): ...

    async def __call__(
        self, auth: JwtAuthorizationCredentials = Security(access_security)
    ) -> AuthManagerData:
        user_id = int(auth["user_id"])

        return AuthManagerData(user_id=user_id)
