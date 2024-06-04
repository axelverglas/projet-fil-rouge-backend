from db import mongo
from src.model.user import User

class UserRepository:
    def create_user(self, user):
        user_json = user.to_json(include_password=True)
        if self.find_user_by_email(user_json['email']):
            raise ValueError("Email already in use")
        mongo.db.users.insert_one(user_json)
        return user

    def find_user_by_email(self, email):
        user_data = mongo.db.users.find_one({'email': email})
        return User.from_dict(user_data) if user_data else None
    
    def find_user_by_id(self, user_id):
        return mongo.db.users.find_one({'_id': user_id})
    
    def find_user_by_username(self, username):
        user_data = mongo.db.users.find_one({'username': username})
        return user_data if user_data else None
    
    def update_user_avatar(self, user_id, avatar_file_name):
        mongo.db.users.update_one({'_id': user_id}, {'$set': {'avatar': avatar_file_name}})