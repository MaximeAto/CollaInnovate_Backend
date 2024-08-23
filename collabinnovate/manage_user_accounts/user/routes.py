
from datetime import datetime, timedelta
from faker import Faker
from flask import Blueprint, jsonify, make_response, request, current_app
import jwt
from collabinnovate import db,LogginFormatter
from collabinnovate.manage_user_accounts.account.model import Account
from collabinnovate.manage_user_accounts.user.model import User
from collabinnovate.manage_user_accounts.authentification.routes import generate_token, generer_code_pin
from werkzeug.security import generate_password_hash
from collabinnovate.manage_user_accounts.notification.utils import confirmation_mail
from collabinnovate import mail
import re
from flask import render_template
from collabinnovate.manage_user_accounts.session.utils import *


users = Blueprint('users', __name__)
fake = Faker()


  
  
# Créer 20 user
@users.route("/hundred_users", methods=['POST'])
def hundred_users():
  domains = [
    "Agro-pastoral et halieutique",
    "Industries extractives et de transformation",
    "Tourisme et artisanat",
    "Technologies de l'information et de la communication (TIC)",
    "Infrastructures",
    "Capital humain",
    "Gouvernance et décentralisation",
    "État de droit et sécurité"
  ]
  for _ in range(20):
      
    user = User(
      full_name=fake.name(),
      role_id = 1,
      email=fake.email(),
      phone_number=fake.phone_number(),
      social_link=fake.url(),
      password=generate_password_hash('Motdepass123#', method='pbkdf2:sha256', salt_length=8),
      address=fake.address(),
      city=fake.city(),
      country=fake.country(),
      profile_photo=fake.image_url(),
      bio=fake.text(),
      activity_domain=fake.random_element(elements=domains),
      group_id = 1,
      work_title=fake.job(),
      website=fake.url(),
      language=fake.random_element(elements=("fr","en")),
      confirmed = True
    )
    
    db.session.add(user)
    db.session.commit()

    account = Account(
      user_id=user.id,
      account_details={},
      role="client"
    )
    db.session.add(account)
    db.session.commit()
  
  return jsonify(message = "les 20 users ont été enregistré")

@users.route('/all', methods=['GET'])
def get_all_users():
  return render_template('welcome.html', full_name = 'Maxime')  

@users.route('/get/<int:user_id>', methods=['GET'])
def get_user(user_id):
  pass

@users.route('/create', methods=['POST','GET'])
def create_user():
  try:
    data = request.form

    # Vérification que tous les attributs sont présents
    required_attributes = ['full_name', 'email', 'password']
    for attribute in required_attributes:
      if attribute not in data or not data[attribute]:
        return jsonify({'message': f'Missing or empty value for {attribute}.'}), 400

    # Validation du format de l'adresse e-mail
    email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if not re.match(email_regex, data['email']):
      return jsonify({'message': 'Invalid email format.'}), 400

    # Validation du format du numéro de téléphone (exemple de format : +1234567890)
    phone_regex = r'^\+\d{8,15}$'
    if 'phone_number' in data and not re.match(phone_regex, data['phone_number']):
      return jsonify({'message': 'Invalid phone number format.'}), 400

    # Vérification si l'utilisateur existe déjà
    existing_mail = User.query.filter_by(email=data['email']).first()
    existing_phonenumeber = User.query.filter_by(phone_number=data['phone_number']).first()

    if existing_phonenumeber or existing_mail:
      return jsonify({'message': 'This user already exists.'}), 409

    hashed_password = generate_password_hash(data.get('password'), method='pbkdf2:sha256', salt_length=8)

    # Création d'un nouvel utilisateur
    new_user = User(
      full_name=data.get('full_name'),
      email=data['email'],
      phone_number=data.get('phone_number'),
      password=hashed_password,
    )

    codeping = generer_code_pin()

    # Génération du token JWT
    token = generate_token(new_user.email, codeping)

    # Envoie du mail d'inscription
    confirmation_mail(data['email'], codeping,mail)
    log_message = "user créée avec succès"
    app = current_app._get_current_object()
    app.logger.info(log_message)

    db.session.add(new_user)
    db.session.commit()

    account = Account(
      user_id=new_user.id,
      account_details={},
      role="client"
    )
    db.session.add(account)
    db.session.commit()

    create_session(new_user.id,token)

    return jsonify({"token": token, "ping": codeping, "email": data['email'] }),200
  except Exception as e:
    return jsonify({'message': f'An error occured'}), 500
  
  
@users.route('/update/<int:user_id>', methods=['PUT'])
def update_user(user_id):
  pass

@users.route('/delete/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
  pass

@users.route('/get_role/<int:user_id>/roles', methods=['GET'])
def get_user_roles(user_id):
  pass

@users.route('/update_role/<int:user_id>/roles', methods=['PUT'])
def update_user_roles(user_id):
  pass

