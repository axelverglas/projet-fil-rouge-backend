class Friendship:
    def __init__(self, creator_id, receiver_id, status='pending'):
        self.creator_id = creator_id
        self.receiver_id = receiver_id
        self.status = status

    def to_dict(self):
        return {
            "creator_id": self.creator_id,
            "receiver_id": self.receiver_id,
            "status": self.status
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            creator_id=data.get("creator_id"),
            receiver_id=data.get("receiver_id"),
            status=data.get("status")
        )
