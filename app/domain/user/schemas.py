from typing import TypeAlias, Annotated

from pydantic import BaseModel, EmailStr, ConfigDict, Field, AfterValidator


Email: TypeAlias = Annotated[EmailStr, AfterValidator(str.lower)]


class UserCreate(BaseModel):
    email: Email
    password: str = Field(..., min_length=8)


class UserRead(BaseModel):
    id: int
    email: Email

    model_config = ConfigDict(from_attributes=True)
