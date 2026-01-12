import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from books_api.db import get_db
from books_api.db.books import get_book_by_id
from books_api.db.borrowings import (
    create_borrowing,
    get_all_borrowings,
    get_borrowing_by_id,
    get_borrowings_by_user,
    return_book,
    update_borrowing,
)
from books_api.db.borrowings import (
    delete_borrowing as db_delete_borrowing,
)
from books_api.db.users import get_user_by_id
from books_api.http.borrowings.schemas import (
    BorrowingCreate,
    BorrowingResponse,
    BorrowingUpdate,
)
from books_api.models.borrowings import Borrowing

logger = logging.getLogger("books_api")

router = APIRouter(prefix="/borrowings", tags=["borrowings"])


@router.get("", response_model=list[BorrowingResponse])
def get_borrowings(
    user_id: int | None = None, db: Session = Depends(get_db)
) -> list[Borrowing]:
    logger.info("GET /borrowings - Starting request")
    if user_id is not None:
        borrowings = get_borrowings_by_user(db, user_id)
    else:
        borrowings = get_all_borrowings(db)
    logger.info("GET /borrowings - Completed request")
    return borrowings


@router.get("/{borrowing_id}", response_model=BorrowingResponse)
def get_borrowing(borrowing_id: int, db: Session = Depends(get_db)) -> Borrowing:
    logger.info("GET /borrowings/%s - Starting request", borrowing_id)
    borrowing = get_borrowing_by_id(db, borrowing_id)
    if borrowing is None:
        raise HTTPException(status_code=404, detail="Borrowing not found")
    logger.info("GET /borrowings/%s - Completed request", borrowing_id)
    return borrowing


@router.post("", response_model=BorrowingResponse, status_code=201)
def create_new_borrowing(
    borrowing_data: BorrowingCreate, db: Session = Depends(get_db)
) -> Borrowing:
    logger.info("POST /borrowings - Starting request")
    # Validate user exists
    user = get_user_by_id(db, borrowing_data.user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    # Validate book exists
    book = get_book_by_id(db, borrowing_data.book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    borrowing = create_borrowing(db, borrowing_data.model_dump())
    logger.info("POST /borrowings - Completed request")
    return borrowing


@router.delete("/{borrowing_id}", status_code=204)
def delete_borrowing(borrowing_id: int, db: Session = Depends(get_db)) -> None:
    logger.info("DELETE /borrowings/%s - Starting request", borrowing_id)
    borrowing = get_borrowing_by_id(db, borrowing_id)
    if borrowing is None:
        raise HTTPException(status_code=404, detail="Borrowing not found")
    db_delete_borrowing(db, borrowing)
    logger.info("DELETE /borrowings/%s - Completed request", borrowing_id)


@router.patch("/{borrowing_id}", response_model=BorrowingResponse)
def patch_borrowing(
    borrowing_id: int, borrowing_update: BorrowingUpdate, db: Session = Depends(get_db)
) -> Borrowing:
    logger.info("PATCH /borrowings/%s - Starting request", borrowing_id)
    borrowing = get_borrowing_by_id(db, borrowing_id)
    if borrowing is None:
        raise HTTPException(status_code=404, detail="Borrowing not found")
    update_data = {
        k: v for k, v in borrowing_update.model_dump().items() if v is not None
    }
    updated_borrowing = update_borrowing(db, borrowing, update_data)
    logger.info("PATCH /borrowings/%s - Completed request", borrowing_id)
    return updated_borrowing


@router.post("/{borrowing_id}/return", response_model=BorrowingResponse)
def return_borrowed_book(borrowing_id: int, db: Session = Depends(get_db)) -> Borrowing:
    logger.info("POST /borrowings/%s/return - Starting request", borrowing_id)
    borrowing = get_borrowing_by_id(db, borrowing_id)
    if borrowing is None:
        raise HTTPException(status_code=404, detail="Borrowing not found")
    if borrowing.returned_at is not None:
        raise HTTPException(status_code=400, detail="Book already returned")
    returned_borrowing = return_book(db, borrowing)
    logger.info("POST /borrowings/%s/return - Completed request", borrowing_id)
    return returned_borrowing
