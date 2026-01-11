import pytest
from books_api.http.books.schemas import BookCreate, BookResponse
from pydantic import ValidationError


class TestBookCreate:
    def test_valid_minimal(self):
        book = BookCreate(title="Title", author="Author")
        assert book.title == "Title"
        assert book.author == "Author"
        assert book.description is None
        assert book.year is None

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
