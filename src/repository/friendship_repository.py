from db import mongo
from src.model.friendship import Friendship

class FriendshipRepository:
    def create_friend_request(self, request):
        request_json = request.to_dict()
        mongo.db.friendships.insert_one(request_json)
        return request

    def find_friend_request(self, creator_id, receiver_id):
        return mongo.db.friendships.find_one({"creator_id": creator_id, "receiver_id": receiver_id, "status": "pending"})

    def update_friend_request(self, request):
        mongo.db.friendships.update_one({"_id": request._id}, {"$set": {"status": request.status}})

    def find_friendship(self, creator_id, receiver_id):
        return mongo.db.friendships.find_one({"creator_id": creator_id, "receiver_id": receiver_id, "status": "accepted"})

    def get_friends(self, user_id):
        friendships = mongo.db.friendships.find({"creator_id": user_id, "status": "accepted"})
        return [Friendship.from_dict(friendship) for friendship in friendships]
