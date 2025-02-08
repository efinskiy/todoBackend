from datetime import timedelta
import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.db import get_session
from app.entities.auth import UserAuthScheme, JWTAuthScheme, AuthManagerData
from app.entities.common import MessageResponseSchema
from app.models import User
from app.utils.auth import (
    get_password_hash,
    verify_password,
    access_security,
)

router = APIRouter(prefix="/auth", tags=["Authentication"])


# Регистрация пользователя
@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=MessageResponseSchema,
)
async def register_user(
    user: UserAuthScheme, session: AsyncSession = Depends(get_session)
):
    user_check = await session.scalar(
        select(User).where(User.username == user.username)
    )
    # Если пользователь уже существует, возвращаем 400 ошибку
    if user_check:
        raise HTTPException(
            status_code=400, detail="Пользователь с таким именем уже существует"
        )

    # Создаем нового пользователя
    user = User(
        username=user.username, password_hashed=get_password_hash(user.password)
    )

    session.add(user)
    await session.commit()
    return {"msg": "Пользователь успешно зарегистрирован"}


# Авторизация пользователя
@router.post("/login", response_model=JWTAuthScheme)
async def login_user(
    login_data: UserAuthScheme, session: AsyncSession = Depends(get_session)
):
    user: User = await session.scalar(
        select(User).where(User.username == login_data.username)
    )
    # Если не существует пользователь, или пароль не подходит, возвращаем ошибку
    if not user or not verify_password(login_data.password, user.password_hashed):
        raise HTTPException(status_code=400, detail="Неверный логин или пароль")

    # таймштамп когда истечет access_token
    expires_timestamp = int(
        (datetime.datetime.now(datetime.UTC) + timedelta(days=1)).timestamp()
    )

    # генерируем токен
    access_token = access_security.create_access_token(
        {"user_id": user.id},
        expires_delta=timedelta(days=1),
    )

    return {"access_token": access_token, "expires": expires_timestamp}


# TODO: Добавить рефреш токенов
