from flask import Flask, render_template, redirect

app = Flask(__name__)


@app.route('/')
def home():
    return render_template("body.html", title="Главная страница")


@app.route('/about')
def about_page():
    return render_template("about.html", title="О нас")


if __name__ == '__main__':
    app.run(debug=True)
