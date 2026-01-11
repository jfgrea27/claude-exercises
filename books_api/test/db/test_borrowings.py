from books_api.db.books import create_book
from books_api.db.borrowings import (
    create_borrowing,
    delete_borrowing,
    get_all_borrowings,
    get_borrowing_by_id,
    get_borrowings_by_book,
    get_borrowings_by_user,
    return_book,
    update_borrowing,
)
from books_api.db.users import create_user


class TestGetAllBorrowings:
    def test_empty_database(self, db_session):
        borrowings = get_all_borrowings(db_session)
        assert borrowings == []

    def test_returns_all_borrowings(self, db_session):
        user = create_user(db_session, {"name": "User", "email": "user@example.com"})
        book1 = create_book(db_session, {"title": "Book 1", "author": "Author 1"})
        book2 = create_book(db_session, {"title": "Book 2", "author": "Author 2"})

        create_borrowing(db_session, {"user_id": user.id, "book_id": book1.id})
        create_borrowing(db_session, {"user_id": user.id, "book_id": book2.id})

        borrowings = get_all_borrowings(db_session)
        assert len(borrowings) == 2


class TestGetBorrowingById:
    def test_borrowing_not_found(self, db_session):
        borrowing = get_borrowing_by_id(db_session, 999)
        assert borrowing is None

    def test_borrowing_found(self, db_session):
        user = create_user(db_session, {"name": "User", "email": "user@example.com"})
        book = create_book(db_session, {"title": "Book", "author": "Author"})
        created = create_borrowing(db_session, {"user_id": user.id, "book_id": book.id})

        borrowing = get_borrowing_by_id(db_session, created.id)
        assert borrowing is not None
        assert borrowing.id == created.id


class TestGetBorrowingsByUser:
    def test_no_borrowings_for_user(self, db_session):
        user = create_user(db_session, {"name": "User", "email": "user@example.com"})

        borrowings = get_borrowings_by_user(db_session, user.id)
        assert borrowings == []

    def test_returns_user_borrowings_only(self, db_session):
        user1 = create_user(
            db_session, {"name": "User 1", "email": "user1@example.com"}
        )
        user2 = create_user(
            db_session, {"name": "User 2", "email": "user2@example.com"}
        )
        book1 = create_book(db_session, {"title": "Book 1", "author": "Author 1"})
        book2 = create_book(db_session, {"title": "Book 2", "author": "Author 2"})

        create_borrowing(db_session, {"user_id": user1.id, "book_id": book1.id})
        create_borrowing(db_session, {"user_id": user2.id, "book_id": book2.id})

        borrowings = get_borrowings_by_user(db_session, user1.id)
        assert len(borrowings) == 1
        assert borrowings[0].user_id == user1.id


class TestGetBorrowingsByBook:
    def test_no_borrowings_for_book(self, db_session):
        book = create_book(db_session, {"title": "Book", "author": "Author"})

        borrowings = get_borrowings_by_book(db_session, book.id)
        assert borrowings == []


class TestCreateBorrowing:
    def test_create_borrowing(self, db_session):
        user = create_user(db_session, {"name": "User", "email": "user@example.com"})
        book = create_book(db_session, {"title": "Book", "author": "Author"})

        borrowing = create_borrowing(
            db_session, {"user_id": user.id, "book_id": book.id}
        )

        assert borrowing.id is not None
        assert borrowing.user_id == user.id
        assert borrowing.book_id == book.id
        assert borrowing.borrowed_at is not None
        assert borrowing.returned_at is None

    def test_borrowing_persisted(self, db_session):
        user = create_user(db_session, {"name": "User", "email": "user@example.com"})
        book = create_book(db_session, {"title": "Book", "author": "Author"})
        created = create_borrowing(db_session, {"user_id": user.id, "book_id": book.id})

        fetched = get_borrowing_by_id(db_session, created.id)
        assert fetched is not None
        assert fetched.user_id == user.id


class TestReturnBook:
    def test_return_book(self, db_session):
        user = create_user(db_session, {"name": "User", "email": "user@example.com"})
        book = create_book(db_session, {"title": "Book", "author": "Author"})
        borrowing = create_borrowing(
            db_session, {"user_id": user.id, "book_id": book.id}
        )

        returned = return_book(db_session, borrowing)

        assert returned.returned_at is not None


class TestUpdateBorrowing:
    def test_update_borrowing(self, db_session):
        user1 = create_user(
            db_session, {"name": "User 1", "email": "user1@example.com"}
        )
        user2 = create_user(
            db_session, {"name": "User 2", "email": "user2@example.com"}
        )
        book = create_book(db_session, {"title": "Book", "author": "Author"})
        borrowing = create_borrowing(
            db_session, {"user_id": user1.id, "book_id": book.id}
        )

        updated = update_borrowing(db_session, borrowing, {"user_id": user2.id})

        assert updated.user_id == user2.id


class TestDeleteBorrowing:
    def test_delete_borrowing(self, db_session):
        user = create_user(db_session, {"name": "User", "email": "user@example.com"})
        book = create_book(db_session, {"title": "Book", "author": "Author"})
        borrowing = create_borrowing(
            db_session, {"user_id": user.id, "book_id": book.id}
        )

        delete_borrowing(db_session, borrowing)

        assert get_borrowing_by_id(db_session, borrowing.id) is None
