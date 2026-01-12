import logging
from datetime import UTC, datetime
from typing import Any

from sqlalchemy.orm import Session

from books_api.models.borrowings import Borrowing

logger = logging.getLogger("books_api")


def get_all_borrowings(db: Session) -> list[Borrowing]:
    logger.debug("Querying all borrowings from database")
    borrowings = db.query(Borrowing).all()
    logger.debug("Retrieved %d borrowings from database", len(borrowings))
    return borrowings


def get_borrowing_by_id(db: Session, borrowing_id: int) -> Borrowing | None:
    logger.debug("Querying borrowing with id=%d from database", borrowing_id)
    borrowing = db.query(Borrowing).filter(Borrowing.id == borrowing_id).first()
    logger.debug(
        "Borrowing with id=%d %s", borrowing_id, "found" if borrowing else "not found"
    )
    return borrowing


def get_borrowings_by_user(db: Session, user_id: int) -> list[Borrowing]:
    logger.debug("Querying borrowings for user id=%d from database", user_id)
    borrowings = db.query(Borrowing).filter(Borrowing.user_id == user_id).all()
    logger.debug("Retrieved %d borrowings for user id=%d", len(borrowings), user_id)
    return borrowings


def get_borrowings_by_book(db: Session, book_id: int) -> list[Borrowing]:
    logger.debug("Querying borrowings for book id=%d from database", book_id)
    borrowings = db.query(Borrowing).filter(Borrowing.book_id == book_id).all()
    logger.debug("Retrieved %d borrowings for book id=%d", len(borrowings), book_id)
    return borrowings


def create_borrowing(db: Session, data: dict[str, Any]) -> Borrowing:
    logger.debug("Creating new borrowing with data: %s", data)
    borrowing = Borrowing(**data)
    db.add(borrowing)
    db.commit()
    db.refresh(borrowing)
    logger.debug("Created borrowing with id=%d", borrowing.id)
    return borrowing


def update_borrowing(
    db: Session, borrowing: Borrowing, data: dict[str, Any]
) -> Borrowing:
    logger.debug("Updating borrowing id=%d with data: %s", borrowing.id, data)
    for key, value in data.items():
        setattr(borrowing, key, value)
    db.commit()
    db.refresh(borrowing)
    logger.debug("Updated borrowing id=%d", borrowing.id)
    return borrowing


def return_book(db: Session, borrowing: Borrowing) -> Borrowing:
    logger.debug("Returning book for borrowing id=%d", borrowing.id)
    borrowing.returned_at = datetime.now(UTC)
    db.commit()
    db.refresh(borrowing)
    logger.debug("Book returned for borrowing id=%d", borrowing.id)
    return borrowing


def delete_borrowing(db: Session, borrowing: Borrowing) -> None:
    logger.debug("Deleting borrowing id=%d from database", borrowing.id)
    db.delete(borrowing)
    db.commit()
    logger.debug("Deleted borrowing id=%d", borrowing.id)
