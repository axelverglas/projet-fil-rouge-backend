from src.model.queue import Queue

queue = Queue()

class QueueRepository:
    def add_to_queue(self, user_id, game_type):
        queue.add_to_queue(user_id, game_type)

    def get_next_player(self, game_type):
        return queue.get_next_player(game_type)