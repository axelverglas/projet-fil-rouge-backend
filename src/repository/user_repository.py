from db import mongo

class UserRepository:
    def create_user(self, user):
        user_json = user.to_json()
        if self.find_user_by_email(user_json['email']):
            raise ValueError("Email already in use")
        mongo.db.users.insert_one(user_json)
        return user

    def find_user_by_email(self, email):
        return mongo.db.users.find_one({'email': email})