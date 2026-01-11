from pydantic import BaseModel


class BookBase(BaseModel):
    title: str
    author: str
    description: str | None = None
    year: int | None = None


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    title: str | None = None
    author: str | None = None
    description: str | None = None
    year: int | None = None


class BookResponse(BookBase):
    id: int

    model_config = {"from_attributes": True}
