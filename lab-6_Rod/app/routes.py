from flask import Blueprint, render_template, send_from_directory, current_app, abort, request, flash, redirect, url_for
from flask_login import login_required, current_user
from app.repositories import CategoryRepository, ImageRepository, CourseRepository  # Импортируем CourseRepository также
from app.models import db, Review

# Инициализация репозиториев
category_repository = CategoryRepository(db)
image_repository = ImageRepository(db)
course_repository = CourseRepository(db)  # Добавление CourseRepository

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    categories = category_repository.get_all_categories()
    return render_template('index.html', categories=categories)

@bp.route('/images/<image_id>')
def image(image_id):
    img = image_repository.get_by_id(image_id)
    if img is None:  # Исправлено на img вместо image
        abort(404)
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], img.storage_filename)

@bp.route('/<int:course_id>/review', methods=['POST'])
@login_required
def add_review(course_id):
    course = course_repository.get_course_by_id(course_id)
    if course is None:
        abort(404)

    rating = request.form.get('rating', type=int)
    text = request.form.get('text')

    # Проверка на существующий отзыв
    existing_review = Review.query.filter_by(course_id=course_id, user_id=current_user.id).first()

    if existing_review:
        existing_review.rating = rating
        existing_review.text = text
    else:
        existing_review = Review(rating=rating, text=text, course_id=course_id, user_id=current_user.id)
        db.session.add(existing_review)

    # Обновление рейтинга курса
    if existing_review:
        # Корректировка суммы рейтинга
        course.rating_sum += rating - existing_review.rating
    else:
        course.rating_sum += rating  # Добавляем новую оценку

    # Обновляем количество отзывов
    course.rating_num = len(course.reviews)
    db.session.commit()

    flash("Ваш отзыв был успешно сохранен!", "success")
    return redirect(url_for('courses.show', course_id=course_id))