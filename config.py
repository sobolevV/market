import os
from mail_config import *

basedir = os.path.abspath(os.path.dirname(__file__))

# Config for default Flask
SECRET_KEY = 'myseckretkey'
SECURITY_PASSWORD_SALT = 'mysecretsalt'
CSRF_ENABLED = True

MAX_CONTENT_LENGTH = 24 * 1024 * 1024

# Config for Flask-sqlalchemy
# SECURITY_LOGIN_USER_TEMPLATE = "custom/login.html"
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'test.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = False

ITEMS_PER_PAGE = 16
