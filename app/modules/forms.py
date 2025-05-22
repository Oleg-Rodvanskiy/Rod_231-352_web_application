from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length, EqualTo
import re

class UserForm(FlaskForm):
    login = StringField('Логин', validators=[DataRequired(), Length(min=5)])
    password = PasswordField('Пароль', validators=[DataRequired()])
    last_name = StringField('Фамилия')
    first_name = StringField('Имя', validators=[DataRequired()])
    patronymic = StringField('Отчество')
    role_id = SelectField('Роль', coerce=int)  # обычно заполняется из БД
    submit = SubmitField('Сохранить')

    @staticmethod
    def validate_password(password):
        password = password.data
        if not re.match(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)[A-Za-z\d~!?@#$%^&*()_\-+=\[\]{}<>\/|":;\',\.]{8,128}$', password):
            raise ValidationError('Пароль должен содержать не менее 8 символов, как минимум одну заглавную букву и одну цифру, без пробелов.')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Старый пароль', validators=[DataRequired()])
    new_password = PasswordField('Новый пароль', validators=[DataRequired()])
    confirm_password = PasswordField('Повторите новый пароль', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Изменить пароль')