import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from books_api.db import get_db
from books_api.db.users import (
    create_user,
    get_all_users,
    get_user_by_id,
    update_user,
)
from books_api.db.users import (
    delete_user as db_delete_user,
)
from books_api.http.users.schemas import UserCreate, UserResponse, UserUpdate
from books_api.models.users import User

logger = logging.getLogger("books_api")

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)) -> list[User]:
    logger.info("GET /users - Starting request")
    users = get_all_users(db)
    logger.info("GET /users - Completed request")
    return users


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)) -> User:
    logger.info("GET /users/%s - Starting request", user_id)
    user = get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    logger.info("GET /users/%s - Completed request", user_id)
    return user


@router.post("", response_model=UserResponse, status_code=201)
def create_new_user(user_data: UserCreate, db: Session = Depends(get_db)) -> User:
    logger.info("POST /users - Starting request")
    user = create_user(db, user_data.model_dump())
    logger.info("POST /users - Completed request")
    return user


@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: int, db: Session = Depends(get_db)) -> None:
    logger.info("DELETE /users/%s - Starting request", user_id)
    user = get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_delete_user(db, user)
    logger.info("DELETE /users/%s - Completed request", user_id)


@router.patch("/{user_id}", response_model=UserResponse)
def patch_user(
    user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)
) -> User:
    logger.info("PATCH /users/%s - Starting request", user_id)
    user = get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    update_data = {k: v for k, v in user_update.model_dump().items() if v is not None}
    updated_user = update_user(db, user, update_data)
    logger.info("PATCH /users/%s - Completed request", user_id)
    return updated_user
