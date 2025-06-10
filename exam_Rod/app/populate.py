from app import app, db
from app.models import User, Role, Book, Genre, Review
from faker import Faker
import random

fake = Faker()

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
    books = []
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
        db.session.flush()  # gets the id for the book
        # Randomly assign genres
        for _ in range(random.randint(1, 3)):
            genre = Genre.query.order_by(db.func.random()).first()  # Random genre
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
    with app.app_context():
        db.drop_all()
        db.create_all()
        create_roles()          # Создание ролей
        create_users()         # Создание пользователей
        create_genres()        # Создание жанров
        create_books()         # Создание книг
        create_reviews()       # Создание рецензий