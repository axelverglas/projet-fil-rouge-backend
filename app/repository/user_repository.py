from ...db import get_db

class UserRepository:
    def __init__(self, db):
        self.db = get_db()

    def create_user(self, user):
        user_json = user.to_json()
        if self.find_user_by_email(user_json['email']):
            raise ValueError("Email already in use")
        self.db.users.insert_one(user_json)
        return user_json

    def find_user_by_email(self, email):
        return self.db.users.find_one({'email': email})