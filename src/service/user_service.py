from src.model.user import User

class UserService:
    def __init__(self, user_repository, auth_service):
        self.user_repository = user_repository
        self.auth_service = auth_service

    def register_user(self, username, email, password):
        if self.user_repository.find_user_by_email(email):
            raise ValueError("Email already in use")
        if self.user_repository.find_user_by_username(username):
            raise ValueError("Username already in use")
        password_hashed = self.auth_service.hash_password(password)
        user = User(username, email, password_hashed)
        return self.user_repository.create_user(user)
    
    def get_user(self, user_id):
       user_data = self.user_repository.find_user_by_id(user_id)
       if not user_data:
              raise ValueError("User not found")
       user = User(user_data['username'], user_data['email'], user_data['password'], user_data.get('avatar', None))
       user._id = user_data['_id']
       return user
    
    def update_user_avatar(self, user_id, avatar_file_name):
        user = self.user_repository.find_user_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        return self.user_repository.update_user_avatar(user_id, avatar_file_name)