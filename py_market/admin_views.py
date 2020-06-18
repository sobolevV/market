from flask_admin.contrib.sqla import ModelView
from flask import request
from flask_admin.contrib.sqla.fields import QuerySelectField
from flask_admin.form.upload import ImageUploadField
from flask_admin import form

# from flask_admin.form.widgets import Select2Widget
# from wtforms.widgets import html_params, HTMLString
# from flask_admin.helpers import get_url
# from flask_admin._compat import string_types, urljoin
# from flask_admin._backwards import Markup

from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
from itsdangerous.serializer import Serializer
from pathlib import Path, PurePath
from py_market.models import *
import os
# import random
import os.path as op
from PIL import Image, ImageOps

IMAGE_DIR_PRODUCTS = Path(op.curdir).joinpath(Path("py_market\\static\\"))
print("IMAGES PATH " + str(IMAGE_DIR_PRODUCTS))
safe_url = Serializer("image-key")


class BaseView(ModelView):
    can_delete = True
    can_create = True
    can_set_page_size = True


class UserView(ModelView):
    can_delete = True
    can_create = True
    can_set_page_size = True
    column_hide_backrefs = False


class RoleView(ModelView):
    can_create = True
    can_edit = True
    can_delete = True
    # column_hide_backrefs = True
    column_list = ('name', 'description')


def image_name_gen(obj, file_data):
    root, ext = op.splitext(file_data.filename)
    root = safe_url.dumps(root)
    return secure_filename(f"p-{root}{ext}")


class MyImageUploadField(ImageUploadField):
    def _save_image(self, image, path, format='JPEG'):
        squared_size = max(image.size[0], image.size[1])
        image = ImageOps.fit(image, (squared_size, squared_size), Image.ANTIALIAS)
        self.image = image
        if image.mode not in ('RGB', 'RGBA'):
            image = image.convert('RGBA')

        with open(path, 'wb') as fp:
            image.save(fp, format)


class ProductView(ModelView):
    can_delete = True
    can_create = True
    can_edit = True
    column_hide_backrefs = False

    column_sortable_list = ("name", "arrival_date")
    inline_models = [(ProductPhoto,
                      dict(form_extra_fields={
                            'path': MyImageUploadField(label='Image',
                                                     base_path=str(IMAGE_DIR_PRODUCTS),
                                                     relative_path='images/products/',
                                                     namegen=image_name_gen,
                                                     max_size=(500, 500, True),
                                                     )})
                     )]

    # form_choices = {
    #     'my_form_field': [('material', Material.query.all()),]
    # }




