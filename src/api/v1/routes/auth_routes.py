from flask import request, jsonify, Blueprint
from src.repository.user_repository import UserRepository
from src.service.auth_service import AuthService

user_repository = UserRepository()
auth_service = AuthService(user_repository)

auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    try:
        user = auth_service.register_user(data['username'], data['email'], data['password'])
        access_token, refresh_token = auth_service.generate_tokens(str(user._id))
        user_data = user.to_json()
        return jsonify({
            "user": user_data,
            "access_token": access_token,
            "refresh_token": refresh_token
        }), 201
        
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@auth_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    try:
        user = auth_service.authenticate_user(data['email'], data['password'])
        access_token, refresh_token = auth_service.generate_tokens(user['_id'])
        user_data = user.to_json()
        return jsonify({
            "user": user_data,
            "access_token": access_token,
            "refresh_token": refresh_token
        }), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 401

@auth_blueprint.route('/token/refresh', methods=['POST'])
def refresh_token():
    data = request.get_json()
    try:
        new_access_token = auth_service.refresh_access_token(data['refresh_token'])
        return jsonify({"access_token": new_access_token}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 401