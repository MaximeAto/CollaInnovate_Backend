
from datetime import datetime, timedelta
import random
import re
import string

from flask import Blueprint, jsonify, make_response, request
import jwt
from collabinnovate import db
from collabinnovate.config import SECRET_JWT_KEY
from collabinnovate.manage_user_accounts.notification.utils import confirmation_mail
from collabinnovate.manage_user_accounts.session.model import Session
from collabinnovate.manage_user_accounts.session.utils import *
from collabinnovate.manage_user_accounts.user.model import User
from werkzeug.security import check_password_hash
from collabinnovate import mail
from werkzeug.security import generate_password_hash
from collabinnovate.manage_user_accounts.notification.utils import reset_password_mail

auth = Blueprint('auth', __name__)

@auth.route('/resendvalidation/<email>', methods=['GET'])
def resendvalidation(email):
    user = User.query.filter_by(email = email).first()
    usersession = Session.query.filter_by(user_id = user.id).first()
    codeping = generer_code_pin()
    usersession.token = generate_token(email,codeping)
    confirmation_mail(email, codeping,mail)
    db.session.add(usersession)
    db.session.commit()

    return jsonify({'message': codeping})

@auth.route('/emailconfirmation/<codeping>/<email>', methods=['GET'])
def confirmMail(codeping, email):
    try:
        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({'message': 'User not found'}), 404

        # Récupérer la session
        usersession = Session.query.filter_by(user_id=user.id).first()
        if not usersession:
            return jsonify({'message': 'Session not found'}), 404

        try:
            decoded_token = jwt.decode(usersession.token, SECRET_JWT_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Expired token'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token'}), 400

        print(f'Decoded token: {decoded_token}')

        # Vérifier si le codeping fourni correspond à celui stocké dans le token
        if codeping != decoded_token.get('codeping'):
            return jsonify({'message': 'Incorrect code'}), 400

        user.confirmed = True
        db.session.add(user)
        db.session.commit()

        return jsonify({'message': 'Codeping and token validated successfully.'}), 200

    except Exception as e:
        print(f'An error occurred: {e}')
        return jsonify({'message': 'An error occurred'}), 500

@auth.route('/login', methods=['POST'])
def login():
    try:
        data = request.form

        # Vérification de la présence du nom d'utilisateur et du mot de passe
        username = data['username']
        password = data['password']
        rememberme = data['rememberme']
        if not username or not password:
            return jsonify({'message' :'Username and password are required.'})

        # Vérification si l'utilisateur existe
        user = User.query.filter_by(email=username).first()
        if not user:
            return jsonify({'message' :'User not found.'})
            

        # Vérification du mot de passe
        if not check_password_hash(user.password, password):
            return jsonify({'message' :'Incorrect password.'})

        # Authentification réussie
    
        if(rememberme):
            token = month_refresh_token(username)
        else:
            token = refresh_token(username)

        user_agent = request.user_agent.string
        usersession = Session.query.filter_by(user_id = user.id, user_agent = user_agent ).first()
        if(usersession):
            usersession.token = token
            db.session.add(usersession)
            db.session.commit()
        else:
            new_session = Session(
                user_id = user.id,
                token = token,
                ip_address = request.remote_addr,
                user_agent = user_agent,
            )

            db.session.add(new_session)
            db.session.commit()

        return jsonify({'email': username}), 200

    except ValueError as e:
        return jsonify({'message': str(e)}), 400
    except Exception as e:
        return jsonify({'message': 'An error occurred.', 'error': str(e)}), 500

@auth.route('/logout', methods=['POST'])
def logout():
    # implémentation la logique de déconnexion, comme la suppression de la session utilisateur
    return jsonify({'message': 'Logout successful.'}), 200

@auth.route('/resetpassword/<email>', methods=['GET'])
def resetpassword(email):
    try:
        user = User.query.filter_by(email = email).first()
        if not user:
           return jsonify({"message":"User not found!"}),409
        
        password = generate_random_string()       
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)

        user.password = hashed_password
        db.session.add(user)
        db.session.commit()
        reset_password_mail(email,password,mail)

        return jsonify({"message" : "Password reset"}),200

    except Exception as e:
        return jsonify({"message": "Processing errors"}),500


def refresh_token(email):
    token_payload = {
      'user_id': email,
      'exp': datetime.utcnow() + timedelta(hours=1)
    }
    token = jwt.encode(token_payload, SECRET_JWT_KEY, algorithm='HS256')
    return token

def month_refresh_token(email):
    token_payload = {
      'user_id': email,
      'exp': datetime.utcnow() + timedelta(days=30)
    }
    token = jwt.encode(token_payload, SECRET_JWT_KEY, algorithm='HS256')
    return token

def generer_code_pin():
    return ''.join([str(random.randint(0, 9)) for _ in range(8)])

def generate_token(email, codeping):
    token_payload = {
      'user_id': email,
      'codeping':codeping,
      'exp': datetime.utcnow() + timedelta(hours=1)
    }
    token = jwt.encode(token_payload, SECRET_JWT_KEY, algorithm='HS256')

    return token

def generate_random_string():
    characters = string.ascii_letters + string.digits + string.punctuation
    random_string = ''.join(random.choice(characters) for _ in range(8))
    return random_string
