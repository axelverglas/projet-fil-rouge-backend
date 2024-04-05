from flask_pymongo import ObjectId
from datetime import datetime

from src.service.upload_service import UploadService

upload_service = UploadService()

class User:
    def __init__(self, username, email, password, avatar=None):
        self._id = ObjectId()
        self.username = username
        self.email = email
        self.password = password
        self.avatar = avatar
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
    
    def to_json(self, include_avatar_url=False):
        user_json = {
            "_id": str(self._id),
            "username": self.username,
            "email": self.email,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
        if self.avatar and include_avatar_url:
            user_json['avatar_url'] = upload_service.get_file_url(f"{self.avatar}")
        return user_json

