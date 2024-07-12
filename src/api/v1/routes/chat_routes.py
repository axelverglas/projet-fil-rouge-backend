from flask import Blueprint, request, jsonify
from src.repository.user_repository import UserRepository
from src.repository.notification_repository import NotificationRepository
from src.service.chat_service import ChatService
from src.repository.chat_repository import ChatRepository
from src.socket_events import socketio

chat_repository = ChatRepository()
notification_repository = NotificationRepository()
user_repository = UserRepository()
chat_service = ChatService(chat_repository, notification_repository, user_repository)

chat_bp = Blueprint('chat_bp', __name__)

@chat_bp.route('/<user1_id>/<user2_id>', methods=['GET'])
def get_conversation(user1_id, user2_id):
    conversation = chat_service.get_conversation(user1_id, user2_id)
    if conversation:
        return jsonify(conversation.to_json()), 200
    else:
        return jsonify({'error': 'Conversation introuvable !'}), 404

@chat_bp.route('/messages', methods=['POST'])
def send_message():
    data = request.get_json()
    sender_id = data['sender_id']
    receiver_id = data['receiver_id']
    content = data['content']
    conversation_id = data['conversation_id']

    message = chat_service.send_message(sender_id, receiver_id, content, conversation_id)
    socketio.emit('new_message', message.to_json(), room=conversation_id)
    return jsonify(message.to_json()), 201

