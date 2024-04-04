from src.model.user import User

class UserService:
    def __init__(self, user_repository, auth_service):
        self.user_repository = user_repository
        self.auth_service = auth_service

    def register_user(self, username, email, password):
        if self.user_repository.find_user_by_email(email):
            raise ValueError("Email already in use")
        password_hashed = self.auth_service.hash_password(password)
        user = User(username, email, password_hashed)
        return self.user_repository.create_user(user)