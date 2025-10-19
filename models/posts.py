from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text, Integer
from .base import Base

class PostDB(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True) 
    slug: Mapped[str] = mapped_column(String(200), nullable=False, unique=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    author: Mapped[str] = mapped_column(String(100), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    image_url: Mapped[str] = mapped_column(String(200), nullable=True)
    likes: Mapped[int] = mapped_column(default=0)

    def __repr__(self):
        return f"Post(id={self.id}, slug={self.slug}, title={self.title})"