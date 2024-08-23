from collabinnovate import ma
from collabinnovate.manage_solutions.mentions.model import Mention

class MashmallowMention(ma.SQLAlchemyAutoSchema):
  class Meta:
    model = Mention