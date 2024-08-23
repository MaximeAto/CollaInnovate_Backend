from collabinnovate import db

class Edit(db.Model) :
  __tablename__ = "edit"
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
