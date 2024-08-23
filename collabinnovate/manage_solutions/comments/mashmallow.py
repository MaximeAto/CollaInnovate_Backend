from collabinnovate import ma
from collabinnovate.manage_solutions.comments.model import Comment

class MashmallowComment(ma.SQLAlchemyAutoSchema):
  class Meta:
    model = Comment