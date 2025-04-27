from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length, EqualTo, Regexp
from models import User

class UserForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired(), Length(min=5)])
    last_name = StringField('Фамилия')
    first_name = StringField('Имя', validators=[DataRequired()])
    middle_name = StringField('Отчество')
    role_id = SelectField('Роль', coerce=int)
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=8)])

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Логин уже существует.')

class PasswordChangeForm(FlaskForm):
    old_password = PasswordField('Старый пароль', validators=[DataRequired()])
    new_password = PasswordField('Новый пароль', validators=[
        DataRequired(),
        Length(min=8, max=128),
        Regexp('^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=[^ ]+$)', message='Пароль должен содержать хотя бы одну заглавную, одну строчную букву и одну цифру.')
    ])
    confirm_password = PasswordField('Повторите новый пароль', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Сменить пароль')