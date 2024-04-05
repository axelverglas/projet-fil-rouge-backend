from flask import request, jsonify, Blueprint
from src.repository.user_repository import UserRepository
from src.service.auth_service import AuthService

user_repository = UserRepository()
auth_service = AuthService(user_repository)

auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    try:
        # user est maintenant une instance de User, pas un JSON
        user = auth_service.authenticate_user(data['email'], data['password'])
        access_token, refresh_token = auth_service.generate_tokens(str(user._id))
        # Convertissez l'instance User en JSON ici
        user_json = user.to_json(include_avatar_url=True)
        return jsonify({
            "user": user_json,
            "access_token": access_token,
            "refresh_token": refresh_token
        }), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 401

@auth_blueprint.route('/refresh-token', methods=['POST'])
def refresh_token():
    data = request.get_json()
    try:
        new_access_token, new_refresh_token, user_data = auth_service.refresh_access_token(data['refresh_token'])
        return jsonify({
            "access_token": new_access_token,
            "refresh_token": new_refresh_token,
            "user": user_data
        }), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 401
