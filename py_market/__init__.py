import os
from flask import Flask, flash, g, url_for
from flask_admin import Admin
from flask_admin.base import MenuLink
from flask_mail import Mail
from flask_security import Security, SQLAlchemyUserDatastore
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate


BASE_DIR = os.path.abspath("./")

app = Flask(__name__)
app.jinja_env.add_extension('jinja2.ext.loopcontrols')
app.config.from_pyfile(os.path.join(BASE_DIR, "config.py"))

mail = Mail(app=app)

# Protection CSRF Token for Flask forms
csrf = CSRFProtect(app)
# DB declaration
db = SQLAlchemy(app)
with app.app_context():
    db.metadata.create_all(db.engine)
    db.create_all()

# Database migration
migrate = Migrate(app, db)

# security declaration
from py_market.forms import CustomLoginForm, CustomRegisterForm
from py_market.models import User, Role
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore, login_form=CustomLoginForm, register_form=CustomRegisterForm)

# Create first user - admin
if User.get_user_by_email(app.config["ADMIN_MAIL"]) is None:
    admin = User(name="Admin", email=app.config["ADMIN_MAIL"], password=app.config["ADMIN_PASSWORD"])
    if user_datastore.find_role(app.config["ADMIN_ROLE"]) is None:
        user_datastore.create_role(name=app.config["ADMIN_ROLE"])
    user_datastore.activate_user(admin)
    user_datastore.add_role_to_user(admin, user_datastore.find_role("Admin"))
    print("Admin created")

if app.config['SSL_REDIRECT']:
    from flask_sslify import SSLify
    # from werkzeug.contrib.fixers import ProxyFix
    sslify = SSLify(app)
    # app.wsgi_app = ProxyFix(app.wsgi_app)

# Routes at bottom
from py_market import routes

# Blueprints
from auth import auth
from my_admin import bp_admin
from products import products

app.register_blueprint(auth.bp_auth)
app.register_blueprint(bp_admin.bp_admin)
app.register_blueprint(products.bp_prods)
app.add_url_rule('/', endpoint='home')
