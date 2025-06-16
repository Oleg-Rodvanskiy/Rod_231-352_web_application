from app import db
from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required
from app.config import Config
from app.forms import BookForm
from faker import Faker
from app.models import User, Role, Book, Genre, Review
import random

# Инициализация приложения
app = Flask(__name__)
app.config.from_object(Config)  # Загружаем конфигурацию из класса Config

# Инициализация базы данных и менеджера входа
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # Указываем маршрут для страницы входа

# Создание экземпляра Faker
fake = Faker()

@app.route('/')
def index():
    books = Book.query.order_by(Book.year.desc()).limit(10).all()  # Получение книг
    return render_template('index.html', books=books)

@app.route('/book/<int:book_id>')
def book_detail(book_id):
    book = Book.query.get_or_404(book_id)
    return render_template('book_detail.html', book=book)

@app.route('/add_book', methods=['GET', 'POST'])
@login_required
def add_book():
    form = BookForm()
    form.genres.choices = [(genre.id, genre.name) for genre in Genre.query.all()]

    if form.validate_on_submit():
        new_book = Book(
            title=form.title.data,
            description=form.description.data,
            year=form.year.data,
            publisher=form.publisher.data,
            author=form.author.data,
            page_count=form.page_count.data
        )
        db.session.add(new_book)
        db.session.commit()

        # Привязка жанров
        for genre_id in form.genres.data:
            genre = Genre.query.get(genre_id)
            new_book.genres.append(genre)

        db.session.commit()
        flash('Book added successfully!', 'success')
        return redirect(url_for('index'))

    return render_template('book_form.html', form=form)

@app.route('/populate')
def populate_database():
    # Метод для создания фейковых данных
    with app.app_context():
        db.drop_all()
        db.create_all()
        create_roles()  # Создание ролей
        create_users()  # Создание пользователей
        create_genres()  # Создание жанров
        create_books()  # Создание книг
        create_reviews()  # Создание рецензий
    flash('Database populated with fake data!', 'success')
    return redirect(url_for('index'))

def create_roles():
    roles = [
        Role(name='Administrator', description='Full access to the system'),
        Role(name='Moderator', description='Can manage books and reviews'),
        Role(name='User', description='Can leave reviews')
    ]
    db.session.bulk_save_objects(roles)
    db.session.commit()

def create_users(num=10):
    roles = Role.query.all()
    users = [User(
        login=fake.user_name(),
        password_hash=fake.password(),
        last_name=fake.last_name(),
        first_name=fake.first_name(),
        patronymic=fake.first_name_male(),
        role_id=random.choice(roles).id
    ) for _ in range(num)]
    db.session.bulk_save_objects(users)
    db.session.commit()

def create_genres(num=5):
    genres = [Genre(name=fake.word()) for _ in range(num)]
    db.session.bulk_save_objects(genres)
    db.session.commit()

def create_books(num=20):
    all_genres = Genre.query.all()  # Загружаем все жанры один раз
    for _ in range(num):
        book = Book(
            title=fake.sentence(nb_words=4),
            description=fake.text(),
            year=fake.year(),
            publisher=fake.company(),
            author=fake.name(),
            page_count=random.randint(100, 1000)
        )
        db.session.add(book)
        selected_genres = set()  # Множество для уникальных жанров
        for _ in range(random.randint(1, 3)):
            genre = random.choice(all_genres)  # Выбираем случайный жанр
            selected_genres.add(genre)
        for genre in selected_genres:
            book.genres.append(genre)

    db.session.commit()

def create_reviews(num=30):
    users = User.query.all()
    books = Book.query.all()
    reviews = [Review(
        book_id=random.choice(books).id,
        user_id=random.choice(users).id,
        rating=random.randint(0, 5),
        text=fake.text()
    ) for _ in range(num)]
    db.session.bulk_save_objects(reviews)
    db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)
