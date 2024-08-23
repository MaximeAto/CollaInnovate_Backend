import random
from flask import Blueprint, json, jsonify, request
from collabinnovate import db
from faker import Faker

from collabinnovate.manage_solutions.mentions.model import Mention



mentions = Blueprint('mentions', __name__)
fake = Faker()

def generate_fake_mentions():
    user_ids = list(range(1, 21))  
    solution_ids = list(range(1, 1001))  
    
    for solution_id in solution_ids:
        mention = Mention(
            user_id=fake.random_element(elements=user_ids),
            solution_id=solution_id,
            approuved=fake.boolean()
        )
        db.session.add(mention)
        db.session.commit()



@mentions.route("/thousand_mention", methods=["POST"])
def thousand_solution():
    generate_fake_mentions()




