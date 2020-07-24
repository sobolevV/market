from py_market import app
from flask_admin import Admin
from flask import Blueprint
# Flask-admin views
from py_market.models import *
from .admin_views import *
from os import path

admin = Admin(app, template_mode='bootstrap3', index_view=MyHomeView(name="Главная"))
admin.add_view(UserView(User, db.session, category="Пользователи", name="Пользователь"))
admin.add_view(RoleView(Role, db.session, category="Пользователи", name="Роли"))
admin.add_view(ProductView(Product, db.session, category="Товар", name="Товар"))
admin.add_views(DefaultView(Material, db.session, category="Товар", name="Материалы/состав товара"),
                DefaultView(Category, db.session, category="Товар", name="Категории товара "))
admin.add_view(NewsEditor(endpoint="news", name="Добавить новость"))

bp_admin = Blueprint('bp_admin', __name__,
                     url_prefix='/admin',
                     template_folder="templates",
                     static_folder="static", static_url_path="my_admin/static")
