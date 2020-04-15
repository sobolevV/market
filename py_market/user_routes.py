from flask import render_template, redirect, flash, request, url_for
from py_market import app, security, admin
from flask_security import login_required
from flask_security.forms import RegisterForm
from flask_security.templates.security import *
# https://pythonhosted.org/Flask-Security/api.html
from flask_security.utils import login_user, logout_user, hash_password


# @app.route("/register")
# def register(method=("POST", "GET")):
#     if request.method == "POST":
#         return "wait"
#
#     return render_template("register_user.html")