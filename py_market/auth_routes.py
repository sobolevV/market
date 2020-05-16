from flask import render_template, redirect, flash, request, url_for, abort
from py_market import app, security, admin, user_datastore, db, mail
from flask_security import login_required
# from flask_login import LoginManager, UserMixin
from flask_mail import Message
from flask_security.utils import login_user, logout_user, hash_password, url_for_security

from flask_security.decorators import login_required, roles_required
from py_market.forms import CustomRegisterForm, CustomLoginForm
from py_market.routes import *

from itsdangerous.url_safe import URLSafeTimedSerializer
from itsdangerous.exc import BadSignature, SignatureExpired
from .models import User
from datetime import datetime

signer = URLSafeTimedSerializer(secret_key=app.config.get("SECRET_KEY"))


def collect_warnings(form_errors) -> list:
    warnings = []
    for errors in form_errors.values():
        warnings += errors
    return warnings


@app.route("/register", methods=["POST", "GET"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    warnings = False  # warnings from validation

    form = CustomRegisterForm(request.form)
    if request.method == "POST":

        if form.validate_on_submit():
            # Success register
            user = user_datastore.create_user(name=form.name.data,
                                              password=hash_password(form.password.data),
                                              email=form.email.data)
            db.session.commit()
            sign = signer.dumps({"id": user.id, "email": user.email})
            print(sign)
            confirm_link = url_for("activate_user", token=sign)
            # Send message to Email and info to user
            flash(f"На почту {form.email.data} отправлено сообщение для подтверждения", category="message")
            msg = Message("Подтверждение регистрации",
                          recipients=[user.email],
                          html=render_template("mail.html", username=user.name,
                                               name="TestName",
                                               link=confirm_link))
            mail.send(msg)

            return redirect(url_for("login_user"))

        # else not valid user form
        if form.errors:
            warnings = collect_warnings(form.errors)

    return security.render_template("register_user.html",
                                    title="Регистрация",
                                    form=form,
                                    warnings=warnings)


@app.route("/login/", methods=["POST", "GET"])
def login():
    form = CustomLoginForm(request.form)
    if request.method == "POST":
        if form.validate_on_submit():
            user = User.get_user_by_email(form.email.data)
            # If user confirmed email
            if user.is_auth:
                flash("Вы успешно вошли", category="message")
                login_user(user, form.remember_me.data)
                return redirect(url_for("home"))
            elif user.is_auth is False:
                flash(f"Подтвердите вашу почту {form.email.data}", category='warning')
            else:
                flash(f"Пользователя с указанным Email адресом не существует", category='warning')
    return security.render_template('login.html', title='Войти', form=form)


@app.route("/user_confirm/<string:token>")
def activate_user(token):
    # data = None
    try:
        data = signer.loads(token)
    except Exception as ex:
        print(ex)
        return abort(404)

    token_user_id, token_user_email = data["id"], data["email"]
    user = User.query.get_or_404(token_user_id)
    if user.email == token_user_email:
        # User confirmed email
        user.auth_user()
        login_user(user)

        return redirect(home)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(home)
