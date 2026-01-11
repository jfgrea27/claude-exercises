class TestGetBooks:
    def test_get_books_empty(self, client):
        response = client.get("/books")
        assert response.status_code == 200
        assert response.json() == []

    def test_get_books_with_data(self, client):
        client.post("/books", json={"title": "Book 1", "author": "Author 1"})
        client.post("/books", json={"title": "Book 2", "author": "Author 2"})

        response = client.get("/books")
        assert response.status_code == 200
        books = response.json()
        assert len(books) == 2


class TestGetBook:
    def test_get_book_not_found(self, client):
        response = client.get("/books/999")
        assert response.status_code == 404
        assert response.json()["detail"] == "Book not found"

    def test_get_book_success(self, client):
        create_response = client.post(
            "/books", json={"title": "Test Book", "author": "Test Author"}
        )
        book_id = create_response.json()["id"]

        response = client.get(f"/books/{book_id}")
        assert response.status_code == 200
        book = response.json()
        assert book["id"] == book_id
        assert book["title"] == "Test Book"
        assert book["author"] == "Test Author"


class TestCreateBook:
    def test_create_new_book(self, client):
        response = client.post(
            "/books",
            json={
                "title": "New Book",
                "author": "New Author",
                "description": "A description",
                "year": 2024,
            },
        )
        assert response.status_code == 201
        book = response.json()
        assert book["id"] is not None
        assert book["title"] == "New Book"
        assert book["author"] == "New Author"
        assert book["description"] == "A description"
        assert book["year"] == 2024

    def test_create_minimal_book(self, client):
        response = client.post(
            "/books",
            json={"title": "Minimal", "author": "Author"},
        )
        assert response.status_code == 201
        book = response.json()
        assert book["id"] is not None
        assert book["description"] is None
        assert book["year"] is None


class TestDeleteBook:
    def test_delete_book_not_found(self, client):
        response = client.delete("/books/999")
        assert response.status_code == 404

    def test_delete_book_success(self, client):
        create_response = client.post(
            "/books", json={"title": "To Delete", "author": "Author"}
        )
        book_id = create_response.json()["id"]

        response = client.delete(f"/books/{book_id}")
        assert response.status_code == 204

        response = client.get(f"/books/{book_id}")
        assert response.status_code == 404

    def test_delete_only_affects_target(self, client):
        response1 = client.post(
            "/books", json={"title": "Book 1", "author": "Author"}
        )
        response2 = client.post(
            "/books", json={"title": "Book 2", "author": "Author"}
        )
        book1_id = response1.json()["id"]
        book2_id = response2.json()["id"]

        client.delete(f"/books/{book1_id}")

        assert client.get(f"/books/{book1_id}").status_code == 404
        assert client.get(f"/books/{book2_id}").status_code == 200
