import os


# Connexion des bases de données
LOCAL_DB_CONNEXION = {
    'host': 'localhost',
    'user': 'postgres',
    'password': '10322',
    'database': 'mercatodb',
    'port': '5432'
}

DISTANT_DB_CONNEXION_POSTGRESQL = {
    'host': 'dpg-cqb7thmehbks73dl81ig-a.frankfurt-postgres.render.com',
    'user': 'mercatobd_saq8_user',
    'password': 'QuK5kxNL6mxbWh59TYajq6CeYfNvlGeP',
    'database': 'mercatobd_saq8',
    'port': '5432'
}

DISTANT_DB_CONNEXION = {
    'host': 'bllkz2rubsr6lxqhlttx-mysql.services.clever-cloud.com',
    'user': 'usbqefhqtsll6nh6',
    'password': 'AbOmXp99etO4zgXBZxH9',
    'database': 'bllkz2rubsr6lxqhlttx',
    'port': '3306'
}

SQL_CONNEXION = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'mercatodb',
}

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'WO2JxQLMzAMAnIZfRYbVtR8yfPPbfBSJ'
    SECRET_JWT_KEY = "5ee06252f7b14d3ea2463ff9d4b65c44"
    DEBUG = True 

    # Config email
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = 'melainenkeng@gmail.com'
    MAIL_PASSWORD = 'vbpd ofhv muxm vhff'
    MAIL_DEFAULT_SENDER = 'melainenkeng@gmail.com' 

    # Cookies
    JWT_TOKEN_LOCATION = ['cookies']
    JWT_COOKIE_CSRF_PROTECT = True
    JWT_ACCESS_COOKIE_PATH = '/' 
    JWT_REFRESH_COOKIE_PATH = '/token/refresh'
    JWT_COOKIE_SECURE = False  # Modifie en True si nécessaire en production


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{SQL_CONNEXION['user']}:{SQL_CONNEXION['password']}@{SQL_CONNEXION['host']}/{SQL_CONNEXION['database']}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DISTANT_DB_CONNEXION['user']}:{DISTANT_DB_CONNEXION['password']}@{DISTANT_DB_CONNEXION['host']}/{DISTANT_DB_CONNEXION['database']}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

