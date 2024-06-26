import jwt
from flask import request, jsonify, g
from functools import wraps
from src.repository.user_repository import UserRepository
import os

secret_key = os.getenv('JWT_SECRET_KEY')

user_repository = UserRepository()

def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, secret_key, algorithms=["HS256"])
            current_user = user_repository.find_user_by_id(data['user_id'])
            if not current_user:
                return jsonify({'message': 'User not found!'}), 401
        except Exception as e:
            return jsonify({'message': 'Token is invalid!', 'error': str(e)}), 401

        return f(*args, **kwargs)
    return decorated_function
