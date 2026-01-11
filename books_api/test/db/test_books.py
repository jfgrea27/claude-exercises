from books_api.db import (
    create_book,
    delete_book,
    get_all_books,
    get_book_by_id,
    update_book,
)


class TestGetAllBooks:
    def test_empty_database(self, db_session):
        books = get_all_books(db_session)
        assert books == []

    def test_returns_all_books(self, db_session):
        create_book(db_session, {"title": "Book 1", "author": "Author 1"})
        create_book(db_session, {"title": "Book 2", "author": "Author 2"})

        books = get_all_books(db_session)
        assert len(books) == 2


class TestGetBookById:
    def test_book_not_found(self, db_session):
        book = get_book_by_id(db_session, 999)
        assert book is None

    def test_book_found(self, db_session):
        created = create_book(db_session, {"title": "Test", "author": "Author"})

        book = get_book_by_id(db_session, created.id)
        assert book is not None
        assert book.id == created.id
        assert book.title == "Test"


class TestCreateBook:
    def test_create_minimal_book(self, db_session):
        book = create_book(db_session, {"title": "Title", "author": "Author"})

        assert book.id is not None
        assert book.title == "Title"
        assert book.author == "Author"
        assert book.description is None
        assert book.year is None

    def test_create_full_book(self, db_session):
        book = create_book(
            db_session,
            {
                "title": "Title",
                "author": "Author",
                "description": "A description",
                "year": 2024,
            },
        )

        assert book.id is not None
        assert book.title == "Title"
        assert book.author == "Author"
        assert book.description == "A description"
        assert book.year == 2024

    def test_book_persisted(self, db_session):
        created = create_book(db_session, {"title": "Title", "author": "Author"})

        fetched = get_book_by_id(db_session, created.id)
        assert fetched is not None
        assert fetched.title == "Title"


class TestUpdateBook:
    def test_update_single_field(self, db_session):
        book = create_book(db_session, {"title": "Original", "author": "Author"})

        updated = update_book(
            db_session, book, {"title": "Updated", "author": "Author"}
        )

        assert updated.title == "Updated"
        assert updated.author == "Author"

    def test_update_all_fields(self, db_session):
        book = create_book(db_session, {"title": "Title", "author": "Author"})

        updated = update_book(
            db_session,
            book,
            {
                "title": "New Title",
                "author": "New Author",
                "description": "New desc",
                "year": 2025,
            },
        )

        assert updated.title == "New Title"
        assert updated.author == "New Author"
        assert updated.description == "New desc"
        assert updated.year == 2025

    def test_update_persisted(self, db_session):
        book = create_book(db_session, {"title": "Original", "author": "Author"})
        update_book(db_session, book, {"title": "Updated", "author": "Author"})

        fetched = get_book_by_id(db_session, book.id)
        assert fetched.title == "Updated"


class TestDeleteBook:
    def test_delete_book(self, db_session):
        book = create_book(db_session, {"title": "Title", "author": "Author"})

        delete_book(db_session, book)

        assert get_book_by_id(db_session, book.id) is None

    def test_delete_only_target_book(self, db_session):
        book1 = create_book(db_session, {"title": "Book 1", "author": "Author"})
        book2 = create_book(db_session, {"title": "Book 2", "author": "Author"})

        delete_book(db_session, book1)

        assert get_book_by_id(db_session, book1.id) is None
        assert get_book_by_id(db_session, book2.id) is not None
