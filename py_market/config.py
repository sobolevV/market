from .mail_config import *

# Config for default Flask
SECRET_KEY = 'myseckretkey'
SECURITY_PASSWORD_SALT = 'mysecretsalt'
CSRF_ENABLED = True

# Config for Flask-sqlalchemy
# SECURITY_LOGIN_USER_TEMPLATE = "custom/login.html"
SQLALCHEMY_DATABASE_URI = "sqlite:///test.db"
SQLALCHEMY_ECHO = True
