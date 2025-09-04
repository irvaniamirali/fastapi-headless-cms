from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict, model_validator


class PostBase(BaseModel):
    title: str = Field(min_length=3, max_length=200)
    content: str = Field(min_length=1)
    slug: str | None = Field(default=None, min_length=1, max_length=240)


class PostCreate(PostBase):
    pass


class PostUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=3, max_length=200)
    content: str | None = Field(default=None, min_length=1)
    slug: str | None = Field(default=None, min_length=1, max_length=240)

    @model_validator(mode="after")
    def at_least_one_field(cls, values):  # noqa: D401
        if not any(values.model_dump(exclude_unset=True).values()):
            raise ValueError("At least one field must be provided")
        return values


class PostOut(BaseModel):
    id: int
    title: str
    slug: str
    content: str
    author_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PostList(BaseModel):
    total: int
    items: list[PostOut]
