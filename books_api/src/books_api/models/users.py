from typing import TYPE_CHECKING

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from books_api.db.db import Base

if TYPE_CHECKING:
    from books_api.models.borrowings import Borrowing


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)

    borrowings: Mapped[list["Borrowing"]] = relationship(
        "Borrowing", back_populates="user"
    )
