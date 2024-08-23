from flask import Blueprint

notifications = Blueprint('notifications', __name__)

@notifications.route('/all/<int:user_id>', methods=['GET'])
def get_notifications(user_id):
  pass

@notifications.route('/get/<int:notification_id>', methods=['GET'])
def get_notification(notification_id):
  pass

@notifications.route('/create', methods=['POST'])
def create_notification():
  pass

@notifications.route('/update/<int:notification_id>', methods=['PUT'])
def update_notification(notification_id):
  pass

@notifications.route('/delete/<int:notification_id>', methods=['DELETE'])
def delete_notification(notification_id):
  pass