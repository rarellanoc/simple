import os
basedir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = 'SET T0 4NY SECRET KEY L1KE RAND0M H4SH'

#SQLALCHEMY_DATABASE_URI = 'mysql://madeer_dbuser:madeer-2015@mysql.madeer.cl/jugando'

SQLALCHEMY_DATABASE_URI = 'mysql://mac:mac-2015@192.168.2.8/jugando'




MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = 'madeer.lab'
MAIL_PASSWORD = 'chaohola321'


