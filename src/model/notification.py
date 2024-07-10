from datetime import datetime
from bson import ObjectId

class Notification:
    def __init__(self, user_id, content, notif_type="general", read=False, created_at=None, _id=None):
        self._id = _id or ObjectId()
        self.user_id = user_id
        self.content = content
        self.notif_type = notif_type
        self.read = read
        self.created_at = created_at or datetime.utcnow()

    @classmethod
    def from_dict(cls, data):
        created_at = data['created_at']
        if isinstance(created_at, str):
            created_at = datetime.fromisoformat(created_at)
        return cls(
            user_id=data['user_id'],
            content=data['content'],
            notif_type=data.get('notif_type', 'general'),
            read=data.get('read', False),
            created_at=created_at,
            _id=data['_id']
        )

    def to_json(self):
        return {
            "_id": str(self._id),
            "user_id": self.user_id,
            "content": self.content,
            "notif_type": self.notif_type,
            "read": self.read,
            "created_at": self.created_at.isoformat()
        }
