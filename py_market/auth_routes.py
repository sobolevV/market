from py_market import app, security, admin, user_datastore, db, mail, g, flash, User

from flask import Flask, url_for, redirect, request, render_template, abort
from flask_security.decorators import login_required, roles_required
from flask_security.core import current_user
from flask_login import login_user, logout_user

from py_market.forms import CustomRegisterForm, CustomLoginForm
from py_market.routes import home

from flask_mail import Message
from flask_security.utils import login_user, logout_user, hash_password
from itsdangerous.url_safe import URLSafeTimedSerializer
from itsdangerous.exc import BadSignature, SignatureExpired
from datetime import datetime

signer = URLSafeTimedSerializer(secret_key=app.config.get("SECRET_KEY"))


def collect_warnings(form_errors) -> list:
    """Collect all warning in form and return
        :returns list of strings"""
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
            # print(sign)
            # external - link with hostname
            confirm_link = url_for("activate_user", token=sign, _external=True)
            # Send message to Email and info to user
            flash(f"На почту {form.email.data} отправлено сообщение для подтверждения", category="message")
            msg = Message("Подтверждение регистрации",
                          recipients=[user.email],
                          html=render_template("mail.html", username=user.name,
                                               name="TestName",
                                               link=confirm_link))
            mail.send(msg)

            return redirect(url_for("login"))

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
    warnings = None
    if request.method == "POST":
        if form.validate_on_submit():
            user = User.get_user_by_email(form.email.data)
            # If user confirmed email
            if user.is_auth:
                flash("Вы успешно вошли", category="message")
                login_user(user, form.remember_me.data)
                # set user to global variable
                return redirect(url_for("home"))
        # else not valid user form
        if form.errors:
            flash("У вас ошибки", "warning")
            warnings = collect_warnings(form.errors)
    return security.render_template('login.html', title='Войти', form=form, warnings=warnings)


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
        # set user to global variable
        g.user = current_user
        return redirect(home)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    del g.user
    return redirect('home')
