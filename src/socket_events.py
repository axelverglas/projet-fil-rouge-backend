from flask_socketio import SocketIO, join_room, leave_room, emit
from src.repository.user_repository import UserRepository
from src.service.notification_service import NotificationService
from src.service.game_service import GameService
from src.repository.game_repository import GameRepository
from src.service.chat_service import ChatService
from src.repository.chat_repository import ChatRepository
from src.repository.notification_repository import NotificationRepository

chat_repository = ChatRepository()
notification_repository =  NotificationRepository()
user_repository = UserRepository()
chat_service = ChatService(chat_repository, notification_repository, user_repository)
game_repository = GameRepository()
game_service = GameService(game_repository)

socketio = SocketIO()

@socketio.on('join_conversation')
def on_join_conversation(data):
    user1_id = data.get('user1_id')
    user2_id = data.get('user2_id')

    # Check if both user IDs are provided
    if not user1_id or not user2_id:
        return emit('error', {'message': 'user1_id and user2_id are required'})

    # Check if the conversation exists, if not create it
    conversation = chat_service.get_conversation(user1_id, user2_id)
    conversation_id = conversation._id

    # Join the room associated with the conversation
    join_room(conversation_id)

    emit('conversation_joined', {'conversation_id': conversation_id})

@socketio.on('new_message')
def on_new_message(data):
    message = chat_service.send_message(data['sender_id'], data['receiver_id'], data['content'], data['conversation_id'])
    emit('new_message', message.to_json(), room=data['conversation_id'])

    NotificationService.create_notification(data['receiver_id'], 'Tu as un nouveau message !')

@socketio.on('join_game')
def on_join_game(data):
    user_id = data.get('user_id')
    game_id = data.get('game_id')
    game_type = data.get('game_type')
    if not user_id or not game_id or not game_type:
        return False, "user_id, game_id, and game_type are required"

    print(f"User {user_id} joining game {game_id}")
    join_room(game_id)
    try:
        game = game_service.get_game(game_id, game_type)
        if game.player1_id == user_id or game.player2_id == user_id:
            socketio.emit('game_start', {'game_id': game_id}, room=game_id)
        else:
            return False, "User not part of this game"
    except ValueError as e:
        print(f"Error retrieving game: {e}")
        return False, str(e)

@socketio.on('make_move')
def on_make_move(data):
    print(data)
    game_id = data.get('game_id')
    player_id = data.get('player_id')
    move = data.get('move')
    game_type = data.get('game_type')

    if not all([game_id, player_id, move is not None, game_type]):
        emit('error', {'message': 'Missing game_id, player_id, move, or game_type'})
        return

    try:
        move = int(move)
        game = game_service.make_move(game_id, player_id, move, game_type)
        emit('game_update', game.to_json(), room=game_id)
    except ValueError as e:
        emit('error', {'message': str(e)}, room=game_id)
