from py_market import db
from flask_security import UserMixin, RoleMixin

# Таблица связей
roles_users = db.Table("roles_users",
                       db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class User(db.Model, UserMixin):
    """Registered user"""
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    def __repr__(self):
        return f"<User id={self.id}, email={self.email}"


class Role(db.Model, RoleMixin):
    """User Role type"""
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __repr__(self):
        return f"ID: {self.id}, Name: {self.name}"


# class Product(db.Model):
#     """Product for sale"""
#     pass

