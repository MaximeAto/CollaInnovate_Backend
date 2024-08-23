from flask import Blueprint


password = Blueprint('password', __name__)


@password.route('/password/reset', methods=['POST'])
def reset_password():
  pass

@password.route('/password/change', methods=['POST'])
def change_password():
  pass
