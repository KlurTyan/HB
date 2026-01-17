from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .types import UserRole, ReactionsTypes

from .manager import Base

class User(Base):
    __tablename__ = "users"

    token : Mapped[str] = mapped_column(String(255), unique=True, nullable=True)
    name: Mapped[str] = mapped_column(String(255))
    role: Mapped[UserRole] = mapped_column()
    secret_char : Mapped[str] = mapped_column(String(255))
    #relationship
    tasks : Mapped[list["Task"]] = relationship(back_populates="tasks_user")

class Task(Base):
    __tablename__ = "tasks"

    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text)
    is_completed: Mapped[bool] = mapped_column(default=False, server_default='false')
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    #relationship
    tasks_user: Mapped["User"] = relationship(back_populates="tasks")

class Reactions(Base):
    __tablename__ = "reactions"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    reaction_type: Mapped[ReactionsTypes]= mapped_column()

class SystemLog(Base):
    __tablename__ = "system_log"

    message: Mapped[str] = mapped_column(Text)
    is_alert: Mapped[bool] = mapped_column(default=False, server_default='false')

