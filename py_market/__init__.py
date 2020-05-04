from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore
from flask_wtf.csrf import CSRFProtect
from flask_admin import Admin
from flask_security.utils import url_for_security

app = Flask(__name__)
app.jinja_env.add_extension('jinja2.ext.loopcontrols')  # controls for break and continue
app.config.from_object('py_market.config')


# app.config['SECURITY_CONFIRMABLE'] = True
# app.config['SECURITY_REGISTERABLE'] = True  # Возвращает стандартный шаблон от security

# Объявление БД
db = SQLAlchemy(app)
db.create_all()

from py_market.models import User, Role
from py_market.market_wtf_forms import *

u = User(email="email@ru", password="pass", name="userName")
# Объявление security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore, login_form=CustomLoginForm, register_form=CustomRegisterForm)

# Объявление админа
admin = Admin(app)

# Глобальная защита CSRF для форм Flask
csrf = CSRFProtect(app)

# Вниз файла т.к. содержит и обращение к БД и к security
from py_market import routes, user_routes