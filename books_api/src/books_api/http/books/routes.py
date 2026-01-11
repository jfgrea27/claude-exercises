import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from books_api.db import (
    create_book,
    get_all_books,
    get_book_by_id,
    get_db,
)
from books_api.db import delete_book as db_delete_book
from books_api.http.books.schemas import BookCreate, BookResponse
from books_api.models import Book

logger = logging.getLogger("books_api")

router = APIRouter(prefix="/books", tags=["books"])


@router.get("", response_model=list[BookResponse])
def get_books(db: Session = Depends(get_db)) -> list[Book]:
    logger.info("GET /books - Starting request")
    books = get_all_books(db)
    logger.info("GET /books - Completed request")
    return books


@router.get("/{book_id}", response_model=BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)) -> Book:
    logger.info("GET /books/%s - Starting request", book_id)
    book = get_book_by_id(db, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    logger.info("GET /books/%s - Completed request", book_id)
    return book


@router.post("", response_model=BookResponse, status_code=201)
def create_new_book(book_data: BookCreate, db: Session = Depends(get_db)) -> Book:
    logger.info("POST /books - Starting request")
    book = create_book(db, book_data.model_dump())
    logger.info("POST /books - Completed request")
    return book


@router.delete("/{book_id}", status_code=204)
def delete_book(book_id: int, db: Session = Depends(get_db)) -> None:
    logger.info("DELETE /books/%s - Starting request", book_id)
    book = get_book_by_id(db, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    db_delete_book(db, book)
    logger.info("DELETE /books/%s - Completed request", book_id)
