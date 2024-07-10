
import logging
from src.model.message import Message


class ChatService:
    def __init__(self, chat_repository, notification_repository, user_repository):
        self.chat_repository = chat_repository
        self.notification_repository = notification_repository
        self.user_repository = user_repository

    def get_conversation(self, user1_id, user2_id):
        conversation = self.chat_repository.find_conversation(user1_id, user2_id)
        if not conversation:
            conversation = self.chat_repository.create_conversation(user1_id, user2_id)
        return conversation

    def send_message(self, sender_id, receiver_id, content, conversation_id):
        try:
            logging.info(f"Creating message from {sender_id} to {receiver_id} in conversation {conversation_id} with content: {content}")
            message = Message(sender_id=sender_id, receiver_id=receiver_id, content=content, conversation_id=conversation_id)
            self.chat_repository.add_message(conversation_id, message)

            # Get sender's name
            sender = self.user_repository.find_user_by_id(sender_id)
            if sender is None:
                logging.error(f"Sender with ID {sender_id} not found.")
                raise ValueError("Sender not found")
            sender_name = sender['username']

            # Create a notification for the receiver
            notification_content = f"Nouveau message de {sender_name}"
            notif_type = 'chat'  # Définir le type de notification ici
            self.notification_repository.create_notification(receiver_id, notification_content, notif_type)


            return message
        except Exception as e:
            logging.error(f"Error sending message: {e}")
            raise e