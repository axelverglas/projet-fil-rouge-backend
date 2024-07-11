from bson import ObjectId
from datetime import datetime

class Message:
    def __init__(self, sender_id, receiver_id, content, conversation_id, _id=None, created_at=None):
        self._id = _id or ObjectId()
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.content = content
        self.created_at = created_at or datetime.now()
        self.conversation_id = conversation_id

    def to_json(self):
        return {
            '_id': str(self._id),
            'sender_id': str(self.sender_id),
            'receiver_id': str(self.receiver_id),
            'content': self.content,
            'created_at': self.created_at.isoformat(),
            'conversation_id': str(self.conversation_id)
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            sender_id=data['sender_id'],
            receiver_id=data['receiver_id'],
            content=data['content'],
            conversation_id=data['conversation_id'],
            _id=ObjectId(data['_id']),
            created_at=datetime.fromisoformat(data['created_at'])
        )
