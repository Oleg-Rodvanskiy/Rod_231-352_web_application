from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Секретный ключ для сессий
db = SQLAlchemy(app)

# Имитация модели пользователя
class User:
    def __init__(self, username, school):
        self.username = username
        self.school = school

# Mock users
users = [
    User('Geralt', 'Волк'),
    User('Vesemir', 'Волк'),
    User('Yennefer', 'Гадюка'),
    User('Triss', 'Грифон')
]

# Доступные школы
SCHOOLS = ['Волк', 'Гадюка', 'Грифон']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        school = request.form.get('school')
        # Проверка существования пользователя
        user = next((user for user in users if user.username == username), None)
        if user and user.school == school:
            session['username'] = username
            session['school'] = school
            flash(f'Вы успешно вошли как {username} из школы {school}.')
            return redirect(url_for('home'))
        else:
            flash('Некорректное имя или школа!')
    return render_template('login.html', schools=SCHOOLS)

@app.route('/home')
@login_required
def home():
    return f'Добро пожаловать, {session["username"]}! Ваш выбор: {session["school"]}.'

@app.route('/kaermorhen')
@login_required
def kaermorhen():
    if session.get('school') != 'Волк':
        flash('У вас нет доступа к этой странице.')
        return redirect(url_for('home'))
    return 'Добро пожаловать в Каэр Морхен!'

@app.route('/logout')
@login_required
def logout():
    session.pop('username', None)
    session.pop('school', None)
    flash('Вы успешно вышли из системы.')
    return redirect(url_for('index'))