
SECRET_KEY = 'WO2JxQLMzAMAnIZfRYbVtR8yfPPbfBSJ'

SECRET_JWT_KEY = "5ee06252f7b14d3ea2463ff9d4b65c44"
DEBUG = True 


#config email
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_USERNAME = 'melainenkeng@gmail.com'
MAIL_PASSWORD = 'vbpd ofhv muxm vhff'
MAIL_DEFAULT_SENDER = 'melainenkeng@gmail.com' 

#Cookies
JWT_TOKEN_LOCATION = ['cookies']
JWT_COOKIE_CSRF_PROTECT = True
JWT_ACCESS_COOKIE_PATH = '/' 
JWT_REFRESH_COOKIE_PATH = '/token/refresh'

#local bd connexion
LOCAL_DB_CONNEXION = {
  'host': 'localhost',
  'user': 'postgres',
  'password': '10322',
  'database': 'mercatodb',
  'port': '5432'
}



#distante bd connexion
DISTANT_DB_CONNEXION_POSTGRESQL = {
  'host': 'dpg-cqb7thmehbks73dl81ig-a.frankfurt-postgres.render.com',
  'user': 'mercatobd_saq8_user',
  'password': 'QuK5kxNL6mxbWh59TYajq6CeYfNvlGeP',
  'database': 'mercatobd_saq8',
  'port': '5432'
}

#distante bd connexion
DISTANT_DB_CONNEXION = {
  'host': 'collabinnovatedb.chkwyqi0uadk.eu-north-1.rds.amazonaws.com',
  'user': 'admin',
  'password': '1A2Z3E4R5T#',
  'database': 'mercatodb',
  'port': '3306'
}

#distante bd connexion
SQL_CONNEXION = {
  'host': 'localhost',
  'user': 'root',
  'password': '',
  'database': 'mercatodb',
}