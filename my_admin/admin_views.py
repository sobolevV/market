from flask_admin.contrib.sqla import ModelView
from flask_admin.form.upload import ImageUploadField
from flask_admin import BaseView, AdminIndexView, expose
from flask_security import current_user
from flask import abort, request, jsonify, url_for, redirect
from werkzeug.utils import secure_filename
from itsdangerous.serializer import Serializer

from py_market import BASE_DIR, app, db
from py_market.models import ProductPhoto, User, Product, News

from pathlib import Path, PurePath
from PIL import Image, ImageOps

import os.path as op

STATIC_DIR = Path(BASE_DIR).joinpath(Path("py_market\\static\\"))
safe_url = Serializer("image-key")


class RoleModelView(ModelView):
    # Setup access only for Admin
    def is_accessible(self):
        if current_user.has_role(app.config["ADMIN_ROLE"]):
            return True
        abort(403)


class DefaultView(RoleModelView):
    can_delete = True
    can_create = True
    can_set_page_size = True


class UserView(RoleModelView):
    can_delete = True
    can_create = True
    can_set_page_size = True
    # column_hide_backrefs = False


class RoleView(RoleModelView):
    can_create = True
    can_edit = True
    can_delete = True
    # column_hide_backrefs = True
    column_list = ('name', 'description')


def image_name_gen(obj, file_data):
    """Generates name for image"""
    root, ext = op.splitext(file_data.filename)
    # Save only first part of image name
    if len(root) > 10:
        root = root[:10]
    return secure_filename(f"{root}{ext}")


class MyImageUploadField(ImageUploadField):
    def _save_image(self, image, path, format='JPEG'):
        squared_size = max(image.size[0], image.size[1])
        image = ImageOps.fit(image, (squared_size, squared_size), Image.ANTIALIAS)
        self.image = image
        if image.mode not in ('RGB', 'RGBA'):
            image = image.convert('RGBA')

        with open(path, 'wb') as fp:
            image.save(fp, format)


class ProductView(RoleModelView):
    can_delete = True
    can_create = True
    can_edit = True
    column_hide_backrefs = False

    column_sortable_list = ("name", "arrival_date")
    inline_models = [(ProductPhoto,
                      dict(form_extra_fields={
                            'path': MyImageUploadField(label='Image',
                                                       base_path=str(STATIC_DIR),
                                                       relative_path='images/products/',
                                                       namegen=image_name_gen,
                                                       max_size=(550, 550, True),
                                                       )})
                     )]


class MyHomeView(AdminIndexView):
    """Main admin page with some information"""
    @expose('/')
    def home(self):
        products_query = Product.query
        users_query = User.query
        data = {"products": {
                    "title": "Товар",
                    "count": products_query.count(),
                    "last_date": products_query.order_by(Product.arrival_date).first().arrival_date},
                "users": {
                    "title": "Пользователи",
                    "count": users_query.count()}
                }
        return self.render('admin/index.html', data=data)


class NewsEditor(BaseView):
    """Admin editor to create news for main page of web-site"""
    @expose('/')
    def base(self):
        """Show existing news"""
        news = News.query.all()
        return self.render("my_admin/news.html", news=news)

    @expose('/create', methods=("GET", "POST"))
    def create(self):
        """Create new title"""
        if request.method == "POST":
            # Post to get image
            if 'image' in request.files:
                file = request.files["image"]
                filename = image_name_gen(obj=None, file_data=file)
                file_path = Path(STATIC_DIR, "images/news/", filename)
                file.save(file_path)
                return jsonify({"url": url_for('static', filename="images/news/"+filename)})
            # Post to save all HTML data
            if "html" in request.form:
                new_title = News.from_request(request=request)
                db.session.add(new_title)
                db.session.commit()
            return redirect(url_for('news.base'))

        return self.render("my_admin/news_create.html")

    def is_accessible(self):
        """Setup access only for Admin"""
        if current_user.has_role(app.config["ADMIN_ROLE"]):
            return True
        abort(403)

