from flask_pymongo import ObjectId
from datetime import datetime

class User:
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow() 
        
    
    def to_json(self):
        user_json = {
            "_id": ObjectId(),
            "username": self.username,
            "email": self.email,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
        return user_json
