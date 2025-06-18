# app/views.py
from flask import render_template, request, redirect, url_for, flash
from app import app, db
from app.models import Book, Genre
from flask_login import login_required

@app.route('/', methods=['GET'])
def index():
    # Получаем параметры поиска из запроса
    title = request.args.get('title')
    genre_ids = request.args.getlist('genre')
    years = request.args.getlist('year')
    from_pages = request.args.get('from_pages', type=int)
    to_pages = request.args.get('to_pages', type=int)
    author = request.args.get('author')

    query = Book.query  # Начинаем с базового запроса

    # Фильтрация по названию (частичное соответствие)
    if title and title.strip():  # Проверяем, что title существует и не пустой
        query = query.filter(Book.title.ilike(f'%{title}%'))

    # Фильтрация по жанрам
    if genre_ids:
        query = query.join(Book.genres).filter(Genre.id.in_(genre_ids))

    # Фильтрация по годам
    if years:
        query = query.filter(Book.year.in_(years))

    # Фильтрация по объему
    if from_pages is not None:
        query = query.filter(Book.page_count >= from_pages)

    if to_pages is not None:
        query = query.filter(Book.page_count <= to_pages)

    # Фильтрация по автору (частичное соответствие)
    if author and author.strip():  # Проверяем, что author существует и не пустой
        query = query.filter(Book.author.ilike(f'%{author}%'))

    books = query.all()  # Получение отфильтрованных результатов

    # Получение жанров для выпадающего списка
    genres = Genre.query.all()

    # Получение уникальных годов для выпадающего списка, сортировка по убыванию
    years = db.session.query(Book.year).distinct().order_by(Book.year.desc()).all()
    years = [year[0] for year in years]  # Преобразование в список

    return render_template('index.html', books=books, genres=genres, years=years)