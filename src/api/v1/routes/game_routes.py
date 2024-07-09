from flask import Blueprint, request, jsonify
from src.service.user_service import UserService
from src.decorators.token_required import token_required
from src.service.queue_service import QueueService
from src.service.game_service import GameService
from src.repository.queue_repository import QueueRepository
from src.repository.game_repository import GameRepository
from src.repository.user_repository import UserRepository
from src.service.auth_service import AuthService
from src.socket_events import socketio

queue_repository = QueueRepository()
game_repository = GameRepository()
user_repository = UserRepository()
auth_service = AuthService(user_repository)
user_service = UserService(user_repository, auth_service)  # Ajout de auth_service ici
game_service = GameService(game_repository)
queue_service = QueueService(queue_repository, game_service)

games_bp = Blueprint('games_bp', __name__)

@games_bp.route('/queue', methods=['POST'])
def join_queue():
    data = request.get_json()
    user_id = data.get('user_id')
    game_type = data.get('game_type')

    if not user_id or not game_type:
        return jsonify({"error": "user_id and game_type are required"}), 400

    game_id, opponent_id = queue_service.find_or_create_game(user_id, game_type)

    if game_id:
        game = game_service.get_game(game_id, game_type)
        game.state = "ongoing"
        game_service.update_game(game)
        socketio.emit('game_start', {'game_id': game_id, 'opponent_id': opponent_id, 'game_type': game_type}, room=game_id)
        socketio.emit('game_ready', {'game_id': game_id, 'user_id_1': user_id, 'user_id_2': opponent_id, 'game_type': game_type})
        return jsonify({"game_id": game_id, "opponent_id": opponent_id}), 201
    else:
        return jsonify({"message": "Added to queue"}), 200

@games_bp.route('/<game_type>/<game_id>', methods=['GET'])
def get_game(game_type, game_id):
    try:
        game = game_service.get_game(game_id, game_type)
        return jsonify(game.to_json()), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404

@games_bp.route('/<game_type>/<game_id>/move', methods=['PUT'])
def make_move(game_type, game_id):
    data = request.get_json()
    player_id = data.get('player_id')
    move = data.get('move')
    
    try:
        game = game_service.make_move(game_id, player_id, move, game_type)
        return jsonify(game.to_json()), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@games_bp.route('/<game_type>/<game_id>/opponent', methods=['GET'])
@token_required
def get_opponent(game_type, game_id):
    user_id = request.args.get('user_id')
    
    if not user_id:
        return jsonify({"error": "user_id is required"}), 400
    
    try:
        game = game_service.get_game(game_id, game_type)
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

@games_bp.route('/<game_type>/<game_id>/pause', methods=['PUT'])
@token_required
def pause_game(game_type, game_id):
    try:
        game = game_service.get_game(game_id, game_type)
        if game.state != 'finished':
            game.state = 'paused'
            game_service.update_game(game)
            return jsonify({"message": "Game paused"}), 200
        return jsonify({"error": "Game already finished"}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@games_bp.route('/<game_type>/<game_id>/finish', methods=['PUT'])
@token_required
def finish_game(game_type, game_id):
    try:
        game = game_service.get_game(game_id, game_type)
        if game.state != 'finished':
            game.state = 'finished'
            game_service.update_game(game)
            return jsonify({"message": "Game finished"}), 200
        return jsonify({"error": "Game already finished"}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
