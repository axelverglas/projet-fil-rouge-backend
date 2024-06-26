import bcrypt
import jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

from src.model.user import User

load_dotenv()

secret_key = os.getenv('JWT_SECRET_KEY')

class AuthService:
    def __init__(self, user_repository):
        self.user_repository = user_repository

    def hash_password(self, password):
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')

    def verify_password(self, password, hashed):
        hashed_bytes = hashed.encode('utf-8')
        return bcrypt.checkpw(password.encode('utf-8'), hashed_bytes)

    def authenticate_user(self, email, password):
        user_data = self.user_repository.find_user_by_email(email)
        if user_data is None:
            raise ValueError("No user found with the provided email.")
        elif not self.verify_password(password, user_data.password):
            raise ValueError("Invalid password.")
        else:
            return user_data
        
    def generate_tokens(self, user_id):
        access_token = jwt.encode({
            'user_id': str(user_id),
            'exp': datetime.utcnow() + timedelta(minutes=30)
        }, secret_key, algorithm='HS256')

        refresh_token = jwt.encode({
            'user_id': str(user_id),
            'exp': datetime.utcnow() + timedelta(days=7)
        }, secret_key, algorithm='HS256')

        return access_token, refresh_token

    def refresh_access_token(self, refresh_token):
        try:
            payload = jwt.decode(refresh_token, secret_key, algorithms=['HS256'])
            user_id = payload['user_id']

            user_data = self.user_repository.find_user_by_id(user_id)
            if not user_data:
                raise ValueError("User not found")

            new_access_token, new_refresh_token = self.generate_tokens(user_id)

            user = User.from_dict(user_data)

            user_json = user.to_json(include_avatar_url=True)

            return new_access_token, new_refresh_token, user_json
        except jwt.ExpiredSignatureError:
            raise ValueError("Refresh token expired. Please log in again.")
        except jwt.InvalidTokenError:
            raise ValueError("Invalid refresh token. Please log in again.")
