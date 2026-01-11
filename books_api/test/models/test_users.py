from books_api.models.users import User


class TestUserModel:
    def test_user_has_required_attributes(self):
        user = User(id=1, name="John Doe", email="john@example.com")
        assert user.id == 1
        assert user.name == "John Doe"
        assert user.email == "john@example.com"
