from flask import Flask, g, flash, url_for, redirect, request, render_template, abort
from flask_security.decorators import login_required, roles_required
from flask_security.core import current_user
from flask_login import login_user, logout_user

from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore
from flask_wtf.csrf import CSRFProtect
from flask_admin import Admin
from flask_mail import Mail

app = Flask(__name__)
app.jinja_env.add_extension('jinja2.ext.loopcontrols')  # controls for break and continue
app.config.from_object('py_market.config')
mail = Mail(app=app)

# Глобальная защита CSRF для форм Flask
csrf = CSRFProtect(app)

# Объявление БД
db = SQLAlchemy(app)
db.drop_all()
db.metadata.clear()
# print("metadata keys: ", db.metadata.tables.keys())
# print("engine tables: ", db.engine.table_names())

# print("CREATING TABLES...\nmetadata keys: ", db.metadata.tables.keys())
# print("engine tables: ", db.engine.table_names())

from .models import User, Role
from py_market.admin_views import *
from py_market.forms import *

# Объявление security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore, login_form=CustomLoginForm, register_form=CustomRegisterForm)

# Объявление представлений админа
admin = Admin(app, template_mode='bootstrap3')
admin.add_view(UserView(User, db.session))
admin.add_view(RoleView(Role, db.session))
admin.add_view(ProductView(Product, db.session))
admin.add_views(BaseView(Material, db.session), BaseView(Category, db.session))
# admin.add_view(ProductPhotoView(ProductPhoto, db.session))

with app.app_context():
    db.metadata.create_all(db.engine)
    db.create_all()

from .routes import *
from .auth_routes import *