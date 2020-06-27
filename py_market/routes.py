import os
from py_market import app
from py_market.models import Product, Category, Material
from py_market.forms import FilterProductsForm
from flask_security.core import current_user
from flask_login.utils import login_required, login_user, logout_user
from sqlalchemy import desc
from flask import g, flash, url_for, redirect, request, render_template, abort, session, send_from_directory

global filter_tables
filter_tables = {"category", "material"}


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static\\images'),
                               'icon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/editor', methods=["GET", "POST"])
def editor():
    # https://github.com/pavittarx/editorjs-html
    if request.method == "POST":
        if 'image' in request.files:
            file = request.files
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], "filename.jpg"))
        # if any data
        # convert json to string
        # save to db
    return render_template("_empty.html")


@app.route('/home')
@app.route('/')
def home():
    """Main - home page"""
    products = Product.query.order_by(Product.arrival_date).limit(app.config["ITEMS_PER_PAGE"]).all()
    categories = Category.query.all()
    return render_template("home.html",
                           title="Главная страница",
                           products=products,
                           categories=categories)


def products_filter(products_model, form_data):
    filtered_products = products_model.query

    # Check activated filters by user
    for key in filter_tables:
        # if user selected any item by key
        if key in form_data.keys() and form_data[key]:
            filter_list = (form_data[key],) if isinstance(form_data[key], str) else (val for val in form_data[key])
            if key.title() == Category.__tablename__:
                categories = Product.category.any(Category.name.in_(filter_list))
                filtered_products = filtered_products.filter(categories)
            if key.title() == Material.__tablename__:
                materials = Product.category.any(Material.name.in_(filter_list))
                filtered_products = filtered_products.filter(materials)

    if form_data['minPrice']:
        filtered_products = filtered_products.filter(Product.price >= int(form_data['minPrice']))
    if form_data['maxPrice']:
        filtered_products = filtered_products.filter(Product.price <= int(form_data['maxPrice']))

    if form_data["order"]:
        if form_data["order"].startswith("price"):
            order_column = Product.price
        else:
            order_column = Product.arrival_date
        if form_data["order"].endswith("desc"):
            order_column = desc(order_column)
        filtered_products = filtered_products.order_by(order_column)
    return filtered_products


# @app.route('/products/page=<int:page>', methods=["POST", "GET"])
@app.route('/products/', methods=["POST", "GET"])
def products():
    """Page with filtered products"""
    page = 1
    # Get arguments for filtering
    request_args = request.args.to_dict(flat=False)
    if "page" in request_args:
        page = int(request_args["page"][0])
        del request_args["page"]

    # If request contains any arguments

    #     if "form_filter" not in session or session["form_filter"] != request_args:
    #         session["form_filter"] = request_args
    #
    # # If already was request
    # if "form_filter" in session and len(session["form_filter"]):
    #     # Generate form field for user
    if len(request_args):
        form_filter = FilterProductsForm().from_dict(request_args)
        target_products = products_filter(products_model=Product, form_data=form_filter)
    else:
        form_filter = FilterProductsForm()
        target_products = Product.query

    # {'category': ['car', 'cat 1'], 'minPrice': [''], 'maxPrice': [''], 'order': ['date']}
    # Pagination
    products_pagination = target_products.paginate(page=page, per_page=1)  # app.config["ITEMS_PER_PAGE"]
    return render_template("index.html",
                           pagination=products_pagination,
                           product_filter=form_filter)


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
    return render_template('index.html', info="404 Error"), 404


@app.errorhandler(400)
def page_not_found(e):
    """Not found page"""
    return render_template('index.html', info="404 Error"), 400

@app.errorhandler(500)
def server_error(e):
    """Server error page"""
    return render_template('index.html', info="500 Server Error"), 500
