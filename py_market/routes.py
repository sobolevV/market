from py_market import app, security, admin, g, flash, request
from py_market import Product

from flask import Flask, g, flash, url_for, redirect, request, render_template, abort
from flask_security.decorators import login_required, roles_required
from flask_security.core import current_user
from flask_login import login_user, logout_user

from flask_login.utils import login_required, login_user
# from .auth_routes import register, login
from .models import Product, Category


@app.route('/')
def home():
    products = Product.query.all()
    categories = Category.query.all()
    return render_template("index.html",
                           title="Главная страница",
                           products=products,
                           categories=categories)


@app.route('/product/target=<int:id>')
def show_product_page(id):
    target_product = Product.query.filter(Product.id == id).first_or_404()
    return render_template("product_page.html", product=target_product)


# About us
@app.route('/about')
def about():
    return render_template("about.html", title="О нас")


# User cart
@app.route('/cart')
@login_required
def cart():
    flash(f"Your cart {current_user.name}")
    return render_template("base.html")


# User profile
@app.route('/profile')
@login_required
def profile():
    flash(f"Your profile {current_user.name}", "message")
    return render_template("base.html")


# Global user
@app.before_request
def before_request():
    g.user = current_user


# Return to all templates
@app.context_processor
def inject_user():
    return dict(user=g.user)


# Handle errors
@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('index.html', info="404 Error"), 404


@app.errorhandler(500)
def page_not_found(e):
    return render_template('index.html', info="500 Server Error"), 500
