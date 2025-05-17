from flask import Flask, render_template, redirect, url_for, request, session, flash, jsonify
import csv
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Секретный ключ для сессий

# Имитация модели пользователя
class User:
    def __init__(self, username, school, rank):
        self.username = username
        self.school = school
        self.rank = rank

# Mock users
users = [
    User('Geralt', 'Волк', 'Master'),
    User('Vesemir', 'Волк', 'Master'),
    User('Yennefer', 'Гадюка', 'Novice'),
    User('Triss', 'Грифон', 'Novice')
]

@app.route('/contracts')
def contracts():
    # Проверка прав доступа для пользователя
    if session.get('rank') != 'Master':
        flash('У вас нет доступа к этому маршруту.')
        return redirect(url_for('home'))
    
    # Здесь может быть логика для отображения контрактов
    return 'Список контрактов доступен.'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        school = request.form.get('school')
        # Проверка существования пользователя
        user = next((user for user in users if user.username == username), None)
        if user:
            session['username'] = username
            session['school'] = user.school
            session['rank'] = user.rank
            flash(f'Вы успешно вошли как {username} из школы {user.school}.')
            return redirect(url_for('home'))
        else:
            flash('Пользователь не найден!')
    return render_template('login.html')

@app.route('/home')
def home():
    return 'Добро пожаловать на главную страницу!'

if __name__ == '__main__':
    app.run(debug=True)