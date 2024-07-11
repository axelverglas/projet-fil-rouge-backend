class QueueRepository:
    def __init__(self):
        self.queues = {}

    def get_next_player(self, game_type, exclude_user_id):
        if game_type in self.queues:
            for i, user_id in enumerate(self.queues[game_type]):
                if user_id != exclude_user_id:
                    return self.queues[game_type].pop(i)
        return None

    def add_to_queue(self, user_id, game_type):
        if game_type not in self.queues:
            self.queues[game_type] = []
        self.queues[game_type].append(user_id)
