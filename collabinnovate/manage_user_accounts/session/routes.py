from flask import Blueprint, jsonify, request, current_app
from collabinnovate.manage_user_accounts.session.model import Session
from collabinnovate import db
from collabinnovate.manage_user_accounts.user.model import User
from .utils import is_valid_ip


sessions = Blueprint('sessions', __name__)

@sessions.route('/gettoken/<email>', methods=['GET'])
def gettoken(email):
  try:
    user = User.query.filter_by(email = email).first()
    session = Session.query.filter_by(user_id = user.id).first()
    return jsonify({"message": session.token}),200
  except Exception as e:
    return jsonify({"message" : e})


@sessions.route('/create', methods=['POST'])
def create_session():
  data = request.form
    
  # Vérifier si toutes les données nécessaires sont fournies
  if 'user_id' not in data or 'token' not in data or 'ip_address' not in data or 'user_agent' not in data:
    return jsonify({'message': 'Toutes les données requises ne sont pas fournies'}), 400
  
  # Vérifier le format de l'adresse IP
  if not is_valid_ip(data['ip_address']):
    return jsonify({'message': 'Format d\'adresse IP invalide'}), 400
  
  # Créer une nouvelle session
  new_session = Session(
    user_id=data['user_id'],
    token=data['token'],
    ip_address=data['ip_address'],
    user_agent=data['user_agent']
  )
  
  # Ajouter la session à la base de données
  db.session.add(new_session)
  db.session.commit()
  
  return jsonify({'message': 'Session créée avec succès'}), 201

@sessions.route('/update/<session_id>', methods=['PUT'])
def update_session(session_id):
  pass

@sessions.route('/delete/<session_id>', methods=['DELETE'])
def delete_session(session_id):
  pass
