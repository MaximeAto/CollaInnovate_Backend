from flask import Blueprint


journalisations = Blueprint('journalisations', __name__)


@journalisations.route('/write', methods=['POST'])
def log_event():
  pass

@journalisations.route('/get/<int:id>', methods=['GET'])
def get_journalisation_by_id(id):
  pass

@journalisations.route('/all', methods=['GET'])
def get_all_journalisations():
  pass
