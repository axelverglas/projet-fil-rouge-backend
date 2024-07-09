from bson import ObjectId

class TicTacToe:
    def __init__(self, player1_id, player2_id):
        self._id = str(ObjectId())
        self.player1_id = player1_id
        self.player2_id = player2_id
        self.board = [''] * 9
        self.current_turn = player1_id
        self.state = 'waiting'
        self.game_type = 'tictactoe'
        self.winner = None

    def to_json(self):
        return {
            '_id': self._id,
            'player1_id': self.player1_id,
            'player2_id': self.player2_id,
            'board': self.board,
            'current_turn': self.current_turn,
            'state': self.state,
            'game_type': self.game_type,
            'winner': self.winner
        }

    @classmethod
    def from_dict(cls, data):
        game = cls(data['player1_id'], data['player2_id'])
        game._id = data['_id']
        game.board = data['board']
        game.current_turn = data['current_turn']
        game.state = data['state']
        game.game_type = data['game_type']
        game.winner = data.get('winner')
        return game

    def make_move(self, player_id, position):
        if not 0 <= position < 9 or self.board[position] != "":
            raise ValueError("Invalid move")
        self.board[position] = "X" if player_id == self.player1_id else "O"

    def switch_turn(self):
        self.current_turn = self.player2_id if self.current_turn == self.player1_id else self.player1_id

    def check_winner(self):
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]
        for combo in winning_combinations:
            if self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] and self.board[combo[0]] != "":
                return self.board[combo[0]]
        return None

    def get_player1_marker(self):
        return "X"
