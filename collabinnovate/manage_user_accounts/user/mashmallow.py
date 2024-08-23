from collabinnovate import ma
from collabinnovate.manage_favoris.model import Favoris
from collabinnovate.manage_solutions.comments.model import Comment
from collabinnovate.manage_user_accounts.account.model import Account
from collabinnovate.manage_user_accounts.group.model import Group
from collabinnovate.manage_user_accounts.notification.model import Notification
from collabinnovate.manage_user_accounts.session.model import Session
from collabinnovate.manage_user_accounts.user.model import User

class MashmallowNotification(ma.SQLAlchemyAutoSchema):
  class Meta:
    model = Notification
    
class MashmallowSession(ma.SQLAlchemyAutoSchema):
  class Meta:
    model = Session
    
class MashmallowAccount(ma.SQLAlchemyAutoSchema):
  class Meta:
    model = Account

class MashmallowGroup(ma.SQLAlchemyAutoSchema):
  class Meta:
    model = Group

class MashmallowComment(ma.SQLAlchemyAutoSchema):
  class Meta:
    model = Comment

class MashmallowFavoris(ma.SQLAlchemyAutoSchema):
  class Meta:
    model = Favoris
    
class MashmallowUser(ma.SQLAlchemyAutoSchema):
  notifications = ma.Nested(MashmallowNotification,many=True)
  accounts = ma.Nested(MashmallowAccount,many=True)
  groups = ma.Nested(MashmallowGroup,many=True)
  sessions = ma.Nested(MashmallowSession,many=True)
  comments = ma.Nested(MashmallowComment,many=True)
  favoris = ma.Nested(MashmallowFavoris,many=True)
  class Meta:
    model = User
    