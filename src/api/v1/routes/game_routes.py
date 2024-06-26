from flask import Blueprint, request, jsonify
from src.decorators.token_required import token_required
from src.service.user_service import UserService
from src.service.queue_service import QueueService
from src.repository.queue_repository import QueueRepository
from src.service.game_service import GameService
from src.repository.game_repository import GameRepository
from src.repository.user_repository import UserRepository
from src.service.auth_service import AuthService
from src.socket_events import socketio

queue_repository = QueueRepository()
game_repository = GameRepository()
user_repository = UserRepository()
auth_service = AuthService(user_repository)
game_service = GameService(game_repository)
queue_service = QueueService(queue_repository, game_service)
user_service = UserService(user_repository, auth_service)

games_bp = Blueprint('games_bp', __name__)

@games_bp.route('/queue', methods=['POST'])
def join_queue():
    data = request.get_json()
    user_id = data.get('user_id')
    game_type = data.get('game_type')
    game_id, opponent_id = queue_service.find_or_create_game(user_id, game_type)

    if game_id:
        game = game_service.get_game(game_id)
        game.state = "ongoing"
        game_service.update_game(game)
        socketio.emit('game_start', {'game_id': game_id, 'opponent_id': opponent_id}, room=game_id)  # Notify both players
        socketio.emit('game_ready', {'game_id': game_id, 'user_id_1': user_id, 'user_id_2': opponent_id})  # Emit game_ready event
        return jsonify({"game_id": game_id, "opponent_id": opponent_id}), 201
    else:
        return jsonify({"message": "Added to queue"}), 200

@games_bp.route('/<game_type>/<game_id>', methods=['GET'])
def get_game(game_type, game_id):
    try:
        game = game_service.get_game(game_id)
        return jsonify(game.to_json()), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404

@games_bp.route('/tictactoe/<game_id>/move', methods=['PUT'])
def make_move(game_id):
    data = request.get_json()
    player_id = data.get('player_id')
    move = data.get('move')
    
    try:
        game = game_service.make_move(game_id, player_id, move)
        return jsonify(game.to_json()), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@games_bp.route('/<game_id>/opponent', methods=['GET'])
@token_required
def get_opponent(game_id):
    user_id = request.args.get('user_id')
    
    if not user_id:
        return jsonify({"error": "User ID is required"}), 400
    
    try:
        game = game_service.get_game(game_id)
        if game.player1_id == user_id:
            opponent_id = game.player2_id
        elif game.player2_id == user_id:
            opponent_id = game.player1_id
        else:
            return jsonify({"error": "User not part of this game"}), 403
        
        opponent = user_service.get_user(str(opponent_id))
        return jsonify(opponent), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
