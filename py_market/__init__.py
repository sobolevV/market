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