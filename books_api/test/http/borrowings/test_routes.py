class TestGetBorrowings:
    def test_get_borrowings_empty(self, client):
        response = client.get("/borrowings")
        assert response.status_code == 200
        assert response.json() == []

    def test_get_borrowings_with_data(self, client):
        # Create user and books first
        user_response = client.post(
            "/users", json={"name": "User", "email": "user@example.com"}
        )
        user_id = user_response.json()["id"]

        book1_response = client.post(
            "/books", json={"title": "Book 1", "author": "Author 1"}
        )
        book2_response = client.post(
            "/books", json={"title": "Book 2", "author": "Author 2"}
        )
        book1_id = book1_response.json()["id"]
        book2_id = book2_response.json()["id"]

        client.post("/borrowings", json={"user_id": user_id, "book_id": book1_id})
        client.post("/borrowings", json={"user_id": user_id, "book_id": book2_id})

        response = client.get("/borrowings")
        assert response.status_code == 200
        borrowings = response.json()
        assert len(borrowings) == 2

    def test_get_borrowings_filtered_by_user(self, client):
        user1_response = client.post(
            "/users", json={"name": "User 1", "email": "user1@example.com"}
        )
        user2_response = client.post(
            "/users", json={"name": "User 2", "email": "user2@example.com"}
        )
        user1_id = user1_response.json()["id"]
        user2_id = user2_response.json()["id"]

        book_response = client.post(
            "/books", json={"title": "Book", "author": "Author"}
        )
        book_id = book_response.json()["id"]

        client.post("/borrowings", json={"user_id": user1_id, "book_id": book_id})
        client.post("/borrowings", json={"user_id": user2_id, "book_id": book_id})

        response = client.get(f"/borrowings?user_id={user1_id}")
        assert response.status_code == 200
        borrowings = response.json()
        assert len(borrowings) == 1
        assert borrowings[0]["user_id"] == user1_id


class TestGetBorrowing:
    def test_get_borrowing_not_found(self, client):
        response = client.get("/borrowings/999")
        assert response.status_code == 404
        assert response.json()["detail"] == "Borrowing not found"

    def test_get_borrowing_success(self, client):
        user_response = client.post(
            "/users", json={"name": "User", "email": "user@example.com"}
        )
        book_response = client.post(
            "/books", json={"title": "Book", "author": "Author"}
        )
        user_id = user_response.json()["id"]
        book_id = book_response.json()["id"]

        create_response = client.post(
            "/borrowings", json={"user_id": user_id, "book_id": book_id}
        )
        borrowing_id = create_response.json()["id"]

        response = client.get(f"/borrowings/{borrowing_id}")
        assert response.status_code == 200
        borrowing = response.json()
        assert borrowing["id"] == borrowing_id
        assert borrowing["user_id"] == user_id
        assert borrowing["book_id"] == book_id


class TestCreateBorrowing:
    def test_create_new_borrowing(self, client):
        user_response = client.post(
            "/users", json={"name": "User", "email": "user@example.com"}
        )
        book_response = client.post(
            "/books", json={"title": "Book", "author": "Author"}
        )
        user_id = user_response.json()["id"]
        book_id = book_response.json()["id"]

        response = client.post(
            "/borrowings", json={"user_id": user_id, "book_id": book_id}
        )
        assert response.status_code == 201
        borrowing = response.json()
        assert borrowing["id"] is not None
        assert borrowing["user_id"] == user_id
        assert borrowing["book_id"] == book_id
        assert borrowing["borrowed_at"] is not None
        assert borrowing["returned_at"] is None

    def test_create_borrowing_user_not_found(self, client):
        book_response = client.post(
            "/books", json={"title": "Book", "author": "Author"}
        )
        book_id = book_response.json()["id"]

        response = client.post("/borrowings", json={"user_id": 999, "book_id": book_id})
        assert response.status_code == 404
        assert response.json()["detail"] == "User not found"

    def test_create_borrowing_book_not_found(self, client):
        user_response = client.post(
            "/users", json={"name": "User", "email": "user@example.com"}
        )
        user_id = user_response.json()["id"]

        response = client.post("/borrowings", json={"user_id": user_id, "book_id": 999})
        assert response.status_code == 404
        assert response.json()["detail"] == "Book not found"


class TestDeleteBorrowing:
    def test_delete_borrowing_not_found(self, client):
        response = client.delete("/borrowings/999")
        assert response.status_code == 404

    def test_delete_borrowing_success(self, client):
        user_response = client.post(
            "/users", json={"name": "User", "email": "user@example.com"}
        )
        book_response = client.post(
            "/books", json={"title": "Book", "author": "Author"}
        )
        user_id = user_response.json()["id"]
        book_id = book_response.json()["id"]

        create_response = client.post(
            "/borrowings", json={"user_id": user_id, "book_id": book_id}
        )
        borrowing_id = create_response.json()["id"]

        response = client.delete(f"/borrowings/{borrowing_id}")
        assert response.status_code == 204

        response = client.get(f"/borrowings/{borrowing_id}")
        assert response.status_code == 404


class TestReturnBook:
    def test_return_book_not_found(self, client):
        response = client.post("/borrowings/999/return")
        assert response.status_code == 404
        assert response.json()["detail"] == "Borrowing not found"

    def test_return_book_success(self, client):
        user_response = client.post(
            "/users", json={"name": "User", "email": "user@example.com"}
        )
        book_response = client.post(
            "/books", json={"title": "Book", "author": "Author"}
        )
        user_id = user_response.json()["id"]
        book_id = book_response.json()["id"]

        create_response = client.post(
            "/borrowings", json={"user_id": user_id, "book_id": book_id}
        )
        borrowing_id = create_response.json()["id"]

        response = client.post(f"/borrowings/{borrowing_id}/return")
        assert response.status_code == 200
        borrowing = response.json()
        assert borrowing["returned_at"] is not None

    def test_return_book_already_returned(self, client):
        user_response = client.post(
            "/users", json={"name": "User", "email": "user@example.com"}
        )
        book_response = client.post(
            "/books", json={"title": "Book", "author": "Author"}
        )
        user_id = user_response.json()["id"]
        book_id = book_response.json()["id"]

        create_response = client.post(
            "/borrowings", json={"user_id": user_id, "book_id": book_id}
        )
        borrowing_id = create_response.json()["id"]

        client.post(f"/borrowings/{borrowing_id}/return")
        response = client.post(f"/borrowings/{borrowing_id}/return")
        assert response.status_code == 400
        assert response.json()["detail"] == "Book already returned"
