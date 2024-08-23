from collabinnovate import ma
from collabinnovate.manage_favoris.model import Favoris

class MashmallowFavoris(ma.SQLAlchemyAutoSchema):
  class Meta:
    model = Favoris