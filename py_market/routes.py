from flask import render_template, redirect, flash, request
from py_market import app, security, admin


@app.route('/')
def home():
    return render_template("body.html", title="Главная страница")


@app.route('/about')
def about_page():
    return render_template("about.html", title="О нас")