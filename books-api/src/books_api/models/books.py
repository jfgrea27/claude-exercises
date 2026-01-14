from enum import Enum

from sqlalchemy import Enum as SQLEnum
from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from books_api.db.db import Base


class BookType(str, Enum):
    fiction = "fiction"
    non_fiction = "non_fiction"
    unknown = "unknown"


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    author: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    year: Mapped[int | None] = mapped_column(Integer, nullable=True)
    book_type: Mapped[BookType] = mapped_column(
        SQLEnum(BookType), nullable=False, default=BookType.unknown
    )
