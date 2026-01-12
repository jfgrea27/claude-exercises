import logging
from typing import Any

from sqlalchemy.orm import Session

from books_api.models.users import User

logger = logging.getLogger("books_api")


def get_all_users(db: Session) -> list[User]:
    logger.debug("Querying all users from database")
    users = db.query(User).all()
    logger.debug("Retrieved %d users from database", len(users))
    return users


def get_user_by_id(db: Session, user_id: int) -> User | None:
    logger.debug("Querying user with id=%d from database", user_id)
    user = db.query(User).filter(User.id == user_id).first()
    logger.debug("User with id=%d %s", user_id, "found" if user else "not found")
    return user


def create_user(db: Session, data: dict[str, Any]) -> User:
    logger.debug("Creating new user with data: %s", data)
    user = User(**data)
    db.add(user)
    db.commit()
    db.refresh(user)
    logger.debug("Created user with id=%d", user.id)
    return user


def update_user(db: Session, user: User, data: dict[str, Any]) -> User:
    logger.debug("Updating user id=%d with data: %s", user.id, data)
    for key, value in data.items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    logger.debug("Updated user id=%d", user.id)
    return user


def delete_user(db: Session, user: User) -> None:
    logger.debug("Deleting user id=%d from database", user.id)
    db.delete(user)
    db.commit()
    logger.debug("Deleted user id=%d", user.id)
