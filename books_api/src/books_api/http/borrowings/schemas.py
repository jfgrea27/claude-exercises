from datetime import datetime

from pydantic import BaseModel


class BorrowingBase(BaseModel):
    user_id: int
    book_id: int


class BorrowingCreate(BorrowingBase):
    pass


class BorrowingUpdate(BaseModel):
    user_id: int | None = None
    book_id: int | None = None


class BorrowingResponse(BorrowingBase):
    id: int
    borrowed_at: datetime
    returned_at: datetime | None = None

    model_config = {"from_attributes": True}
