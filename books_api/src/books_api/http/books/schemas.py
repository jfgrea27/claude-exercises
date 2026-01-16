from pydantic import BaseModel

from books_api.models.books import BookType


class BookBase(BaseModel):
    title: str
    author: str
    description: str | None = None
    year: int | None = None
    book_type: BookType = BookType.unknown


class BookCreate(BookBase):
    pass


class BookResponse(BookBase):
    id: int

    model_config = {"from_attributes": True}
