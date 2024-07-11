class QueueRepository:
    def __init__(self):
        self.queues = {}

    def find_one(self, query):
        game_type = query.get('game_type')
        user_id = query.get('user_id')
        for player in self.queues.get(game_type, []):
            if player != user_id:
                return {'user_id': player, 'game_type': game_type}
        return None

    def get_next_player(self, game_type):
        if game_type in self.queues and self.queues[game_type]:
            return self.queues[game_type].pop(0)
        return None

    def add_to_queue(self, user_id, game_type):
        if game_type not in self.queues:
            self.queues[game_type] = []
        self.queues[game_type].append(user_id)
