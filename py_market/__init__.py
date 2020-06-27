import os
from flask import Flask, flash, g
from flask_admin import Admin
from flask_mail import Mail
from flask_security import Security, SQLAlchemyUserDatastore
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate

base_dir = os.path.abspath("./")

app = Flask(__name__)
app.jinja_env.add_extension('jinja2.ext.loopcontrols')
app.config.from_pyfile(os.path.join(base_dir, "config.py"))
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

# Flask-admin views
from py_market.models import *
from py_market.admin_views import *

admin = Admin(app, template_mode='bootstrap3')
admin.add_view(UserView(User, db.session))
admin.add_view(RoleView(Role, db.session))
admin.add_view(ProductView(Product, db.session))
admin.add_views(BaseView(Material, db.session), BaseView(Category, db.session))
# admin.add_view(ProductPhotoView(ProductPhoto, db.session))

from py_market.forms import *
# security declaration
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore, login_form=CustomLoginForm, register_form=CustomRegisterForm)

# Always at bottom
from py_market import routes, auth_routes