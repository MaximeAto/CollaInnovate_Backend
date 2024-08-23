from collabinnovate import db
from sqlalchemy import JSON
import random
import json


class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    solution_id = db.Column(db.Integer, db.ForeignKey('solutions.id'), nullable=False)
    comment = db.Column(db.Text)
    overall = db.Column(db.Integer)
    
    



