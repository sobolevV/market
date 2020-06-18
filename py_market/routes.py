from py_market import app, security, admin, g, flash, request
from py_market import Product
from  py_market.forms import FilterProductsForm

from flask import Flask, g, flash, url_for, redirect, request, render_template, abort
from flask_security.decorators import login_required, roles_required
from flask_security.core import current_user
from flask_login import login_user, logout_user
from flask_login.utils import login_required, login_user
from flask_wtf import FlaskForm
# from .auth_routes import register, login
from .models import Product, Category, Material

global filter_tables
filter_tables = {"category", "material"}


@app.route('/')
def home():
    """Main - home page"""
    products = Product.query.all()
    categories = Category.query.all()
    return render_template("index.html",
                           title="Главная страница",
                           products=products,
                           categories=categories)


def products_filter(products_model, form):
    filtered_products = products_model.query

    # Check activated filters by user
    for key in form.keys():
        # if user selected any item by key
        if key in filter_tables and len(form.getlist(key)) > 0:
            if key.title() == Category.__tablename__:
                categories = Product.category.any(Category.name.in_(form.getlist(key)))
                filtered_products = filtered_products.filter(categories)
            if key.title() == Material.__tablename__:
                materials = Product.category.any(Material.name.in_(form.getlist(key)))
                filtered_products = filtered_products.filter(materials)

    if form['minPrice']:
        filtered_products = filtered_products.filter(Product.price >= int(form['minPrice']))
    if form['maxPrice']:
        filtered_products = filtered_products.filter(Product.price <= int(form['maxPrice']))

    return filtered_products.all()


@app.route('/products/category=<string:category_name>', methods=["POST", "GET"])
@app.route('/products/', methods=["POST", "GET"])
def product_filter(category_name=None):
    """Page with filtered products"""
    # form = request.form
    form_filter = FilterProductsForm(request.form)
    if category_name is not None:
        form_filter.category.data = form_filter.category.data + [category_name]
        return redirect("/products")
    if request.method == "POST":
        target_products = products_filter(Product, request.form)
    else:
        target_products = Product.query.all()

    return render_template("index.html", products=target_products, filter=form_filter)


@app.route('/product/target=<int:id>')
def show_product_page(id):
    """Page with Product description"""
    target_product = Product.query.filter(Product.id == id).first_or_404()
    return render_template("product_page.html", product=target_product)


@app.route('/about')
def about():
    """About page"""
    return render_template("about.html", title="О нас")


@app.route('/cart')
@login_required
def cart():
    """Page with user product"""
    flash(f"Your cart {current_user.name}")
    return render_template("base.html")


@app.route('/profile')
@login_required
def profile():
    """Page with user data"""
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
    """Not found page"""
    return render_template('index.html', info="404 Error"), 404


@app.errorhandler(500)
def server_error(e):
    """Server error page"""
    return render_template('index.html', info="500 Server Error"), 500
