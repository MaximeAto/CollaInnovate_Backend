from collabinnovate import db
from sqlalchemy import JSON
import random
import json


class Mention(db.Model):
    __tablename__ = "mentions"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    solution_id = db.Column(db.Integer, db.ForeignKey('solutions.id'), nullable=False)
    approuved = db.Column(db.Boolean)
    

