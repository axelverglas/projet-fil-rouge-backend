from db import mongo

from bson import ObjectId

class GameRepository:
    def create_game(self, game):
        game_json = game.to_json()
        print(f"Creating game with data: {game_json}")
        game_id = mongo.db.games.insert_one(game_json).inserted_id
        print(f"Game created with ID: {game_id}")
        return str(game_id)

    def find_game_by_id(self, game_id):
        try:
            print(f"Finding game with ID: {game_id}")
            game = mongo.db.games.find_one({"_id": game_id})
            if game:
                print(f"Found game: {game}")
            else:
                print("Game not found")
            return game
        except Exception as e:
            print(f"Error finding game: {e}")
            return None

    def update_game(self, game):
        game_id = game._id
        game_json = game.to_json()
        print(f"Updating game with ID: {game_id}")
        result = mongo.db.games.update_one({"_id": game_id}, {"$set": game_json})
        if result.modified_count == 0:
            print("No game was updated.")
        return result.modified_count
