from py_market import app, db, mail, g, flash, security, user_datastore
from py_market.models import User
from py_market.forms import CustomRegisterForm, CustomLoginForm

from flask import Blueprint, url_for, redirect, request, render_template, abort

from flask_security.decorators import login_required, roles_required
from flask_security.utils import login_user, logout_user, hash_password
from flask_security.core import current_user
from flask_login import login_user, logout_user

from flask_mail import Message

from itsdangerous.url_safe import URLSafeTimedSerializer
from itsdangerous.exc import BadSignature, SignatureExpired
from jinja2 import Markup
from datetime import datetime

confirm_time = 3  # hours
invalid_token_markup = Markup(f"""<h3>Время для подтверждения истекло</h3><br>
                                  Проведите повторную регистрацию для подтверждения""")
signer = URLSafeTimedSerializer(secret_key=app.config.get("SECRET_KEY"))

bp_auth = Blueprint('auth', __name__, url_prefix='/auth', template_folder="templates")


# !!!! Переделать - убрать тут и добавить в html
def collect_warnings(form_errors) -> list:
    """Collect all warning in form and return
        :returns list of strings"""
    warnings = []
    for errors in form_errors.values():
        warnings += errors
    return warnings


@bp_auth.route("/register", methods=["POST", "GET"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    warnings = False  # warnings from validation
    form = CustomRegisterForm(request.form)
    if request.method == "POST":
        if form.validate_on_submit():
            # Success register
            user = User(name=form.name.data, password=hash_password(form.password.data), email=form.email.data)
            role = user_datastore.find_role(app.config["USER_ROLE"])
            # Set default role to user
            user_datastore.add_role_to_user(user, role)
            db.session.add(user)
            user_datastore.commit()
            sign = signer.dumps({"id": user.id, "email": user.email})
            # external - link with hostname
            confirm_link = url_for("activate_user", token=sign, _external=True)
            # Send message to Email and info to user
            flash(f"На почту {form.email.data} отправлено сообщение для подтверждения", category="message")
            msg = Message("Подтверждение регистрации",
                          recipients=[user.email],
                          html=render_template("auth/mail.html",
                                               username=user.name,
                                               name="TestName",
                                               link=confirm_link,
                                               confirm_time=confirm_time))
            mail.send(msg)
            return redirect(url_for("login"))

        # else not valid user form
        if form.errors:
            warnings = collect_warnings(form.errors)

    return render_template("auth/register_user.html",
                           title="Регистрация",
                           form=form,
                           warnings=warnings)


@bp_auth.route("/login", methods=["POST", "GET"])
def login():
    form = CustomLoginForm(request.form)
    warnings = None
    if request.method == "POST":
        if form.validate_on_submit():
            user = user_datastore.find_user(email=form.email.data)
            # If user confirmed email
            if user.is_auth:
                login_user(user, form.remember_me.data)
                flash("Вы успешно вошли", category="message")
                # set user to global variable
                return redirect(url_for("home"))
        # else not valid user form
        if form.errors:
            # flash("У вас ошибки", "warning")
            warnings = collect_warnings(form.errors)
    return render_template('auth/login.html', title='Войти', form=form, warnings=warnings)


@bp_auth.route("/user_confirm/<string:token>")
def activate_user(token):

    try:
        data = signer.loads(token, max_age=confirm_time*60*60)
    except (Exception, BadSignature, SignatureExpired) as ex:
        print(ex)
        # again try load data
        data = signer.loads(token)
        try:
            # get user from DB
            tmp_user = User.query.get_or_404(data["id"])
            db.session.delete(tmp_user)
            db.session.commit()
        except Exception as e:
            print(e)
        # Invalid token data
        return render_template("py_market/base.html", info=invalid_token_markup)

    # Valid token
    token_user_id, token_user_email = data["id"], data["email"]
    # user = User.query.get_or_404(token_user_id)
    user = user_datastore.find_user(id=token_user_id, email=token_user_email)

    if user is not None:
        # User confirmed email
        # user.auth_user()
        user_datastore.activate_user(user)
        login_user(user)
        return redirect('home')
    return render_template("py_market/base.html", info="Sorry. Bad user token id")


@bp_auth.route("/logout")
@login_required
def logout():
    # Delete user data from session
    logout_user()
    # Delete from context
    del g.user
    return redirect('home')
