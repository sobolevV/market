from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Required, Regexp, EqualTo, InputRequired, Length, Optional

messages = {
    "register": {
        "email": "Электронная почта указана неверно.",
        "password": "Пароль не соответствует требованиям.",
        "confirm_password": "Пароли не совпадают.",
    },

    "login": {
        "password": ""
    }
}


class RegisterForm(FlaskForm):
    name = StringField("Имя Фамилия")
    password = PasswordField("Пароль")
    confirm_password = PasswordField("Подтвердите пароль")
    submit = SubmitField()


class ChangePassword(FlaskForm):
    password = PasswordField('New Password', [InputRequired(), EqualTo('confirm', message='Passwords must match')])
    confirm  = PasswordField('Repeat Password')