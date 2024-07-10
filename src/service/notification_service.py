import logging

class NotificationService:
    def __init__(self, notification_repository):
        self.notification_repository = notification_repository

    def get_notifications(self, user_id):
        logging.info(f"Fetching notifications for user_id: {user_id}")
        notifications = self.notification_repository.find_notifications_by_user(user_id)
        logging.info(f"Found notifications: {notifications}")
        return notifications

    def mark_as_read(self, notif_id):
        logging.info(f"Marking notification {notif_id} as read")
        success = self.notification_repository.mark_notification_as_read(notif_id)
        logging.info(f"Marking notification {notif_id} as read successful: {success}")
        return success

    def delete_notifications(self, user_id):
        logging.info(f"Deleting notifications for user_id: {user_id}")
        success = self.notification_repository.delete_notifications_by_user(user_id)
        logging.info(f"Deleting notifications for user_id: {user_id} successful: {success}")
        return success
