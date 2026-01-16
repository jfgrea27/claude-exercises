import pytest
from books_api.http.books.schemas import BookCreate, BookResponse
from books_api.models.books import BookType
from pydantic import ValidationError


class TestBookCreate:
    def test_valid_minimal(self):
        book = BookCreate(title="Title", author="Author")
        assert book.title == "Title"
        assert book.author == "Author"
        assert book.description is None
        assert book.year is None
        assert book.book_type == BookType.unknown

    def test_valid_full(self):
        book = BookCreate(
            title="Title",
            author="Author",
            description="A description",
            year=2024,
        )
        assert book.title == "Title"
        assert book.author == "Author"
        assert book.description == "A description"
        assert book.year == 2024

    def test_missing_title(self):
        with pytest.raises(ValidationError):
            BookCreate(author="Author")

    def test_missing_author(self):
        with pytest.raises(ValidationError):
            BookCreate(title="Title")

    def test_empty_title(self):
        book = BookCreate(title="", author="Author")
        assert book.title == ""

    def test_year_as_string_coerced(self):
        book = BookCreate(title="Title", author="Author", year="2024")
        assert book.year == 2024

    def test_book_type_fiction(self):
        book = BookCreate(title="Title", author="Author", book_type=BookType.fiction)
        assert book.book_type == BookType.fiction

    def test_book_type_non_fiction(self):
        book = BookCreate(
            title="Title", author="Author", book_type=BookType.non_fiction
        )
        assert book.book_type == BookType.non_fiction

    def test_book_type_from_string(self):
        book = BookCreate(title="Title", author="Author", book_type="fiction")
        assert book.book_type == BookType.fiction

    def test_book_type_invalid_value(self):
        with pytest.raises(ValidationError):
            BookCreate(title="Title", author="Author", book_type="invalid")


class TestBookResponse:
    def test_valid_response(self):
        book = BookResponse(
            id=1,
            title="Title",
            author="Author",
            description="Desc",
            year=2024,
        )
        assert book.id == 1
        assert book.title == "Title"

    def test_missing_id(self):
        with pytest.raises(ValidationError):
            BookResponse(title="Title", author="Author")

    def test_from_attributes_config(self):
        assert BookResponse.model_config["from_attributes"] is True

    def test_response_with_book_type(self):
        book = BookResponse(
            id=1,
            title="Title",
            author="Author",
            book_type=BookType.fiction,
        )
        assert book.book_type == BookType.fiction
