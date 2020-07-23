import os
from mail_config import *

basedir = os.path.abspath(os.path.dirname(__file__))

# Config for default Flask
SECRET_KEY = os.environ.get("SECRET_KEY")
SECURITY_PASSWORD_SALT = os.environ.get("SECRET_SALT")
USER_ROLE = "User"
ADMIN_ROLE = "Admin"
CSRF_ENABLED = True

MAX_CONTENT_LENGTH = 24 * 1024 * 1024

# Config for Flask-sqlalchemy
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'test.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = False

ITEMS_PER_PAGE = 16

# Admin data
ADMIN_MAIL = os.environ.get('ADMIN_MAIL')
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD')

# SSL
SSL_REDIRECT = True if os.environ.get('DYNO') else False
