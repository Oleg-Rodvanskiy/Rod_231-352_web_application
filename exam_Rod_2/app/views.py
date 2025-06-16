from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db, login_manager
from app.models import Book, Genre, User
from app.forms import BookForm, LoginForm

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    books = Book.query.order_by(Book.year.desc()).limit(10).all()  # Пагинация может быть добавлена позже
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
        flash('Книга успешно добавлена!', 'success')
        return redirect(url_for('index'))

    return render_template('book_form.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(login=form.login.data).first()
        if user and user.check_password(form.password.data):  # Предполагается, что у вас есть метод для проверки пароля в модели User
            login_user(user)
            flash('Успешный вход!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Неправильный логин или пароль', 'danger')

    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из системы.', 'success')
    return redirect(url_for('index'))