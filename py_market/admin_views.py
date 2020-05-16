from flask_admin.contrib.sqla import ModelView
from flask_admin.form.upload import ImageUploadField
from flask_admin import form
from flask_admin.form.widgets import Select2Widget
from wtforms.widgets import html_params, HTMLString
from flask_admin.helpers import get_url
from flask_admin._compat import string_types, urljoin
from flask_admin._backwards import Markup
from werkzeug.datastructures import FileStorage
from pathlib import Path
from py_market.models import *
import os, random

IMAGE_DIR_PRODUCTS = Path("static/images/products")
print("IMAGES PATH " + str(IMAGE_DIR_PRODUCTS))


class UserView(ModelView):
    can_delete = True
    can_create = True
    can_set_page_size = True

    column_hide_backrefs = False
    # column_select_related_list = (User.roles, roles_users.role_id)
    # column_list = ('email', 'password', ('roles', User.roles))
    # column_select_related_list = ("User", "Role")


class RoleView(ModelView):
    can_create = True
    can_edit = True
    can_delete = True
    # column_hide_backrefs = True
    column_list = ('name', 'description')


class ImageUploadInput:
    empty_template = ('<input %(file)s>')
    data_template = ('<div class="image-thumbnail">'
                     ' <img %(image)s multiple>'
                     ' <input type="checkbox" name="%(marker)s">Delete</input>'
                     ' <input %(text)s>'
                     '</div>'
                     '<input %(file)s>')

    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        kwargs.setdefault('name', field.name)

        template = self.data_template if field.data else self.empty_template

        if field.errors:
            template = self.empty_template

        if field.data and isinstance(field.data, FileStorage):
            value = field.data.filename
        else:
            value = field.data or ''

        return Markup(template % {
            'text': html_params(type='text',
                                readonly='readonly',
                                value=value,
                                name=field.name),
            'file': html_params(type='file',
                                value=value,
                                multiple=True,
                                **kwargs),
            'marker': '_%s-delete' % field.name
        })


class ProductView(ModelView):
    # can_delete = True
    can_create = True
    # inline_models = (ProductPhoto, )
    form_columns  = ['name',]
    inline_models = [(ProductPhoto,
                      dict(form_extra_fields={
                            'path': form.ImageUploadField(label='Image',
                                                          base_path=IMAGE_DIR_PRODUCTS,
                                                          max_size=(400, 400, True), )},
                            empty_template="<input %(file)s multiple>",
                            data_template=ImageUploadInput)
                     )]



