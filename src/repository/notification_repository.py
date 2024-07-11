import logging
from db import mongo
from src.model.notification import Notification

class NotificationRepository:
    def create_notification(self, user_id, content, notif_type, sender_id):
        logging.info(f"Creating notification for user_id: {user_id} with content: '{content}' and type: '{notif_type}' from sender_id: {sender_id}")
        notification = Notification(user_id=user_id, content=content, notif_type=notif_type, sender_id=sender_id)
        mongo.db.notifications.insert_one(notification.to_json())
        return notification

    def find_notifications_by_user(self, user_id):
        try:
            logging.info(f"Finding notifications for user_id: {user_id}")
            notifications = mongo.db.notifications.find({'user_id': user_id})
            notifications_list = [Notification.from_dict(notif) for notif in notifications]
            logging.info(f"Found notifications: {notifications_list}")
            return notifications_list
        except Exception as e:
            logging.error(f"Error finding notifications for user {user_id}: {e}")
            return []

    def mark_notification_as_read(self, notif_id):
        try:
            logging.info(f"Marking notification {notif_id} as read")
            result = mongo.db.notifications.update_one(
                {'_id': notif_id},
                {'$set': {'read': True}}
            )
            logging.info(f"Notification {notif_id} marked as read: {result.matched_count > 0}")
            return result.matched_count > 0
        except Exception as e:
            logging.error(f"Error marking notification {notif_id} as read: {e}")
            return False

    def delete_notifications_by_user(self, user_id):
        try:
            logging.info(f"Deleting notifications for user_id: {user_id}")
            result = mongo.db.notifications.delete_many({'user_id': user_id})
            logging.info(f"Notifications deleted for user_id: {user_id}, count: {result.deleted_count}")
            return result.deleted_count > 0
        except Exception as e:
            logging.error(f"Error deleting notifications for user {user_id}: {e}")
            return False
