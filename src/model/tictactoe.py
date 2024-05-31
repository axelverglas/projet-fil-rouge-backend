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
        self.winner = None  # Add winner attribute

    def to_json(self):
        return {
            '_id': self._id,
            'player1_id': self.player1_id,
            'player2_id': self.player2_id,
            'board': self.board,
            'current_turn': self.current_turn,
            'state': self.state,
            'game_type': self.game_type,
            'winner': self.winner  # Include winner in JSON
        }

    @classmethod
    def from_dict(cls, data):
        game = cls(data['player1_id'], data['player2_id'])
        game._id = data['_id']
        game.board = data['board']
        game.current_turn = data['current_turn']
        game.state = data['state']
        game.game_type = data['game_type']
        game.winner = data.get('winner')  # Add winner attribute
        return game
