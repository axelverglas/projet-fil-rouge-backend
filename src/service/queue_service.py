class QueueService:
    def __init__(self, queue_repository, game_service):
        self.queue_repository = queue_repository
        self.game_service = game_service

    def find_or_create_game(self, user_id, game_type):
        print(f"User {user_id} is looking for a game of type {game_type}")
        opponent_id = self.queue_repository.get_next_player(game_type)
        if opponent_id:
            print(f"Found opponent {opponent_id} for user {user_id}")
            game = self.game_service.create_game(opponent_id, user_id, game_type)
            print(f"Created game with ID: {game._id}")
            return game._id, opponent_id
        else:
            print(f"No opponent found for user {user_id}, adding to queue")
            self.queue_repository.add_to_queue(user_id, game_type)
            return None, None
