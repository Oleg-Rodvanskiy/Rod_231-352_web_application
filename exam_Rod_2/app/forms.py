from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, FileField, SelectMultipleField, PasswordField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    login = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')

class BookForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    author = StringField('Автор', validators=[DataRequired()])
    year = IntegerField('Год', validators=[DataRequired()])
    publisher = StringField('Издатель', validators=[DataRequired()])
    page_count = IntegerField('Количество страниц', validators=[DataRequired()])
    cover = FileField('Обложка')  # Поле для загрузки обложки
    genres = SelectMultipleField('Жанры', coerce=int)
    submit = SubmitField('Сохранить')