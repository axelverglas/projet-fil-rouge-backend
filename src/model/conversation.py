from bson import ObjectId
from .message import Message

class Conversation:
    def __init__(self, user1_id, user2_id, _id=None):
        self._id = _id or ObjectId()
        self.user1_id = user1_id
        self.user2_id = user2_id
        self.messages = []

    def to_json(self):
        return {
            '_id': str(self._id),
            'user1_id': str(self.user1_id),
            'user2_id': str(self.user2_id),
            'messages': [message.to_json() for message in self.messages]
        }

    @classmethod
    def from_dict(cls, data):
        conversation = cls(
            user1_id=data['user1_id'],
            user2_id=data['user2_id'],
            _id=data['_id']
        )
        conversation.messages = [Message.from_dict(msg) for msg in data['messages']]
        return conversation
