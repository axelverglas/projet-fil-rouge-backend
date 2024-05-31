class QueueService:
    def __init__(self, queue_repository, game_service):
        self.queue_repository = queue_repository
        self.game_service = game_service

    def find_or_create_game(self, user_id, game_type):
        opponent_id = self.queue_repository.get_next_player(game_type)
        if opponent_id:
            game_id = self.game_service.create_game(opponent_id, user_id)
            return game_id, opponent_id
        else:
            self.queue_repository.add_to_queue(user_id, game_type)
            return None, None
