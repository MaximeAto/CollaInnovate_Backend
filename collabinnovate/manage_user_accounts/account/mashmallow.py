from collabinnovate import ma
# from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from collabinnovate.manage_problems.mashmallow import MashmallowComment
from collabinnovate.manage_problems.model import Problem
from collabinnovate.manage_solutions.mentions.model import Mention
from collabinnovate.manage_solutions.model import Solution
from collabinnovate.manage_user_accounts.account.model import Account
    
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


class MashmallowAccount(ma.SQLAlchemyAutoSchema):
  problems = ma.Nested(MashmallowProblem,many=True)
  solutions = ma.Nested(MashmallowSolution,many=True)
  class Meta:
    model = Account