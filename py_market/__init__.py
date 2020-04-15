from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, login_required
from flask_security.forms import RegisterForm, LoginForm  # ForgotPasswordForm, ChangePasswordForm
from flask_wtf.csrf import CSRFProtect
from flask_admin import Admin

app = Flask(__name__)
app.config['SECRET_KEY'] = 'myseckretkey'
app.config['SECURITY_PASSWORD_SALT'] = 'mysecretsalt'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test.db"
app.config['SECURITY_CONFIRMABLE'] = True
# app.config['SECURITY_REGISTERABLE'] = True  # Возвращает стандартный шаблон от security

# Объявление БД
db = SQLAlchemy(app)

from py_market.models import User, Role

# Объявление security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

# Объявление админа
admin = Admin(app)

# Глобальная защита CSRF для форм Flask
csrf = CSRFProtect(app)

# Вниз файла т.к. содержит и обращение к БД и к security
from py_market import routes