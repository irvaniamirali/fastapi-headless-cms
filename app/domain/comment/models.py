from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, ForeignKey, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.base import Base

if TYPE_CHECKING:
    from app.domain.post.models import Post
    from app.domain.user.models import User


class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"), nullable=False)
    parent_id: Mapped[int | None] = mapped_column(
        ForeignKey("comments.id"), nullable=True
    )
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now()
    )

    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    author: Mapped["User"] = relationship("User", back_populates="comments")
    post: Mapped["Post"] = relationship("Post", back_populates="comments")
    replies: Mapped[list["Comment"]] = relationship(
        "Comment", back_populates="parent", cascade="all, delete-orphan"
    )
    parent: Mapped["Comment"] = relationship(
        "Comment", back_populates="replies", remote_side=[id]
    )

    def __repr__(self) -> str:
        return (
            f"<Comment id={self.id} post_id={self.post_id} author_id={self.author_id}>"
        )
