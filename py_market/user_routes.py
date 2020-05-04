from flask import render_template, redirect, flash, request, url_for
from py_market import app, security, admin, user_datastore
from flask_security import login_required
from flask_login import LoginManager, UserMixin
# from flask_security.forms import RegisterForm
# from flask_security.templates.security import

# https://pythonhosted.org/Flask-Security/api.html
from flask_security.utils import login_user, logout_user, get_hmac, verify_password, url_for_security
from flask_security.core import current_user
from flask_security.decorators import login_required, roles_required
from py_market.market_wtf_forms import CustomRegisterForm, CustomLoginForm
from py_market.routes import home


@app.route("/register", methods=["POST", "GET"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = CustomRegisterForm(request.form)
    if form.validate_on_submit():
        flash(f"На почту {form.email.data} отправлено сообщение для подтверждения")
        return render_template("register_user.html",
                               title="Регистрация завершена",
                               to_home=True)

    warnings = False
    if form.errors:
        warnings = []
        for errors in form.errors.values():
            warnings += errors
    print(warnings)
    return render_template("register_user.html",
                           title="Регистрация",
                           form=form,
                           warnings=warnings)


@app.route("/login/", methods=["POST", "GET"])
def login_user():
    form = CustomLoginForm(request.form)
    if form.validate_on_submit():
        flash("ALL OK")
        return redirect(url_for_security("/index"))
    flash("register")
    return security.render_template('login.html', title='Войти', form=form)
