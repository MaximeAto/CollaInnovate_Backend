from datetime import datetime
import random

from collabinnovate import db


class Favoris(db.Model):
    __tablename__ = "favoris"
    type = db.Column(db.String(10), primary_key=True, nullable=False)
    id_favoris = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True, nullable=False)

    def to_dict(self):
        return {
            'type': self.type,
            'id_favoris': self.id_favoris,
            'user_id': self.user_id
        }



