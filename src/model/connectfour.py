from bson import ObjectId

class ConnectFour:
    ROWS = 6
    COLUMNS = 7

    def __init__(self, player1_id, player2_id):
        self._id = str(ObjectId())
        self.player1_id = player1_id
        self.player2_id = player2_id
        self.board = [[''] * self.COLUMNS for _ in range(self.ROWS)]
        self.current_turn = player1_id
        self.state = 'waiting'
        self.game_type = 'connectfour'
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

    def make_move(self, player_id, column):
        if not 0 <= column < self.COLUMNS or self.board[0][column] != "":
            raise ValueError("Invalid move")

        for row in reversed(range(self.ROWS)):
            if self.board[row][column] == "":
                self.board[row][column] = "X" if player_id == self.player1_id else "O"
                break

    def switch_turn(self):
        self.current_turn = self.player2_id if self.current_turn == self.player1_id else self.player1_id

    def check_winner(self):
        for row in range(self.ROWS):
            for col in range(self.COLUMNS - 3):
                if self.board[row][col] == self.board[row][col + 1] == self.board[row][col + 2] == self.board[row][col + 3] and self.board[row][col] != "":
                    return self.board[row][col]
        for row in range(self.ROWS - 3):
            for col in range(self.COLUMNS):
                if self.board[row][col] == self.board[row + 1][col] == self.board[row + 2][col] == self.board[row + 3][col] and self.board[row][col] != "":
                    return self.board[row][col]
        for row in range(self.ROWS - 3):
            for col in range(self.COLUMNS - 3):
                if self.board[row][col] == self.board[row + 1][col + 1] == self.board[row + 2][col + 2] == self.board[row + 3][col + 3] and self.board[row][col] != "":
                    return self.board[row][col]
        for row in range(3, self.ROWS):
            for col in range(self.COLUMNS - 3):
                if self.board[row][col] == self.board[row - 1][col + 1] == self.board[row - 2][col + 2] == self.board[row - 3][col + 3] and self.board[row][col] != "":
                    return self.board[row][col]
        return None

    def get_player1_marker(self):
        return "X"
