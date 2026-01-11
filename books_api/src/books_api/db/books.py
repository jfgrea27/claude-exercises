import logging
from typing import Any

from sqlalchemy.orm import Session

from books_api.models import Book

logger = logging.getLogger("books_api")


def get_all_books(db: Session) -> list[Book]:
    return db.query(Book).all()


def get_book_by_id(db: Session, book_id: int) -> Book | None:
    return db.query(Book).filter(Book.id == book_id).first()


def create_book(db: Session, data: dict[str, Any]) -> Book:
    book = Book(**data)
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


def update_book(db: Session, book: Book, data: dict[str, Any]) -> Book:
    for key, value in data.items():
        setattr(book, key, value)
    db.commit()
    db.refresh(book)
    return book


def delete_book(db: Session, book: Book) -> None:
    db.delete(book)
    db.commit()
