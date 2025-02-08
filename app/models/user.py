from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


class User(Base):
    username: Mapped[str] = mapped_column(index=True)
    password_hashed: Mapped[str] = mapped_column()

    tasks: Mapped[List['Task']] = relationship('Task', back_populates='created_by')