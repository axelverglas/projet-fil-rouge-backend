from flask import Blueprint, request, jsonify
from src.service.friendship_service import FriendshipService
from src.decorators.token_required import token_required
from src.repository.friendship_repository import FriendshipRepository
from src.repository.user_repository import UserRepository

user_repository = UserRepository()
friendship_repository = FriendshipRepository()
friendship_service = FriendshipService(friendship_repository, user_repository)

friendship_blueprint = Blueprint('friendship', __name__)

@friendship_blueprint.route('/send-request', methods=['POST'])
@token_required
def send_friend_request():
    data = request.get_json()
    creator_id = data.get('creatorId')
    receiver_id = data.get('receiverId')

    if not creator_id or not receiver_id:
        return jsonify({"error": "Creator ID and Receiver ID are required"}), 400

    try:
        friend_request = friendship_service.send_friend_request(creator_id, receiver_id)
        return jsonify(friend_request.to_dict()), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@friendship_blueprint.route('/accept-request', methods=['POST'])
@token_required
def accept_friend_request():
    data = request.get_json()
    creator_id = data.get('creatorId')
    receiver_id = data.get('receiverId')

    if not creator_id or not receiver_id:
        return jsonify({"error": "Creator ID and Receiver ID are required"}), 400

    try:
        friendship = friendship_service.accept_friend_request(creator_id, receiver_id)
        return jsonify(friendship.to_dict()), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@friendship_blueprint.route('/<user_id>/friends', methods=['GET'])
@token_required
def get_friends(user_id):
    try:
        friends = friendship_service.get_friends(user_id)
        return jsonify([friend.to_dict() for friend in friends]), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@friendship_blueprint.route('/are-friends', methods=['GET'])
@token_required
def are_friends():
    creator_id = request.args.get('creatorId')
    receiver_id = request.args.get('receiverId')

    if not creator_id or not receiver_id:
        return jsonify({"error": "Creator ID and Receiver ID are required"}), 400

    try:
        friendship_status = friendship_service.are_friends(creator_id, receiver_id)
        return jsonify(friendship_status), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@friendship_blueprint.route('/<user_id>/sent-requests', methods=['GET'])
@token_required
def get_sent_requests(user_id):
    try:
        sent_requests = friendship_service.get_sent_requests(user_id)
        return jsonify([{
            "request": request.to_dict(),
            "user": user_repository.find_user_by_id(request.receiver_id)
        } for request in sent_requests]), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@friendship_blueprint.route('/<user_id>/received-requests', methods=['GET'])
@token_required
def get_received_requests(user_id):
    try:
        received_requests = friendship_service.get_received_requests(user_id)
        return jsonify([{
            "request": request.to_dict(),
            "user": user_repository.find_user_by_id(request.creator_id)
        } for request in received_requests]), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
