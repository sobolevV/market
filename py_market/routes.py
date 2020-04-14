from flask import render_template, redirect, flash
from py_market import app
from flask_admin import Admin

admin = Admin(app)


@app.route('/')
def home():
    return render_template("body.html", title="Главная страница")


@app.route('/about')
def about_page():
    return render_template("about.html", title="О нас")