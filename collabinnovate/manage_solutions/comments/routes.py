from datetime import datetime
import random
from flask import Blueprint, json, jsonify, request
from collabinnovate import db
from faker import Faker

from collabinnovate.manage_solutions.comments.model import Comment
from collabinnovate.manage_user_accounts.user.model import User


comments = Blueprint('comments', __name__)
fake = Faker()

# def generate_fake_comments(num_comments=1000):
#     user_ids = list(range(1, 21))
#     solution_ids = list(range(1, 1001))
    
#     for _ in range(num_comments):
#         comment = Comment(
#             user_id=fake.random_element(elements=user_ids),
#             solution_id=fake.random_element(elements=solution_ids),
#             dateAdded = datetime.utcnow
#             comment=fake.paragraph(nb_sentences=3),
#             overall = fake.random_element(elements = list(range(1,6)) ) 
#         )
#         db.session.add(comment)
#         db.session.commit()

# @comments.route("/thousand_comments", methods=["POST"])
# def thousand_solution():
#     generate_fake_comments()

#     return jsonify({"message" : "good"})


@comments.route('/add_comment', methods=['POST'])
def add_comment():
    data = request.get_json()
    user = User.query.filter_by(email = data.get('user_email')).first()

    user_id = user.id
    username = data.get('username')
    solution_id = data.get('solution_id')
    dateAdded = data.get('dateAdded')
    comment_text = data.get('comment')

    if not user_id or not solution_id or not comment_text:
        return jsonify({'error': 'Missing required fields'}), 400

    # Création d'une nouvelle instance de Comment
    new_comment = Comment(
        user_id=user_id,
        solution_id=solution_id,
        comment=comment_text,
        dateAdded = dateAdded,
        username = username
    )

    try:
        db.session.add(new_comment)
        db.session.commit()
        return jsonify({'message': 'Comment added successfully'}), 201
    except Exception as e:
        # Gestion des erreurs
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    

@comments.route('/get_by_solution/<int:solution_id>', methods=['GET'])
def get_comments_by_solution(solution_id):
    # try:
        # Récupérer les commentaires filtrés par solution_id et classés par dateAdded
        comments = Comment.query.filter_by(solution_id=solution_id).order_by(Comment.dateAdded.asc()).all()

        # Si aucun commentaire trouvé
        if not comments:
            return jsonify({'message': 'No comments found for this solution'}), 404

        # Utiliser la méthode to_dict pour chaque commentaire
        comments_list = [comment.to_dict() for comment in comments]

        # Retourner les commentaires en format JSON
        return jsonify(comments_list), 200
    # except Exception as e:
    #     return jsonify({'error': str(e)}), 500