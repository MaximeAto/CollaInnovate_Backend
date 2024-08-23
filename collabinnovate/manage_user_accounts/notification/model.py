from collabinnovate import db

class Notification(db.Model) :
  __tablename__ = "Notifications"
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
  