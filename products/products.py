from flask import g, flash, url_for, redirect, request, render_template, abort, session, send_from_directory, Blueprint, \
    Response
from sqlalchemy import desc
from flask_security import current_user
from py_market.forms import FilterProductsForm
from py_market.models import *
from py_market import app

bp_prods = Blueprint("products", import_name=__name__,
                     url_prefix="/products",
                     template_folder="templates",
                     static_folder='static')


def products_filter(products_model, form_data):
    filtered_products = products_model.query
    filter_tables = {"category", "material"}

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
@bp_prods.route('/', methods=["POST", "GET"])
def base():
    """Page with filtered products"""
    page = 1
    # Get arguments for filtering
    request_args = request.args.to_dict(flat=False)
    if "page" in request_args:
        page = int(request_args["page"][0])
        del request_args["page"]

    if len(request_args):
        form_filter = FilterProductsForm().from_dict(request_args)
        target_products = products_filter(products_model=Product, form_data=form_filter)
    else:
        form_filter = FilterProductsForm()
        target_products = Product.query

    # {'category': ['car', 'cat 1'], 'minPrice': [''], 'maxPrice': [''], 'order': ['date']}
    # Pagination
    products_pagination = target_products.paginate(page=page, per_page=app.config["ITEMS_PER_PAGE"])
    return render_template("products/products_base.html",
                           pagination=products_pagination,
                           product_filter=form_filter)


@bp_prods.route('/target=<int:id>')
def product_page(id):
    """Page with Product description"""
    target_product = Product.query.filter(Product.id == id).first_or_404()
    return render_template("products/product_page.html", product=target_product)


@bp_prods.route('/add_to_cart', methods=("POST", ))
def add_to_cart():
    """Adding product to cart by id"""
    dict_form = request.form.to_dict()
    if "product_id" not in dict_form:
        flash("Невозможно добавить товар в корзину. Данные о товаре указаны неверно или не сущуствуют",
              category="warning")
        return Response(status=400)

    new_cart_add = Cart(user_id=current_user.id, product_id=int(dict_form["product_id"]))
    db.session.add(new_cart_add)
    db.session.commit()
    return Response(status=200)


# Global user
@bp_prods.before_request
def before_request():
    if current_user:
        g.user = current_user