from flask import Flask, render_template, request, jsonify, session, flash
import json
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Путь к файлу JSON для хранения отзывов
REVIEW_FILE = 'reviews.json'

# Функция для загрузки отзывов из файла
def load_reviews():
    if os.path.exists(REVIEW_FILE):
        with open(REVIEW_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

# Функция для сохранения отзывов в файл
def save_reviews(reviews):
    with open(REVIEW_FILE, 'w', encoding='utf-8') as f:
        json.dump(reviews, f, ensure_ascii=False, indent=4)

@app.route('/reviews', methods=['GET', 'POST'])
def reviews():
    if request.method == 'POST':
        # Получаем данные из формы
        username = session.get('username', 'Гость')  # Используем имя пользователя из сессии или Гость
        rating = request.form.get('rating')
        comment = request.form.get('comment')

        # Загружаем существующие отзывы
        reviews = load_reviews()

        # Создаем новый отзыв
        new_review = {
            'username': username,
            'rating': int(rating),
            'comment': comment
        }

        # Добавляем новый отзыв и сохраняем
        reviews.append(new_review)
        save_reviews(reviews)
        flash('Ваш отзыв успешно добавлен!')

        return redirect('/reviews')

    # Отображение всех отзывов
    reviews = load_reviews()
    return render_template('reviews.html', reviews=reviews)

@app.route('/view_reviews')
def view_reviews():
    reviews = load_reviews()
    return jsonify(reviews)

if __name__ == '__main__':
    app.run(debug=True)