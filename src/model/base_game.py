from abc import ABC, abstractmethod
from bson import ObjectId

class BaseGame(ABC):
    def __init__(self, player1_id, player2_id, game_type):
        self._id = str(ObjectId())
        self.player1_id = player1_id
        self.player2_id = player2_id
        self.current_turn = player1_id
        self.state = 'waiting'
        self.game_type = game_type
        self.winner = None

    @abstractmethod
    def to_json(self):
        pass

    @abstractmethod
    def from_dict(self, data):
        pass

    @abstractmethod
    def make_move(self, player_id, move):
        pass
