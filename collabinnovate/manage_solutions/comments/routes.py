import random
from flask import Blueprint, json, jsonify, request
from collabinnovate import db
from faker import Faker

from collabinnovate.manage_solutions.comments.model import Comment


comments = Blueprint('comments', __name__)
fake = Faker()

def generate_fake_comments(num_comments=1000):
    user_ids = list(range(1, 21))
    solution_ids = list(range(1, 1001))
    
    for _ in range(num_comments):
        comment = Comment(
            user_id=fake.random_element(elements=user_ids),
            solution_id=fake.random_element(elements=solution_ids),
            comment=fake.paragraph(nb_sentences=3),
            overall = fake.random_element(elements = list(range(1,6)) ) 
        )
        db.session.add(comment)
        db.session.commit()

@comments.route("/thousand_comments", methods=["POST"])
def thousand_solution():
    generate_fake_comments()

    return jsonify({"message" : "good"})