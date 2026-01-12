from datetime import UTC, datetime

from books_api.models.borrowings import Borrowing


class TestBorrowingModel:
    def test_borrowing_has_required_attributes(self):
        now = datetime.now(UTC)
        borrowing = Borrowing(
            id=1, user_id=1, book_id=1, borrowed_at=now, returned_at=None
        )
        assert borrowing.id == 1
        assert borrowing.user_id == 1
        assert borrowing.book_id == 1
        assert borrowing.borrowed_at == now
        assert borrowing.returned_at is None
