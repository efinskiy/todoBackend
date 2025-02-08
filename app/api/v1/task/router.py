from typing import List

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session
from app.entities.auth import AuthManagerData
from app.entities.common import MessageResponseSchema
from app.entities.tasks import TaskScheme, TaskCreateScheme, TaskUpdateScheme
from app.models import Task
from app.utils.auth import AuthManager

router = APIRouter(prefix="/task", tags=["Task"])


# Получение всех задач пользователя
@router.get("/", response_model=List[TaskScheme])
async def get_tasks(
    user: AuthManagerData = Depends(AuthManager()),
    session: AsyncSession = Depends(get_session),
):
    tasks = await session.scalars(
        select(Task)
        .where(Task.created_by_id == user.user_id)
        .order_by(Task.created_at.desc())
    )

    return tasks


# Создание задачи
@router.post("/", response_model=TaskScheme)
async def create_task(
    data: TaskCreateScheme,
    session: AsyncSession = Depends(get_session),
    user: AuthManagerData = Depends(AuthManager()),
):
    new_task = Task(
        title=data.title,
        description=data.description,
        created_by_id=user.user_id,
    )

    session.add(new_task)
    await session.commit()
    return new_task


# Обновление статуса задачи
@router.patch("/{task_id}", response_model=TaskScheme)
async def update_task(
    task_id: int,
    data: TaskUpdateScheme,
    session: AsyncSession = Depends(get_session),
    user: AuthManagerData = Depends(AuthManager()),
):
    task = await session.get(Task, task_id)

    # Если задача отсутствует в бд, возвращаем 404 ошибку
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    # Если задача была создана другим пользователем, возвращаем 403 ошибку
    if task.created_by_id != user.user_id:
        raise HTTPException(
            status_code=403,
            detail="Недостаточно прав для редактирования задачи созданной не вами",
        )

    task.is_done = data.is_done

    session.add(task)
    await session.commit()
    return task


@router.delete("/{task_id}", response_model=MessageResponseSchema)
async def delete_task(
    task_id: int,
    session: AsyncSession = Depends(get_session),
    user: AuthManagerData = Depends(AuthManager()),
):
    task = await session.get(Task, task_id)
    # Если задача отсутствует в бд, возвращаем 404 ошибку
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    # Если задача была создана другим пользователем, возвращаем 403 ошибку
    if task.created_by_id != user.user_id:
        raise HTTPException(
            status_code=403,
            detail="Недостаточно прав для редактирования задачи созданной не вами",
        )
    await session.delete(task)
    await session.commit()
    return MessageResponseSchema(msg="Задача удалена")
