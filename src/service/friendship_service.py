from src.model.friendship import Friendship
import logging

logger = logging.getLogger(__name__)

class FriendshipService:
    def __init__(self, friendship_repository, user_repository):
        self.friendship_repository = friendship_repository
        self.user_repository = user_repository

    def send_friend_request(self, creator_id, receiver_id):
        if self.are_friends(creator_id, receiver_id)['status'] is not None:
            raise ValueError("Already friends or request pending")

        request = Friendship(creator_id=creator_id, receiver_id=receiver_id, status='pending')
        self.friendship_repository.create_friend_request(request)
        return request
    
    def accept_friend_request(self, creator_id, receiver_id):
        request = self.friendship_repository.find_friend_request(creator_id, receiver_id)
        if not request or request['status'] != 'pending':
            raise ValueError("No pending request found")
        friendship = Friendship.from_dict(request)
        friendship.status = 'accepted'
        self.friendship_repository.update_friend_request(friendship)
        return friendship

    def are_friends(self, creator_id, receiver_id):
        friendship = self.friendship_repository.find_friendship(creator_id, receiver_id)
        if friendship:
            return {"areFriends": True, "status": friendship['status']}
        friend_request = self.friendship_repository.find_friend_request(creator_id, receiver_id)
        if friend_request:
            return {"areFriends": False, "status": friend_request['status']}
        return {"areFriends": False, "status": None}
    
    def get_friends(self, user_id):
        friends = self.friendship_repository.get_friends(user_id)
        for friend in friends:
            if friend.creator_id == user_id:
                friend.user = self.user_repository.find_user_by_id(friend.receiver_id)
            else:
                friend.user = self.user_repository.find_user_by_id(friend.creator_id)
        friends_dict = [friend.to_dict() for friend in friends]
        return friends_dict
    
    def get_sent_requests(self, user_id):
        return self.friendship_repository.get_sent_requests(user_id)

    def get_received_requests(self, user_id):
        return self.friendship_repository.get_received_requests(user_id)
    
    def delete_friendship(self, creator_id, receiver_id):
        logger.debug(f"Deleting friendship: creator_id={creator_id}, receiver_id={receiver_id}")
        result = self.friendship_repository.delete_friendship(creator_id, receiver_id)
            
        if result.deleted_count == 0:
            raise ValueError("No friendship found to delete")
            
        logger.debug(f"Friendship deleted: creator_id={creator_id}, receiver_id={receiver_id}")
