import os
from py_market import app
from py_market.models import Product, Category, Material, News
from flask_security.core import current_user
from flask_login.utils import login_required, login_user, logout_user
from sqlalchemy import desc
from flask import g, flash, url_for, redirect, request, render_template, abort, session, send_from_directory


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static\\images'),
                               'icon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/home')
@app.route('/')
def home():
    """Main - home page"""
    products = Product.query.order_by(Product.arrival_date).limit(app.config["ITEMS_PER_PAGE"]).all()
    categories = Category.query.all()
    titles = News.query.all()
    return render_template("py_market/home.html",
                           title="Главная страница",
                           products=products,
                           categories=categories,
                           titles=titles)


@app.route('/news/target=<int:id>', methods=("GET", ))
def news(id):
    title = News.query.get_or_404(id)
    return render_template("py_market/title.html", title=title)


@app.route('/about')
def about():
    """About page"""
    return render_template("py_market/about.html", title="О нас")


@app.route('/cart')
@login_required
def cart():
    # Product.query.select_from(User).join(Cart, Product.id == Cart.product_id).filter(User.id == 1).all()
    """Page with user product"""
    flash(f"Your cart {current_user.name}")
    return render_template("py_market/base.html")


@app.route('/profile')
@login_required
def profile():
    """Page with user data"""
    return render_template("py_market/profile.html")


# Global user. was - before_request
@app.before_request
def before_request():
    if current_user:
        g.user = current_user
    # if not request.path.startswith(url_for("products")) and "form_filter" in session:
    #     del session["form_filter"]


# Return to all templates
@app.context_processor
def inject_user():
    if current_user:
        return dict(user=g.user)


# Handle errors
@app.errorhandler(404)
def page_not_found(e):
    """Not found page"""
    return render_template('py_market/base.html', info="404 Error"), 404


@app.errorhandler(400)
def page_not_found(e):
    """Not found page"""
    return render_template('py_market/base.html', info="404 Error"), 400


@app.errorhandler(500)
def server_error(e):
    """Server error page"""
    return render_template('py_market/base.html', info="500 Server Error"), 500
