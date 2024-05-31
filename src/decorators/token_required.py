import jwt
from flask import request, jsonify, g
from functools import wraps
from src.repository.user_repository import UserRepository
import os

secret_key = os.getenv('JWT_SECRET_KEY')

user_repository = UserRepository()

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # JWT is passed in the request header
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split()[1]
        # Return 401 if token is not passed
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            # Decoding the payload to fetch the stored details
            data = jwt.decode(token, secret_key, algorithms=["HS256"])
            current_user = user_repository.find_user_by_id(data['user_id'])
            if not current_user:
                return jsonify({'message': 'User not found!'}), 401
            g.current_user = current_user
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token!'}), 401

        return f(*args, **kwargs)

    return decorated
