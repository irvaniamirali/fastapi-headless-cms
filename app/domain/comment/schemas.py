from pydantic import BaseModel, ConfigDict, Field, model_validator


class CommentBase(BaseModel):
    content: str = Field(min_length=1, max_length=2000)

    @model_validator(mode="after")
    def strip_and_validate(cls, values):
        content = values.content.strip()
        if not content:
            raise ValueError("Comment content cannot be empty or whitespace")
        values.content = content
        return values


class CommentCreate(CommentBase):
    post_id: int
    parent_id: int | None = None


class CommentUpdate(CommentBase): ...


class CommentOut(CommentBase):
    id: int
    post_id: int
    author_id: int
    parent_id: int | None
    replies: list["CommentOut"] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)


CommentOut.model_rebuild()


class CommentList(BaseModel):
    total: int
    items: list[CommentOut]
