from flask import render_template, redirect, flash, request, url_for
from py_market import app, security, admin


@app.route('/')
def home():
    return render_template("base.html", title="Главная страница")


@app.route('/about')
def about():
    return render_template("about.html", title="О нас")