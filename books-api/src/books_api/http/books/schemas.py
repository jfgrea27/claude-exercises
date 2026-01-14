from pydantic import BaseModel

from books_api.models import BookType


class BookBase(BaseModel):
    title: str
    author: str
    description: str | None = None
    year: int | None = None
    book_type: BookType = BookType.unknown


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    title: str | None = None
    author: str | None = None
    description: str | None = None
    year: int | None = None
    book_type: BookType | None = None


class BookResponse(BookBase):
    id: int

    model_config = {"from_attributes": True}
