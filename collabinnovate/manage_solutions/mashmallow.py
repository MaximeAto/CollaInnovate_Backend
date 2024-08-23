from collabinnovate import ma
from collabinnovate.manage_solutions.comments.model import Comment
from collabinnovate.manage_solutions.mentions.model import Mention
from collabinnovate.manage_solutions.model import Solution

class MashmallowComment(ma.SQLAlchemyAutoSchema):
  class Meta:
    model = Comment

class MashmallowMention(ma.SQLAlchemyAutoSchema):
  class Meta:
    model = Mention

class MashmallowSolution(ma.SQLAlchemyAutoSchema):
  solutions = ma.Nested(MashmallowComment, many=True)
  solutions = ma.Nested(MashmallowMention, many=True)
  class Meta:
    model = Solution