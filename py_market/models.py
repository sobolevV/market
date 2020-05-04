from py_market import db
from flask_security import UserMixin, RoleMixin

ROLE_USER = "user"
ROLE_ADMIN = "admin"

# roles_users many_to_many
roles_users = db.Table("roles_users",
                       db.Column('user_id', db.Integer, db.ForeignKey('User.id'), primary_key=True),
                       db.Column('role_id', db.Integer, db.ForeignKey('Role.id'), primary_key=True), extend_existing=True)
roles_users

# ____Define models for users____


class User(db.Model, UserMixin):
    __tablename__ = "User"
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users, lazy="dynamic",
                            backref=db.backref('users', lazy='dynamic'))

    name = db.Column(db.String(200), nullable=False)
    sex = db.Column(db.Boolean)
    address = db.relationship('Address', backref=db.backref('user', lazy=True))

    def __repr__(self):
        return f"<User id={self.id}, email={self.email}"


class Role(db.Model, RoleMixin):
    """Roles for user. One or more roles for one user"""
    __tablename__ = "Role"

    id = db.Column(db.SmallInteger, primary_key=True)
    name = db.Column(db.String(50), unique=True, default=ROLE_USER)
    description = db.Column(db.String(100))
    # + user

    def __repr__(self):
        return f"Name: {self.name}, role id: {self.id}"


class Address(db.Model):
    """Address to ship product"""
    __tablename__ = "Address"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("User.id"), nullable=False)
    address = db.Column(db.String(150), nullable=True)

    def __repr__(self):
        return f"<User id: {self.user_id}, address: {self.address}>"


# ____Define models for products____
# products_materials many to many
products_materials = db.Table("products_materials", db.Model.metadata,
                              db.Column('product_id', db.Integer, db.ForeignKey("Product.id")),
                              db.Column('material_id', db.Integer, db.ForeignKey("Material.id")))

# db.Column('id', db.Integer, primary_key=True),


class Product(db.Model):
    """Product"""
    __tablename__ = "Product"
    id = db.Column(db.Integer, primary_key=True)

    type_id = db.Column(db.Integer, db.ForeignKey("Type.id"), nullable=False)
    material_id = db.Column(db.Integer, db.ForeignKey(products_materials.c.material_id))

    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    arrival_date = db.Column(db.Date(), nullable=False)
    description = db.Column(db.String(100), nullable=True)
    # sale - Скидка (to future)

    def __repr__(self):
        return f"<Name {self.name}>, id: {self.id}"


class Material(db.Model):
    """Product materials"""
    __tablename__ = "Material"

    id = db.Column(db.Integer, primary_key=True)
    products = db.relationship(Product, secondary=products_materials,
                               secondaryjoin=(products_materials.c.material_id == id),
                               primaryjoin=(products_materials.c.product_id == Product.id),
                               lazy="dynamic",
                               backref=db.backref('materials', lazy="dynamic"))

    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=True)


class Type(db.Model):
    __tablename__ = "Type"

    id = db.Column(db.Integer, primary_key=True)
    products = db.relationship("Product", lazy="dynamic", backref='type')
    # product_id = db.Column(db.Integer, db.ForeignKey("Product.id"), nullable=False)

    name = db.Column(db.String(100), nullable=False, unique=True)


class Pstorage(db.Column):
    __tablename__ = "Pstorage"

    id = db.Column(db.Integer, primary_key=True)
    products = db.relationship("Product", lazy="dynamic", backref='in_storage')
    size = db.Column(db.Integer)
    count = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"ID: {self.id}, size: {self.size}, count: {self.count}"
