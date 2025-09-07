from typing import Annotated, TypeAlias

from pydantic import AfterValidator, BaseModel, ConfigDict, EmailStr, Field

Email: TypeAlias = Annotated[EmailStr, AfterValidator(str.lower)]


class UserCreate(BaseModel):
    email: Email
    password: str = Field(..., min_length=8)


class UserRead(BaseModel):
    id: int
    email: Email

    model_config = ConfigDict(from_attributes=True)
