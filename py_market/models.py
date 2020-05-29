from py_market import db
from flask_security import UserMixin, RoleMixin
from datetime import date

# not good
ROLE_USER = "user"
ROLE_ADMIN = "admin"

# roles_users many_to_many
roles_users = db.Table("roles_users",
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
    name = db.Column(db.String(30), default=ROLE_USER)
    description = db.Column(db.String(100), nullable=True, )
    user_id = db.Column(db.Integer, db.ForeignKey("User.id"))

    def __repr__(self):
        return f"Name: {self.name}"


class Address(db.Model):
    """Address to ship product"""
    __tablename__ = "Address"

    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(150), nullable=True)


# ____Define models for products____
# products_materials many to many
# products_materials = db.Table("products_materials", db.Model.metadata,
#                               db.Column('product_id', db.Integer, db.ForeignKey("Product.id")),
#                               db.Column('material_id', db.Integer, db.ForeignKey("Material.id")))


class Product(db.Model):
    """Product"""
    __tablename__ = "Product"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    name = db.Column(db.String(100), nullable=False)
    # Float
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(200))
    arrival_date = db.Column(db.Date(), default=date.today())

    # category = db.Column(db.Integer, db.ForeignKey("Category.id"))
    # material = db.Column(db.Integer, db.ForeignKey("Material.id"))
    # photos_id = db.Column(db.Integer, db.ForeignKey("ProductPhoto.id"))
    # photos = db.relationship("ProductPhoto", backref="product", lazy=False, foreign_keys=[photos_id])


class Material(db.Model):
    """Product materials"""
    __tablename__ = "Material"

    id = db.Column(db.Integer, primary_key=True)

    product_id = db.Column(db.Integer, db.ForeignKey("Product.id"))
    products = db.relationship("Product", backref="material", lazy="subquery", foreign_keys=[product_id])
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=True)


class Category(db.Model):
    """Category of product"""
    __tablename__ = "Category"

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("Product.id"))
    products = db.relationship("Product", backref="category", lazy="subquery", foreign_keys=[product_id])
    name = db.Column(db.String(100), nullable=False, unique=True)


class ProductPhoto(db.Model):
    """Photos for product"""
    __tablename__ = "ProductPhoto"

    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(250))
    products = db.Column(db.Integer, db.ForeignKey(Product.id))
    product = db.relationship(Product, backref=db.backref("photos", lazy="subquery"), foreign_keys=[products])

    def __repr__(self):
        return f"<ProductPhoto: {self.path}>"


class Pstorage(db.Column):
    """Count of each product at storage"""
    __tablename__ = "Pstorage"

    id = db.Column(db.Integer, primary_key=True)
    size = db.Column(db.Integer)
    count = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"ID: {self.id}, size: {self.size}, count: {self.count}"

