from flask_pymongo import ObjectId
from datetime import datetime

class User:
    def __init__(self, username, email, password):
        self._id = ObjectId()
        self.username = username
        self.email = email
        self.password = password
        self.avatar = None
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        
    
    def to_json(self):
        user_json = {
            "_id": str(self._id),
            "username": self.username,
            "email": self.email,
            "avatar": self.avatar,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
        return user_json
