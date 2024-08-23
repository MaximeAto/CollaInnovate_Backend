from datetime import datetime
from collabinnovate import db

class Session(db.Model):
  __tablename__ = "sessions"
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
  token = db.Column(db.String(255), nullable=False)  
  ip_address = db.Column(db.String(50), nullable=False) 
  user_agent = db.Column(db.String(200), nullable=False)
  created_at = db.Column(db.DateTime, default=datetime.utcnow) 
  last_activity = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow) 
  is_active = db.Column(db.Boolean, default=True) 
