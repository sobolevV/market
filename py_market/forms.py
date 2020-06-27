from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, BooleanField, SelectMultipleField, SelectField
from wtforms.validators import Required, Regexp, EqualTo, InputRequired, Length, Optional, Email, ValidationError, \
    StopValidation, NumberRange
from wtforms.widgets import CheckboxInput, ListWidget, RadioInput
from wtforms.widgets.html5 import NumberInput
from flask_security.utils import verify_password
from py_market.models import User, Category, Material
import inspect

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


class CustomLoginForm(FlaskForm):
    """Login form"""
    email = CustomRegisterForm.email
    password = PasswordField("Пароль *", validators=[InputRequired()])
    remember_me = BooleanField("Запомнить меня", default=False)
    submit = SubmitField("Войти")

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


class SelectRadioField(SelectField):
    widget = ListWidget(prefix_label=False)
    option_widget = RadioInput()

    def __len__(self):
        return len(self.choices)


class FilterProductsForm(FlaskForm):
    """Filtration for products"""
    # def __init__(self, *args, **kwargs):
    #     super().__init__(self, **kwargs)
    #     keys = self.keys()

    category = MultiCheckboxField("Категория", _prefix="category[]",
                                   choices=[(cat.name, cat.name) for cat in Category.query.order_by('name').all()],)
    material = MultiCheckboxField("Материал",
                                   choices=[(mat.name, mat.name) for mat in Material.query.order_by('name').all()])

    minPrice = IntegerField(label="От", widget=NumberInput(step=1, min=0, max=100000))
    maxPrice = IntegerField(label="До", widget=NumberInput(step=1, min=0, max=100000))

    order = SelectRadioField("Сортировать по", choices=[("date", "По новинкам"),
                                                        ("price", "По возрастанию цены"),
                                                        ("price_desc", "По убыванию цены")], default="date")

    # submit = SubmitField("Применить")

    def from_dict(self, dict_obj):
        if "csrf_token" in dict_obj:
            del dict_obj["csrf_token"]

        for key, val in dict_obj.items():
            if key in self.data:
                try:
                    attr = getattr(self, key)
                    if isinstance(val, (str, list)) and len(val) == 0:
                        attr.data = None
                    elif isinstance(val, list) and len(val) == 1:
                        if len(val[0]):
                            attr.data = val[0]
                        else:
                            attr.data = None
                    else:
                        attr.data = val
                except Exception as e:
                    print(e)
        return self

    def getlist(self, key):
        if isinstance(self[key].data, list):
            return self[key].data
        return [self[key].data]

    @classmethod
    def items(cls):
        return dict(inspect.getmembers(cls, lambda atr: not inspect.isroutine(atr)))

    @classmethod
    def keys(cls):
        return set(cls.items().keys())

    def __getitem__(self, item):
        try:
            return getattr(self, item).data
        except KeyError() as ex:
            print(ex)
            return None



