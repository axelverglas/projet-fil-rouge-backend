from db import mongo
from src.model.friendship import Friendship
from bson import ObjectId
import logging
from pymongo import ReturnDocument

logger = logging.getLogger(__name__)

class FriendshipRepository:
    def create_friend_request(self, request):
        request_json = request.to_dict()
        mongo.db.friendships.insert_one(request_json)
        return request

    def find_friend_request(self, creator_id, receiver_id):
        return mongo.db.friendships.find_one({
            "creator_id": creator_id,
            "receiver_id": receiver_id,
            "status": "pending"
        })
    
    def update_friend_request(self, request):
         mongo.db.friendships.find_one_and_update(
            {"_id": request._id},
            {"$set": {"status": request.status}}
        )

    def find_friendship(self, creator_id, receiver_id):
        return mongo.db.friendships.find_one({
            "creator_id": creator_id,
            "receiver_id": receiver_id,
            "status": "accepted"
        })

    def get_friends(self, user_id):
        friendships = mongo.db.friendships.find({
            "$or": [
                {"creator_id": user_id, "status": "accepted"},
                {"receiver_id": user_id, "status": "accepted"}
            ]
        })
        return [Friendship.from_dict(friendship) for friendship in friendships]

    def get_sent_requests(self, user_id):
        requests = mongo.db.friendships.find({
            "creator_id": user_id,
            "status": "pending"
        })
        return [Friendship.from_dict(request) for request in requests]

    def get_received_requests(self, user_id):
        requests = mongo.db.friendships.find({
            "receiver_id": user_id,
            "status": "pending"
        })
        return [Friendship.from_dict(request) for request in requests]
    
    def delete_friendship(self, creator_id, receiver_id):
        logger.debug(f"Deleting friendship in DB: creator_id={creator_id}, receiver_id={receiver_id}")
        return mongo.db.friendships.delete_one({
            "creator_id": creator_id,
            "receiver_id": receiver_id
        })