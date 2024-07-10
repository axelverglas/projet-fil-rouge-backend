from db import mongo
from src.model.message import Message
from src.model.conversation import Conversation

class ChatRepository:
    def create_conversation(self, user1_id, user2_id):
        conversation = Conversation(user1_id, user2_id)
        mongo.db.conversations.insert_one(conversation.to_json())
        return conversation

    def find_conversation(self, user1_id, user2_id):
        conversation = mongo.db.conversations.find_one({
            "$or": [
                {"user1_id": user1_id, "user2_id": user2_id},
                {"user1_id": user2_id, "user2_id": user1_id}
            ]
        })
        if conversation:
            return Conversation.from_dict(conversation)
        return None

    def find_conversation_by_id(self, conversation_id):
        try:
            conversation = mongo.db.conversations.find_one({"_id": conversation_id})
            if conversation:
                return Conversation.from_dict(conversation)
            return None
        except Exception as e:
            print(f"Error finding conversation by ID: {e}")
            return None

    def add_message(self, conversation_id, message):
        try:
            result = mongo.db.conversations.update_one(
                {"_id": conversation_id},
                {"$push": {"messages": message.to_json()}}
            )

            if result.matched_count == 0:
                raise ValueError("Conversation not found")
        except Exception as e:
            print(f"Error adding message: {e}")
            raise e

    def get_messages(self, conversation_id):
        try:
            conversation = mongo.db.conversations.find_one({"_id": conversation_id})
            if conversation:
                return [Message.from_dict(msg) for msg in conversation.get('messages', [])]
            return []
        except Exception as e:
            print(f"Error getting messages: {e}")
            return []
