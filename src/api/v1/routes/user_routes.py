from flask import request, jsonify, Blueprint
from src.repository.user_repository import UserRepository
from src.service.auth_service import AuthService
from src.service.user_service import UserService

user_repository = UserRepository()
auth_service = AuthService(user_repository)
user_service = UserService(user_repository, auth_service)

user_blueprint = Blueprint('user', __name__)

@user_blueprint.route('/', methods=['POST'])
def register():
    data = request.get_json()
    try:
        user = user_service.register_user(data['username'], data['email'], data['password'])
        access_token, refresh_token = auth_service.generate_tokens(str(user._id))
        user_data = user.to_json()
        return jsonify({
            "user": user_data,
            "access_token": access_token,
            "refresh_token": refresh_token
        }), 201
        
    except ValueError as e:
        return jsonify({"error": str(e)}), 400