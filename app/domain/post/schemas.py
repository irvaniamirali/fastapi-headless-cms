from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, model_validator


class PostBase(BaseModel):
    title: str = Field(min_length=3, max_length=200)
    content: str = Field(min_length=1)
    slug: str | None = Field(default=None, min_length=1, max_length=240)

    @model_validator(mode="after")
    def strip_and_validate(cls, values):
        title = values.title.strip() if values.title else None
        content = values.content.strip() if values.content else None
        slug = values.slug.strip() if values.slug else None

        if not title:
            raise ValueError("Title cannot be empty or whitespace")
        if not content:
            raise ValueError("Content cannot be empty or whitespace")

        values.title = title
        values.content = content
        values.slug = slug
        return values


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

    @model_validator(mode="after")
    def strip_fields(cls, values):
        if values.title is not None:
            values.title = values.title.strip()
            if not values.title:
                raise ValueError("Title cannot be empty or whitespace")
        if values.content is not None:
            values.content = values.content.strip()
            if not values.content:
                raise ValueError("Content cannot be empty or whitespace")
        if values.slug is not None:
            values.slug = values.slug.strip()
            if not values.slug:
                raise ValueError("Slug cannot be empty or whitespace")
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
