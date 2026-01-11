class TestGetUsers:
    def test_get_users_empty(self, client):
        response = client.get("/users")
        assert response.status_code == 200
        assert response.json() == []

    def test_get_users_with_data(self, client):
        client.post("/users", json={"name": "User 1", "email": "user1@example.com"})
        client.post("/users", json={"name": "User 2", "email": "user2@example.com"})

        response = client.get("/users")
        assert response.status_code == 200
        users = response.json()
        assert len(users) == 2


class TestGetUser:
    def test_get_user_not_found(self, client):
        response = client.get("/users/999")
        assert response.status_code == 404
        assert response.json()["detail"] == "User not found"

    def test_get_user_success(self, client):
        create_response = client.post(
            "/users", json={"name": "Test User", "email": "test@example.com"}
        )
        user_id = create_response.json()["id"]

        response = client.get(f"/users/{user_id}")
        assert response.status_code == 200
        user = response.json()
        assert user["id"] == user_id
        assert user["name"] == "Test User"
        assert user["email"] == "test@example.com"


class TestCreateUser:
    def test_create_new_user(self, client):
        response = client.post(
            "/users",
            json={"name": "New User", "email": "new@example.com"},
        )
        assert response.status_code == 201
        user = response.json()
        assert user["id"] is not None
        assert user["name"] == "New User"
        assert user["email"] == "new@example.com"


class TestDeleteUser:
    def test_delete_user_not_found(self, client):
        response = client.delete("/users/999")
        assert response.status_code == 404

    def test_delete_user_success(self, client):
        create_response = client.post(
            "/users", json={"name": "To Delete", "email": "delete@example.com"}
        )
        user_id = create_response.json()["id"]

        response = client.delete(f"/users/{user_id}")
        assert response.status_code == 204

        response = client.get(f"/users/{user_id}")
        assert response.status_code == 404


class TestPatchUser:
    def test_patch_user_not_found(self, client):
        response = client.patch("/users/999", json={"name": "Updated"})
        assert response.status_code == 404
        assert response.json()["detail"] == "User not found"

    def test_patch_single_field(self, client):
        create_response = client.post(
            "/users",
            json={"name": "Original", "email": "original@example.com"},
        )
        user_id = create_response.json()["id"]

        response = client.patch(f"/users/{user_id}", json={"name": "Updated"})
        assert response.status_code == 200
        user = response.json()
        assert user["name"] == "Updated"
        assert user["email"] == "original@example.com"

    def test_patch_multiple_fields(self, client):
        create_response = client.post(
            "/users",
            json={"name": "Original", "email": "original@example.com"},
        )
        user_id = create_response.json()["id"]

        response = client.patch(
            f"/users/{user_id}",
            json={"name": "New Name", "email": "new@example.com"},
        )
        assert response.status_code == 200
        user = response.json()
        assert user["name"] == "New Name"
        assert user["email"] == "new@example.com"
