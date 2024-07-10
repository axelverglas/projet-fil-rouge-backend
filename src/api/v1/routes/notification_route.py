from flask import Blueprint, request, jsonify
from src.service.notification_service import NotificationService
from src.repository.notification_repository import NotificationRepository
import logging

notification_bp = Blueprint('notification_bp', __name__)
notification_repository = NotificationRepository()
notification_service = NotificationService(notification_repository)

@notification_bp.route('/<user_id>', methods=['GET'])
def get_notifications(user_id):
    logging.info(f"Received request to get notifications for user {user_id}")
    notifications = notification_service.get_notifications(user_id)
    notifications = [notif.to_json() for notif in notifications]
    logging.info(f"Returning notifications: {notifications}")
    return jsonify(notifications), 200

@notification_bp.route('/<notif_id>', methods=['PUT'])
def mark_notification_as_read(notif_id):
    logging.info(f"Received request to mark notification {notif_id} as read")
    success = notification_service.mark_as_read(notif_id)
    if not success:
        logging.error(f"Notification {notif_id} not found")
        return jsonify({'error': 'Notification not found'}), 404
    logging.info(f"Notification {notif_id} marked as read")
    return jsonify({'message': 'Notification marked as read'}), 200

@notification_bp.route('/clear/<user_id>', methods=['DELETE'])
def delete_notifications(user_id):
    logging.info(f"Received request to delete notifications for user {user_id}")
    success = notification_service.delete_notifications(user_id)
    if not success:
        logging.error(f"Error deleting notifications for user {user_id}")
        return jsonify({'error': 'Error deleting notifications'}), 500
    logging.info(f"Notifications for user {user_id} deleted successfully")
    return jsonify({'message': 'Notifications deleted successfully'}), 200
