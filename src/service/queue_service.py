class QueueService:
    def __init__(self, queue_repository, game_service):
        self.queue_repository = queue_repository
        self.game_service = game_service

    def find_or_create_game(self, user_id: str, game_type: str):
        # Check if there is an available opponent
        opponent = self.queue_repository.find_one({
            'user_id': {'$ne': user_id},  # Exclude the current user
            'game_type': game_type,
            'state': 'waiting'
        })
        
        if opponent:
            # Create a new game with the found opponent
            game = self.game_service.create_game(user_id, opponent['user_id'], game_type)
            self.queue_repository.delete_one({'_id': opponent['_id']})
            return game._id, opponent['user_id']
        
        # Add the user to the queue
        self.queue_repository.insert_one({
            'user_id': user_id,
            'game_type': game_type,
            'state': 'waiting'
        })
        
        return None, None