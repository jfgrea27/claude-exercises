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
        response1 = client.post("/books", json={"title": "Book 1", "author": "Author"})
        response2 = client.post("/books", json={"title": "Book 2", "author": "Author"})
        book1_id = response1.json()["id"]
        book2_id = response2.json()["id"]

        client.delete(f"/books/{book1_id}")

        assert client.get(f"/books/{book1_id}").status_code == 404
        assert client.get(f"/books/{book2_id}").status_code == 200


class TestPatchBook:
    def test_patch_book_not_found(self, client):
        response = client.patch("/books/999", json={"title": "Updated"})
        assert response.status_code == 404
        assert response.json()["detail"] == "Book not found"

    def test_patch_single_field(self, client):
        create_response = client.post(
            "/books",
            json={"title": "Original", "author": "Author", "year": 2020},
        )
        book_id = create_response.json()["id"]

        response = client.patch(f"/books/{book_id}", json={"title": "Updated"})
        assert response.status_code == 200
        book = response.json()
        assert book["title"] == "Updated"
        assert book["author"] == "Author"
        assert book["year"] == 2020

    def test_patch_multiple_fields(self, client):
        create_response = client.post(
            "/books",
            json={"title": "Original", "author": "Author"},
        )
        book_id = create_response.json()["id"]

        response = client.patch(
            f"/books/{book_id}",
            json={"title": "New Title", "author": "New Author", "year": 2024},
        )
        assert response.status_code == 200
        book = response.json()
        assert book["title"] == "New Title"
        assert book["author"] == "New Author"
        assert book["year"] == 2024

    def test_patch_empty_body(self, client):
        create_response = client.post(
            "/books",
            json={"title": "Original", "author": "Author"},
        )
        book_id = create_response.json()["id"]

        response = client.patch(f"/books/{book_id}", json={})
        assert response.status_code == 200
        book = response.json()
        assert book["title"] == "Original"
        assert book["author"] == "Author"


class TestBookType:
    def test_get_book_returns_book_type(self, client):
        create_response = client.post(
            "/books", json={"title": "Test Book", "author": "Author"}
        )
        book_id = create_response.json()["id"]

        response = client.get(f"/books/{book_id}")
        assert response.status_code == 200
        book = response.json()
        assert "book_type" in book
        assert book["book_type"] == "unknown"

    def test_create_book_with_book_type(self, client):
        response = client.post(
            "/books",
            json={"title": "Fiction Book", "author": "Author", "book_type": "fiction"},
        )
        assert response.status_code == 201
        book = response.json()
        assert book["book_type"] == "fiction"

    def test_create_book_without_book_type_defaults_to_unknown(self, client):
        response = client.post(
            "/books",
            json={"title": "No Type Book", "author": "Author"},
        )
        assert response.status_code == 201
        book = response.json()
        assert book["book_type"] == "unknown"

    def test_patch_book_type(self, client):
        create_response = client.post(
            "/books", json={"title": "Test Book", "author": "Author"}
        )
        book_id = create_response.json()["id"]
        assert create_response.json()["book_type"] == "unknown"

        response = client.patch(f"/books/{book_id}", json={"book_type": "non_fiction"})
        assert response.status_code == 200
        book = response.json()
        assert book["book_type"] == "non_fiction"

    def test_get_books_returns_book_type_in_list(self, client):
        client.post(
            "/books",
            json={"title": "Book 1", "author": "Author", "book_type": "fiction"},
        )
        client.post(
            "/books",
            json={"title": "Book 2", "author": "Author", "book_type": "non_fiction"},
        )

        response = client.get("/books")
        assert response.status_code == 200
        books = response.json()
        assert len(books) == 2
        book_types = {b["book_type"] for b in books}
        assert book_types == {"fiction", "non_fiction"}
