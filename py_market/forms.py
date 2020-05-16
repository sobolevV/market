from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField, BooleanField
from wtforms.validators import Required, Regexp, EqualTo, InputRequired, Length, Optional, Email, ValidationError
from flask_security.utils import verify_password
from py_market import User


password_len = 6
messages = {
    "register": {
        "email": "Электронная почта не соответствует требованиям.",
        "password": "Пароль не соответствует требованиям.",
        "confirm_password": "Пароли не совпадают.",
    },

    "login": {
        "password": ""
    }
}


class CustomRegisterForm(FlaskForm):
    name = StringField("Имя Фамилия *", validators=[InputRequired(),
                                                    Length(min=1, max=200,
                                                    message="Минимальная длина имени 1 символ"),
                                                    Regexp(r"^[а-яА-Яa-z-A-Z]+\s?[а-яА-Яa-z-A-Z]*",
                                                           message="Поле с именем не должно \
                                                    содержать цифры или символы")])
    email = StringField("Email *", validators=[InputRequired(),
                                               Email(message=messages['register']['email']),
                                               Length(min=5, max=200,
                                                      message="Минимальная длина адреса 5 символов, \
                                                               максимальная длина 200 символов")])
    password = PasswordField("Пароль *", validators=[InputRequired(),
                                                     Length(min=password_len,
                                                     message=f"Минимальная длина пароля {password_len} символов."),
                                                     Regexp(regex=r"(?=.*[0-9])",
                                                     message="Пароль должен содержать минимум 1 цифру.")])
    confirm_password = PasswordField("Подтвердите пароль *", validators=[EqualTo('password',
                                                                                 message="Пароли не совпадают.")])
    # sex = RadioField("Пол", choices=[("male", "Мужской"), ("female", "Женский")], validators=[Optional()])
    submit = SubmitField("Регистрация")

    def validate_email(self, email_field):
        if User.query.filter_by(email=email_field.data).first():
            raise ValidationError(message="Пользователь с таким email уже существует")


class CustomLoginForm(FlaskForm):
    email = CustomRegisterForm.email
    password = CustomRegisterForm.password
    remember_me = BooleanField("Запомнить меня", default=False)
    submit = SubmitField("Войти")

    def validate_password(self, password_field):
        user = User.query.filter_by(email=self.email.data).first()
        if not verify_password(password_field.data, user.password):
            raise ValidationError("Неверный пароль")


class ChangePassword(FlaskForm):
    password = PasswordField('Новый пароль', validators=[InputRequired()])
    confirm = PasswordField('Повторите пароль', validators=[EqualTo("password", message='Passwords must match')])
    submit = SubmitField("Подтвердить")