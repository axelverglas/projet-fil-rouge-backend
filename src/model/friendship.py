from bson import ObjectId

class Friendship:
    def __init__(self, creator_id, receiver_id, status='pending', _id=None, user=None):
        self._id = _id or str(ObjectId())
        self.creator_id = creator_id
        self.receiver_id = receiver_id
        self.status = status
        self.user = user

    def to_dict(self):
        data = {
            "_id": str(self._id),
            "creator_id": str(self.creator_id),
            "receiver_id": str(self.receiver_id),
            "status": self.status
        }
        if self.user:
            data["user"] = self.user  # Inclure l'utilisateur si présent
        return data

    @classmethod
    def from_dict(cls, data):
        return cls(
            creator_id=data.get("creator_id"),
            receiver_id=data.get("receiver_id"),
            status=data.get("status"),
            _id=data.get("_id"),
            user=data.get("user")  # Ajoutez l'utilisateur s'il est présent
        )
