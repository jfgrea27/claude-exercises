from books_api.db.users import (
    create_user,
    delete_user,
    get_all_users,
    get_user_by_id,
    update_user,
)


class TestGetAllUsers:
    def test_empty_database(self, db_session):
        users = get_all_users(db_session)
        assert users == []

    def test_returns_all_users(self, db_session):
        create_user(db_session, {"name": "User 1", "email": "user1@example.com"})
        create_user(db_session, {"name": "User 2", "email": "user2@example.com"})

        users = get_all_users(db_session)
        assert len(users) == 2


class TestGetUserById:
    def test_user_not_found(self, db_session):
        user = get_user_by_id(db_session, 999)
        assert user is None

    def test_user_found(self, db_session):
        created = create_user(db_session, {"name": "Test", "email": "test@example.com"})

        user = get_user_by_id(db_session, created.id)
        assert user is not None
        assert user.id == created.id
        assert user.name == "Test"


class TestCreateUser:
    def test_create_user(self, db_session):
        user = create_user(
            db_session, {"name": "John Doe", "email": "john@example.com"}
        )

        assert user.id is not None
        assert user.name == "John Doe"
        assert user.email == "john@example.com"

    def test_user_persisted(self, db_session):
        created = create_user(
            db_session, {"name": "Jane Doe", "email": "jane@example.com"}
        )

        fetched = get_user_by_id(db_session, created.id)
        assert fetched is not None
        assert fetched.name == "Jane Doe"

    def test_cannot_create_duplicate_email(self, db_session):
        from sqlalchemy.exc import IntegrityError

        create_user(db_session, {"name": "User 1", "email": "same@example.com"})

        try:
            create_user(db_session, {"name": "User 2", "email": "same@example.com"})
            assert False, "Expected IntegrityError but no exception was raised"
        except IntegrityError:
            db_session.rollback()


class TestUpdateUser:
    def test_update_single_field(self, db_session):
        user = create_user(
            db_session, {"name": "Original", "email": "original@example.com"}
        )

        updated = update_user(db_session, user, {"name": "Updated"})

        assert updated.name == "Updated"
        assert updated.email == "original@example.com"

    def test_update_all_fields(self, db_session):
        user = create_user(
            db_session, {"name": "Original", "email": "original@example.com"}
        )

        updated = update_user(
            db_session, user, {"name": "New Name", "email": "new@example.com"}
        )

        assert updated.name == "New Name"
        assert updated.email == "new@example.com"

    def test_update_persisted(self, db_session):
        user = create_user(
            db_session, {"name": "Original", "email": "original@example.com"}
        )
        update_user(db_session, user, {"name": "Updated"})

        fetched = get_user_by_id(db_session, user.id)
        assert fetched.name == "Updated"


class TestDeleteUser:
    def test_delete_user(self, db_session):
        user = create_user(
            db_session, {"name": "To Delete", "email": "delete@example.com"}
        )

        delete_user(db_session, user)

        assert get_user_by_id(db_session, user.id) is None

    def test_delete_only_target_user(self, db_session):
        user1 = create_user(
            db_session, {"name": "User 1", "email": "user1@example.com"}
        )
        user2 = create_user(
            db_session, {"name": "User 2", "email": "user2@example.com"}
        )

        delete_user(db_session, user1)

        assert get_user_by_id(db_session, user1.id) is None
        assert get_user_by_id(db_session, user2.id) is not None
