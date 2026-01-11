import logging
from typing import Any

from sqlalchemy.orm import Session

from books_api.models import Book

logger = logging.getLogger("books_api")


def get_all_books(db: Session) -> list[Book]:
    logger.debug("Querying all books from database")
    books = db.query(Book).all()
    logger.debug("Retrieved %d books from database", len(books))
    return books


def get_book_by_id(db: Session, book_id: int) -> Book | None:
    logger.debug("Querying book with id=%d from database", book_id)
    book = db.query(Book).filter(Book.id == book_id).first()
    logger.debug("Book with id=%d %s", book_id, "found" if book else "not found")
    return book


def create_book(db: Session, data: dict[str, Any]) -> Book:
    logger.debug("Creating new book with data: %s", data)
    book = Book(**data)
    db.add(book)
    db.commit()
    db.refresh(book)
    logger.debug("Created book with id=%d", book.id)
    return book


def update_book(db: Session, book: Book, data: dict[str, Any]) -> Book:
    logger.debug("Updating book id=%d with data: %s", book.id, data)
    for key, value in data.items():
        setattr(book, key, value)
    db.commit()
    db.refresh(book)
    logger.debug("Updated book id=%d", book.id)
    return book


def delete_book(db: Session, book: Book) -> None:
    logger.debug("Deleting book id=%d from database", book.id)
    db.delete(book)
    db.commit()
    logger.debug("Deleted book id=%d", book.id)
