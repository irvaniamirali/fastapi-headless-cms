from enum import Enum

from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, Enum as SQLAlchemyEnum

from app.infrastructure.database.base import Base


class UserRole(str, Enum):
    USER = "USER"
    ADMIN = "ADMIN"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(SQLAlchemyEnum(UserRole, name="user_role"), default=UserRole.USER, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
