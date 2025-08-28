from typing import TypeAlias, Annotated

from pydantic import BaseModel, EmailStr, Field, ConfigDict, AfterValidator

from .models import UserRole

Email: TypeAlias = Annotated[EmailStr, AfterValidator(str.lower)]


class UserCreate(BaseModel):
    email: Email
    password: str = Field(min_length=8)


class UserRead(BaseModel):
    id: int
    email: Email
    role: UserRole = UserRole.USER
    is_active: bool

    model_config = ConfigDict(
        from_attributes=True
    )
