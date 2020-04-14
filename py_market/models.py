from py_market import db


class Admin(db.Model):
    """Админ сайта"""
    def __init__(self):
        pass

    def __repr__(self):
        pass


class User(db.Model):
    """Зарегистрированный пользователь сайта"""
    def __init__(self):
        pass

    def __repr__(self):
        pass


class Product(db.Model):
    """Продукт, который может приобрести и заказать user"""
    def __init__(self):
        pass

    def __repr__(self):
        pass