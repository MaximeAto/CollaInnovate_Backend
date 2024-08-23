from flask import Flask, request, has_request_context
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from collabinnovate import config
from flask_migrate import Migrate
from flask_mail import Mail
from flask_marshmallow import Marshmallow 
import logging
from logging.handlers import RotatingFileHandler
from flask_swagger_ui import get_swaggerui_blueprint

db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()
mail = Mail()

class LogginFormatter(logging.Formatter):
  def format(self, record):
    if has_request_context :
      record.url = request.url
      record.remote = request.remote_addr
    else : 
      record.url = None
      record.remote = None
    return super().format(record)
  
class Role(db.Model):
  __tablename__ = "role"
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  name = db.Column(db.String(5), unique=True, nullable=False)
  description = db.Column(db.Text)

  users = db.relationship('User', backref='role')

class Group(db.Model):
  __tablename__ = "group"
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  name = db.Column(db.String(5), nullable=False)
  description = db.Column(db.Text)

  users = db.relationship('User', backref='group')

def insert_initial_data():
  if Role.query.first() is None and Group.query.first() is None:
    roles = [
        Role(name='Admin', description='Administrator role'),
        Role(name='User', description='User role'),
        Role(name='Investor', description='Investor role')
    ]
    
    groups = [
        Group(name='Guser', description='Guser description'),
        Group(name='Ginvestor', description='Ginvestor description'),
        Group(name='Gadmin', description='Gadmin description')
    ]

    db.session.bulk_save_objects(roles)
    db.session.bulk_save_objects(groups)
    db.session.commit()



def create_app():
  #create the instance of flask app
  app = Flask(__name__,  template_folder='templates', static_folder='static')
  CORS(app, supports_credentials=True)
  
  # db_config = config.LOCAL_DB_CONNEXION
  db_config = config.SQL_CONNEXION
  
  app.config['SECRET_KEY'] = config.SECRET_KEY
  app.config['JWT_TOKEN_LOCATION'] = ['cookies']
  app.config['JWT_COOKIE_CSRF_PROTECT'] = config.JWT_COOKIE_CSRF_PROTECT
  app.config['JWT_ACCESS_COOKIE_PATH'] = config.JWT_ACCESS_COOKIE_PATH
  app.config['JWT_REFRESH_COOKIE_PATH'] = config.JWT_REFRESH_COOKIE_PATH
  app.config['JWT_COOKIE_SECURE'] = False
  app.config['JWT_SESSION_COOKIE'] = False
  app.config.from_object(config)
  
  # Configuration pour MySQL avec XAMPP sans nom d'utilisateur ni mot de passe
  app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{db_config['user']}:{db_config['password']}@{db_config['host']}/{db_config['database']}"
  
  # app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql+psycopg2://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}"
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
  
  db.init_app(app=app)
  migrate.init_app(app=app, db=db)
  ma.init_app(app)
  mail.init_app(app=app)
  
  # Configuration de la journalisation
  logging.basicConfig(level=logging.INFO)
  formatter = LogginFormatter('%(asctime)s - %(url)s - %(remote)s - %(levelname)s - %(message)s')

  # Créer un enregistreur de journalisation pour écrire dans un fichier
  file_handler = RotatingFileHandler('logs/activity.log', maxBytes=10240, backupCount=10)
  file_handler.setFormatter(formatter)
  file_handler.setLevel(logging.INFO)
  
  app.logger.addHandler(file_handler)

  SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
  API_URL = '/static/swagger.json'

  # Call factory function to create our blueprint
  swaggerui_blueprint = get_swaggerui_blueprint(
      SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
      API_URL,
      config={  # Swagger UI config overrides
          'app_name': "CollabInnovate.Api"
      },
      # oauth_config={  # OAuth config. See https://github.com/swagger-api/swagger-ui#oauth2-configuration .
      #    'clientId': "your-client-id",
      #    'clientSecret': "your-client-secret-if-required",
      #    'realm': "your-realms",
      #    'appName': "your-app-name",
      #    'scopeSeparator': " ",
      #    'additionalQueryStringParams': {'test': "hello"}
      # }
  )


  with app.app_context():
    from collabinnovate.manage_user_accounts.account.routes import accounts
    from collabinnovate.manage_user_accounts.authentification.routes import auth
    from collabinnovate.manage_user_accounts.edit.routes import edit
    from collabinnovate.manage_user_accounts.invitation.routes import invitations
    from collabinnovate.manage_user_accounts.journalisation.routes import journalisations
    from collabinnovate.manage_user_accounts.password.routes import password
    from collabinnovate.manage_user_accounts.session.routes import sessions
    from collabinnovate.manage_user_accounts.user.routes import users
    from collabinnovate.manage_user_accounts.notification.routes import notifications
    from collabinnovate.manage_problems.routes import problems
    from collabinnovate.manage_solutions.routes import solutions
    from collabinnovate.manage_solutions.comments.routes import comments
    from collabinnovate.manage_solutions.mentions.routes import mentions
    from collabinnovate.manage_favoris.routes import favoris


    app.register_blueprint(swaggerui_blueprint)

        
    app.register_blueprint(accounts, url_prefix='/accounts')
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(edit, url_prefix='/edit')
    app.register_blueprint(invitations, url_prefix='/invitations')
    app.register_blueprint(journalisations, url_prefix='/journalisations')
    app.register_blueprint(password, url_prefix='/password')
    app.register_blueprint(sessions, url_prefix='/sessions')
    app.register_blueprint(favoris, url_prefix='/favoris')
    app.register_blueprint(users, url_prefix='/users')
    app.register_blueprint(problems, url_prefix='/problems')
    app.register_blueprint(solutions, url_prefix='/solutions')
    app.register_blueprint(notifications, url_prefix='/notifications')
    app.register_blueprint(comments, url_prefix='/comments')
    app.register_blueprint(mentions, url_prefix='/mentions')

    db.create_all()
    insert_initial_data()
    
  return app


