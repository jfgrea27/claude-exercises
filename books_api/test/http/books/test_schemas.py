import pytest
from books_api.http.books.schemas import BookCreate, BookResponse, BookUpdate
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


class TestBookUpdate:
    def test_all_fields_optional(self):
        update = BookUpdate()
        assert update.title is None
        assert update.author is None
        assert update.description is None
        assert update.year is None

    def test_partial_update(self):
        update = BookUpdate(title="New Title")
        assert update.title == "New Title"
        assert update.author is None

    def test_full_update(self):
        update = BookUpdate(
            title="Title",
            author="Author",
            description="Desc",
            year=2024,
        )
        assert update.title == "Title"
        assert update.author == "Author"
        assert update.description == "Desc"
        assert update.year == 2024
