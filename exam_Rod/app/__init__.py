from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from app.config import Config  # Импортируем класс конфигурации

# Инициализация приложения
app = Flask(__name__)
app.config.from_object(Config)  # Загружаем конфигурацию из класса Config

# Инициализация базы данных
db = SQLAlchemy(app)

# Инициализация менеджера входа
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # Указываем маршрут для страницы входа

# Импортируем views после создания приложения для избежания проблемы с логикой импорта
from app import views