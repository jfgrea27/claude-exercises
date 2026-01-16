from books_api.models import Book
from books_api.models.books import BookType


class TestBookType:
    def test_enum_values(self):
        assert BookType.fiction.value == "fiction"
        assert BookType.non_fiction.value == "non_fiction"
        assert BookType.unknown.value == "unknown"

    def test_enum_members(self):
        members = [m.value for m in BookType]
        assert "fiction" in members
        assert "non_fiction" in members
        assert "unknown" in members
        assert len(members) == 3


class TestBookModel:
    def test_tablename(self):
        assert Book.__tablename__ == "books"

    def test_create_book_instance(self, db_session):
        book = Book(
            id=1,
            title="Test Title",
            author="Test Author",
            description="Test Description",
            year=2024,
        )
        db_session.add(book)
        db_session.commit()

        assert book.id == 1
        assert book.title == "Test Title"
        assert book.author == "Test Author"
        assert book.description == "Test Description"
        assert book.year == 2024

    def test_nullable_fields(self, db_session):
        book = Book(
            id=1,
            title="Title",
            author="Author",
        )
        db_session.add(book)
        db_session.commit()

        assert book.description is None
        assert book.year is None

    def test_book_query(self, db_session):
        book = Book(id=1, title="Queryable", author="Author")
        db_session.add(book)
        db_session.commit()

        result = db_session.query(Book).filter(Book.id == 1).first()
        assert result is not None
        assert result.title == "Queryable"

    def test_book_type_default(self, db_session):
        book = Book(id=1, title="Title", author="Author")
        db_session.add(book)
        db_session.commit()

        assert book.book_type == BookType.unknown

    def test_book_type_fiction(self, db_session):
        book = Book(id=1, title="Novel", author="Author", book_type=BookType.fiction)
        db_session.add(book)
        db_session.commit()

        assert book.book_type == BookType.fiction

    def test_book_type_non_fiction(self, db_session):
        book = Book(
            id=1, title="Biography", author="Author", book_type=BookType.non_fiction
        )
        db_session.add(book)
        db_session.commit()

        assert book.book_type == BookType.non_fiction
