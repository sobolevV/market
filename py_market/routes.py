from flask import render_template, redirect, flash, request, url_for
from py_market import app, security, admin
from flask_login.utils import login_required, login_user
from flask_security.core import current_user


@app.route('/')
def home():
    try:
        user = current_user
        print(current_user)
    except Exception as e:
        print(e)
    return render_template("index.html", title="Главная страница", user=current_user)


@app.route('/about')
def about():
    return render_template("about.html", title="О нас")


@app.route('/cart')
@login_required
def cart():
    pass


@app.route('/profile')
@login_required
def profile():
    pass

# Handle errors
@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('index.html', info="404 Error"), 404

