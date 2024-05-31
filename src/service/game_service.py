from src.model.tictactoe import TicTacToe

class GameService:
    def __init__(self, game_repository):
        self.game_repository = game_repository

    def create_game(self, player1_id, player2_id):
        game = TicTacToe(player1_id, player2_id)
        return self.game_repository.create_game(game)

    def get_game(self, game_id):
        game_data = self.game_repository.find_game_by_id(game_id)
        if not game_data:
            raise ValueError("Game not found")
        return TicTacToe.from_dict(game_data)

    def update_game(self, game):
        self.game_repository.update_game(game)

    def make_move(self, game_id, player_id, move):
        game_data = self.game_repository.find_game_by_id(game_id)
        if not game_data:
            raise ValueError("Game not found")

        game = TicTacToe.from_dict(game_data)

        if game.state == 'finished':
            raise ValueError("Game is already finished")

        if game.current_turn != player_id:
            raise ValueError("Not your turn")

        if not 0 <= move < len(game.board) or game.board[move] != "":
            raise ValueError("Invalid move")

        game.board[move] = "X" if player_id == game.player1_id else "O"
        winner = self.check_winner(game.board)
        if winner:
            game.state = "finished"
            game.winner = game.player1_id if winner == "X" else game.player2_id
        else:
            game.current_turn = game.player2_id if player_id == game.player1_id else game.player1_id

        self.update_game(game)
        return game

    def check_winner(self, board):
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
            [0, 4, 8], [2, 4, 6]              # diagonals
        ]

        for combo in winning_combinations:
            if board[combo[0]] == board[combo[1]] == board[combo[2]] and board[combo[0]] != "":
                return board[combo[0]]
        return None