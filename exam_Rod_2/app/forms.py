from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SubmitField, SelectMultipleField, PasswordField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    login = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')

class BookForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    year = IntegerField('Year', validators=[DataRequired()])
    publisher = StringField('Publisher', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    page_count = IntegerField('Page Count', validators=[DataRequired()])
    genres = SelectMultipleField('Genres', coerce=int)
    submit = SubmitField('Save Book')