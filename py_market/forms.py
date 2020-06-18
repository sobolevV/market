from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, BooleanField, SelectMultipleField, FieldList
from wtforms.validators import Required, Regexp, EqualTo, InputRequired, Length, Optional, Email, ValidationError, \
    StopValidation, NumberRange
from wtforms.widgets import CheckboxInput, ListWidget
from wtforms.widgets.html5 import NumberInput
from flask_security.utils import verify_password
from py_market import User, Category, Material

password_len = 6


class CustomRegisterForm(FlaskForm):
    """Registration form"""
    name = StringField("Имя Фамилия *", validators=[InputRequired(),
                                                    Length(min=1, max=200,
                                                    message="Минимальная длина имени 1 символ"),
                                                    Regexp(r"^[а-яА-Яa-z-A-Z]+\s?[а-яА-Яa-z-A-Z]*",
                                                           message="Поле с именем не должно \
                                                    содержать цифры или символы")])
    email = StringField("Email *", validators=[InputRequired(),
                                               Email(message="Электронная почта не соответствует требованиям."),
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

    # @staticmethod
    # def validate_email(email_field):
    #     if User.query.filter_by(email=email_field.data).first():
    #         raise ValidationError(message="Пользователь с таким Email уже существует")


class CustomLoginForm(FlaskForm):
    """Login form"""
    email = CustomRegisterForm.email
    password = PasswordField("Пароль *", validators=[InputRequired()])
    remember_me = BooleanField("Запомнить меня", default=False)
    submit = SubmitField("Войти")

    # @staticmethod
    # def validate_email(email_field):
    #     user = User.query.filter_by(email=email_field.data).first()
    #     if user is None:
    #         raise ValidationError()
    #     if not user.is_auth:
    #         raise ValidationError("Пользователь еще не подтвердил свой почтовый адрес")

    def validate_password(self, password_field):
        user = User.query.filter_by(email=self.email.data).first()
        if user is None:
            raise ValidationError()
        if not verify_password(password_field.data, user.password):
            raise ValidationError("Неверный пароль")


class ChangePassword(FlaskForm):
    """Change password form"""
    # must validate password in db
    password = PasswordField('Новый пароль', validators=[InputRequired()])
    confirm = PasswordField('Повторите пароль', validators=[EqualTo("password", message='Passwords must match')])
    submit = SubmitField("Подтвердить")


class MultiCheckboxField(SelectMultipleField):
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()

    def __len__(self):
        return len(self.choices)


class FilterProductsForm(FlaskForm):
    """Filtration for products"""
    category = MultiCheckboxField("Категория",
                                   choices=[(cat.name, cat.name) for cat in Category.query.order_by('name').all()])
    material = MultiCheckboxField("Материал",
                                   choices=[(mat.name, mat.name) for mat in Material.query.order_by('name').all()])
    #
    minPrice = IntegerField(label="От", widget=NumberInput(step=1, min=0, max=100000))
    maxPrice = IntegerField(label="До", widget=NumberInput(step=1, min=0, max=100000))
    submit = SubmitField("Применить", )


