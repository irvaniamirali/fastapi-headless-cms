from pydantic import BaseModel, Field, ConfigDict, model_validator


class CommentCreate(BaseModel):
    post_id: int
    content: str = Field(min_length=1, max_length=2000)
    parent_id: int | None = None

    @model_validator(mode="after")
    def strip_and_validate(cls, values):
        content = values.content.strip()
        if not content:
            raise ValueError("Comment content cannot be empty or whitespace")
        values.content = content
        return values


class CommentUpdate(BaseModel):
    content: str = Field(min_length=1, max_length=2000)

    @model_validator(mode="after")
    def strip_and_validate(cls, values):
        content = values.content.strip()
        if not content:
            raise ValueError("Comment content cannot be empty or whitespace")
        values.content = content
        return values


class CommentOut(BaseModel):
    id: int
    post_id: int
    author_id: int
    content: str
    parent_id: int | None
    replies: list["CommentOut"] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)


CommentOut.model_rebuild()


class CommentList(BaseModel):
    total: int
    items: list[CommentOut]
