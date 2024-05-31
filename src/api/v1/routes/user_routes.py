from flask import request, jsonify, Blueprint
from src.repository.user_repository import UserRepository
from src.service.auth_service import AuthService
from src.service.upload_service import UploadService
from src.service.user_service import UserService
from src.decorators.token_required import token_required
import uuid
import io
from PIL import Image

user_repository = UserRepository()
auth_service = AuthService(user_repository)
user_service = UserService(user_repository, auth_service)
upload_service = UploadService()

user_blueprint = Blueprint('user', __name__)

@user_blueprint.route('', methods=['POST'])
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

@user_blueprint.route('/<user_id>', methods=['GET'])
@token_required
def get_user(user_id):
    user = user_service.get_user(str(user_id))
    if user:
        return jsonify(user), 200
    return jsonify({"error": "User not found"}), 404

@user_blueprint.route('/<user_id>/avatar', methods=['POST'])
@token_required
def update_profile(user_id):
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file:
        image = Image.open(file.stream)
        webp_filename = f"avatars/{uuid.uuid4()}.webp"
        in_mem_file = io.BytesIO()
        image.save(in_mem_file, format='WebP')
        in_mem_file.seek(0)

        success = upload_service.upload_file(webp_filename, in_mem_file)
        if success:
            try:
                user_service.update_user_avatar(user_id, webp_filename)
                return jsonify({"message": "Profile updated successfully", "filename": webp_filename}), 200
            except ValueError as e:
                return jsonify({"error": str(e)}), 404
        else:
            return jsonify({"error": "Upload failed"}), 500
