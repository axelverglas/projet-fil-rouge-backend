from bson import ObjectId

class Friendship:
    def __init__(self, creator_id, receiver_id, status='pending', _id=None):
        self._id = _id or ObjectId()
        self.creator_id = creator_id
        self.receiver_id = receiver_id
        self.status = status

    def to_dict(self):
        return {
            "_id": str(self._id),
            "creator_id": str(self.creator_id),
            "receiver_id": str(self.receiver_id),
            "status": self.status
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            creator_id=data.get("creator_id"),
            receiver_id=data.get("receiver_id"),
            status=data.get("status"),
            _id=data.get("_id")
        )
