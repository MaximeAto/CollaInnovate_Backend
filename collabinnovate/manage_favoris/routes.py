

from datetime import datetime
import random
from faker import Faker
from flask import Blueprint, jsonify, request, abort
from sqlalchemy.exc import SQLAlchemyError

from collabinnovate import db
from collabinnovate.manage_favoris.model import Favoris
from collabinnovate.manage_problems.model import Problem
from collabinnovate.manage_user_accounts.account.model import Account
from collabinnovate.manage_user_accounts.user.model import User

favoris = Blueprint('favoris', __name__)
fake = Faker()


@favoris.route("/add", methods=["POST"])
def addfavoris():
    data = request.get_json()
    
    # Ajout de vérifications et de logs
    if not isinstance(data, dict):
        return jsonify({"error": "Invalid data format"}), 400

    email = data.get("email")
    type = data.get("type")
    favoris_id = data.get("favoris_id")

    user = User.query.filter_by(email = email).first()
    if not user:
        return jsonify({"error": "User not found"}), 404
   
    # Validate the data
    if not email or not favoris_id or not type:
        return jsonify({"error": "Missing data"}), 400
    
    # Create a new Favoris instance
    new_favoris = Favoris(type=type, id_favoris=favoris_id, user_id=user.id)
    
    try:
        # Add the new favoris to the database
        db.session.add(new_favoris)
        db.session.commit()
        return jsonify({"message": "Favoris added successfully"}), 201
    except Exception as e:
        # Handle any errors that occur
        db.session.rollback()
        return jsonify({"error": "error to Add to favoris"}), 500


@favoris.route("/delete/<email>/<type>/<favoris_id>", methods=["DELETE"])
def deletefavoris(email,type,favoris_id):

    user = User.query.filter_by(email = email).first()
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    # Validate the data
    if not type or not favoris_id or not email:
        return jsonify({"error": "Missing data"}), 400
    
    try:
        # Find the favoris to delete
        favoris_to_delete = Favoris.query.filter_by(type=type, id_favoris=favoris_id, user_id=user.id).first()
        
        if favoris_to_delete is None:
            return jsonify({"error": "Favoris not found"}), 404
        
        # Delete the favoris from the database
        db.session.delete(favoris_to_delete)
        db.session.commit()
        return jsonify({"message": "Favoris deleted successfully"}), 200
    except Exception as e:
        # Handle any errors that occur
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@favoris.route("/list/<email>/<type>", methods=["GET"])
def listOfFavoris(email,type):
    user = User.query.filter_by(email = email).first()
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    favoris_ids = Favoris.query.with_entities(Favoris.id_favoris).filter_by(type = type, user_id = user.id).all()
    favoris_ids_list = [favoris_id[0] for favoris_id in favoris_ids]

    return jsonify(favoris_ids_list)
