from flask_socketio import SocketIO, join_room, leave_room
from flask_socketio import emit
from src.service.game_service import GameService
from src.repository.game_repository import GameRepository

game_repository = GameRepository()
game_service = GameService(game_repository)


socketio = SocketIO()

@socketio.on('join_game')
def on_join_game(data):
    user_id = data.get('user_id')
    game_id = data.get('game_id')
    if not user_id or not game_id:
        return False, "user_id and game_id are required"

    print(f"User {user_id} joining game {game_id}")
    join_room(game_id)
    try:
        game = game_service.get_game(game_id)
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

    if not all([game_id, player_id, move is not None]):
        emit('error', {'message': 'Missing game_id, player_id, or move'})
        return

    try:
        move = int(move)
        game = game_service.make_move(game_id, player_id, move)
        emit('game_update', game.to_json(), room=game_id)
    except ValueError as e:
        emit('error', {'message': str(e)}, room=game_id)


@socketio.on('leave_game')
def on_leave_game(data):
    user_id = data.get('user_id')
    game_id = data.get('game_id')
    print(f"User {user_id} leaving game {game_id}")
    leave_room(game_id)
    socketio.emit('left_game', {'message': 'You have left the game'}, room=user_id)