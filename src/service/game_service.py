from src.model.tictactoe import TicTacToe
from src.model.connectfour import ConnectFour

class GameService:
    def __init__(self, game_repository):
        self.game_repository = game_repository

    def create_game(self, player1_id, player2_id, game_type):
        if game_type == "tictactoe":
            game = TicTacToe(player1_id, player2_id)
        elif game_type == "connectfour":
            game = ConnectFour(player1_id, player2_id)
        else:
            raise ValueError("Unsupported game type")
        
        created_game = self.game_repository.create_game(game)
        game._id = created_game
        print(f"Game created: {game.to_json()}")
        return game

    def get_game(self, game_id, game_type):
        game_data = self.game_repository.find_game_by_id(game_id)
        if not game_data:
            raise ValueError("Game not found")
        if game_type == "tictactoe":
            return TicTacToe.from_dict(game_data)
        elif game_type == "connectfour":
            return ConnectFour.from_dict(game_data)
        else:
            raise ValueError("Unsupported game type")

    def update_game(self, game):
        self.game_repository.update_game(game)

    def make_move(self, game_id, player_id, move, game_type):
        game_data = self.game_repository.find_game_by_id(game_id)
        if not game_data:
            raise ValueError("Game not found")
        if game_type == "tictactoe":
            game = TicTacToe.from_dict(game_data)
            game.make_move(player_id, move)
        elif game_type == "connectfour":
            game = ConnectFour.from_dict(game_data)
            game.make_move(player_id, move)
        else:
            raise ValueError("Unsupported game type")

        if game.state == 'finished':
            raise ValueError("Game is already finished")

        if game.current_turn != player_id:
            raise ValueError("Not your turn")

        winner = game.check_winner()
        if winner:
            game.state = "finished"
            game.winner = game.player1_id if winner == game.get_player1_marker() else game.player2_id
        else:
            game.switch_turn()

        self.update_game(game)
        return game

    def find_ongoing_game_by_user(self, user_id: str, game_type: str):
        return self.game_repository.find_one({
            '$or': [{'player1_id': user_id}, {'player2_id': user_id}],
            'state': 'ongoing',
            'game_type': game_type
        })
