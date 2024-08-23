from sqlalchemy import JSON
from collabinnovate import db

class Account(db.Model):
    __tablename__ = "accounts"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    account_details = db.Column(JSON)
    role = db.Column(db.String(50), nullable=False)
    active = db.Column(db.Boolean, nullable=False, default = True)
    

  