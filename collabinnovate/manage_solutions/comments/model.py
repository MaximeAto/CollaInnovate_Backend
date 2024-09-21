from datetime import datetime
from collabinnovate import db
from sqlalchemy import JSON
import random
import json


class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    solution_id = db.Column(db.Integer, db.ForeignKey('solutions.id'), nullable=False)
    dateAdded = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    comment = db.Column(db.Text)
    overall = db.Column(db.Integer)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'username': self.username,
            'solution_id': self.solution_id,
            'dateAdded': self.dateAdded.strftime('%Y-%m-%d %H:%M:%S'),  # Formatage de la date
            'comment': self.comment,
            'overall': self.overall
        }
    



