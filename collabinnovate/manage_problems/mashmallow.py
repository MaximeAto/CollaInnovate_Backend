from collabinnovate import ma
from collabinnovate.manage_problems.model import Problem
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
  comments = ma.Nested(MashmallowComment, many=True)
  mentions = ma.Nested(MashmallowMention, many=False)
  class Meta:
    model = Solution

class MashmallowProblem(ma.SQLAlchemyAutoSchema):
  solutions = ma.Nested(MashmallowSolution, many=True)
  class Meta:
    model = Problem