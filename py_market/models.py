from py_market import db, BASE_DIR
from flask import url_for
from sqlalchemy import event
from flask_security import UserMixin, RoleMixin
from datetime import date
from random import randint, choice
from pathlib import PurePath
import os

# roles_users many_to_many
roles_users = db.Table("roles_users", db.metadata,
                       db.Column('user_id', db.Integer, db.ForeignKey('User.id')),
                       db.Column('role_id', db.Integer, db.ForeignKey('Role.id'))
                       )


# ____Define models for users____
class User(db.Model, UserMixin):
    __tablename__ = "User"

    # Main attrs
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    last_visit = db.Column(db.Date(), nullable=True)

    # For Flask-login
    active = db.Column(db.Boolean())
    is_auth = db.Column(db.Boolean(), default=False)
    confirmed_at = db.Column(db.DateTime())

    # Relations (FK)
    roles = db.relationship("Role", backref=db.backref("users", lazy=True), uselist=True) # , secondary="roles_users"
    address_id = db.Column(db.Integer, db.ForeignKey("Address.id"))
    address = db.relationship("Address", backref=db.backref("users", lazy=True))

    def __repr__(self):
        return f"<User id={self.id}, email={self.email}"

    @property
    def is_authenticated(self) -> bool:
        """:returns True if user activated account"""
        return self.is_auth

    @property
    def is_active(self):
        return self.active

    @staticmethod
    def get_user_by_email(email: str):
        """:returns User object if email in db,
                    else None
        """
        return User.query.filter_by(email=email).first()

    def auth_user(self):
        """Activate current user, commit in db"""
        self.active = True
        self.is_auth = True
        self.confirmed_at = date.today()
        db.session.commit()


class Role(db.Model, RoleMixin):
    """Roles for user. One or more roles for one user"""
    __tablename__ = "Role"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), default="User")
    description = db.Column(db.String(100), nullable=True, )
    user_id = db.Column(db.Integer, db.ForeignKey("User.id"))

    def __repr__(self):
        return f"Name: {self.name}"


class Address(db.Model):
    """Address to ship product"""
    __tablename__ = "Address"

    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(150), nullable=True)


class News(db.Model):
    """News for main page of web site"""
    __tablename__ = "News"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300))
    description = db.Column(db.String(300))
    text = db.Column(db.Text())
    image_url = db.Column(db.String(400))

    @staticmethod
    def from_request(request):
        html_data = request.form["html"].strip()
        title = request.form["title"]
        desc = request.form["description"]
        image_url = request.form["image_url"]
        if len(image_url) == 0:
            image_url = url_for('static', filename=f"/images/news/bg_news_{randint(1, 4)}.jpg")
            # try:
            #     path = PurePath(url_for("static")).joinpath(PurePath("images/news/"))
            #     img_name = choice(os.listdir(path))
            #     image_url = path.joinpath(img_name)
            # except Exception as e:
            #     print(e)
        return News(title=title, description=desc, text=html_data, image_url=image_url)


products_categories = db.Table("products_categories", db.metadata,
                                db.Column('product_id', db.Integer, db.ForeignKey('Product.id')),
                                db.Column('category_id', db.Integer, db.ForeignKey('Category.id'))
                               )


class Product(db.Model):
    """Product"""
    __tablename__ = "Product"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    male = db.Column(db.Boolean, nullable=True)
    brand = db.Column(db.String(100), nullable=True)
    description = db.Column(db.String(200))
    arrival_date = db.Column(db.Date(), default=date.today())

    def __repr__(self):
        return f"<Product: id={self.id}, name={self.name}>"


@event.listens_for(Product, 'after_delete')
def receive_after_delete(mapper, connection, target):
    print(target, "deleted. image paths ", target.photos)
    if target.photos:
        for photo_obj in target.photos:
            # BASE_DIR
            file_path = PurePath(BASE_DIR, "py_market\\static\\", photo_obj.path)
            if os.path.exists(str(file_path)):
                try:
                    os.remove(str(file_path))
                except Exception as e:
                    print(e)


class Material(db.Model):
    """Product materials"""
    __tablename__ = "Material"

    id = db.Column(db.Integer, primary_key=True)

    product_id = db.Column(db.Integer, db.ForeignKey("Product.id"))
    products = db.relationship("Product",
                               backref=db.backref("material", lazy="select"),
                               lazy="subquery",
                               foreign_keys=[product_id],
                               uselist=True)

    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=True)


class Category(db.Model):
    """Category of product"""
    __tablename__ = "Category"

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("Product.id"))
    products = db.relationship("Product",
                               backref=db.backref("category", lazy="select", uselist=True),
                               secondary=products_categories,
                               uselist=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

    def __repr__(self):
        return f"{self.name}"


class ProductPhoto(db.Model):
    """Photos for product"""
    __tablename__ = "ProductPhoto"

    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(250))
    products = db.Column(db.Integer, db.ForeignKey(Product.id))
    product = db.relationship(Product,
                              backref=db.backref("photos", lazy="subquery"),
                              foreign_keys=[products])

    def __repr__(self):
        return f"<ProductPhoto: {self.path}>"


# # # # # # # # # # # # # #
class Pstorage(db.Model):
    """Count of each product at storage"""
    __tablename__ = "Pstorage"

    id = db.Column(db.Integer, primary_key=True)
    size = db.Column(db.Integer)
    count = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"ID: {self.id}, size: {self.size}, count: {self.count}"

# # # # # # # # # # # # # #


class Cart(db.Model):
    __tablename__ = "Cart"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("User.id"))
    product_id = db.Column(db.Integer, db.ForeignKey("User.id"))
    count = db.Column(db.SmallInteger, default=1)
    add_date = db.Column(db.Date(), default=date.today())