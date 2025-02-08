from datetime import datetime

from pydantic import BaseModel, Field


class TaskScheme(BaseModel):
    id: int
    title: str
    description: str
    is_done: bool

    created_at: datetime


class TaskCreateScheme(BaseModel):
    # Минимальная длина title и description = 3
    title: str = Field(..., min_length=3)
    description: str = Field(..., min_length=3)


class TaskUpdateScheme(BaseModel):
    is_done: bool
