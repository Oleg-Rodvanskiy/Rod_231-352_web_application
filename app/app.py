from flask import Flask, request, render_template, redirect, url_for, flash, make_response
import re

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Необходимо для работы flash-сообщений


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/url-params')
def url_params():
    return render_template('url_params.html', params=request.args)


@app.route('/headers')
def headers():
    return render_template('headers.html', headers=request.headers)


@app.route('/cookies', methods=['GET', 'POST'])
def cookies():
    if request.method == 'POST':
        resp = make_response(redirect(url_for('cookies')))
        resp.set_cookie('my_cookie', 'cookie_value')
        return resp

    # Проверка на удаление куки
    if 'delete' in request.args:
        resp = make_response(redirect(url_for('cookies')))
        resp.delete_cookie('my_cookie')
        return resp

    return render_template('cookies.html', cookie_value=request.cookies.get('my_cookie'))


@app.route('/form-validation', methods=['GET', 'POST'])
def form_validation():
    if request.method == 'POST':
        phone = request.form.get('phone')
        error = None

        # Удаляем все символы, кроме представленных
        cleaned_phone = re.sub(r'[^\d()\+\-.\s]', '', phone)

        # Проверка критериев
        if cleaned_phone.startswith('+7') or cleaned_phone.startswith('8'):
            if len(cleaned_phone) != 11:
                error = 'Недопустимый ввод. Неверное количество цифр.'
        else:
            if len(cleaned_phone) != 10:
                error = 'Недопустимый ввод. Неверное количество цифр.'

        if not error and not re.match(r'^[\d\s().+-]+$', phone):
            error = 'Недопустимый ввод. В номере телефона встречаются недопустимые символы.'

        if error:
            flash(error, 'danger')
            return render_template('form_validation.html', phone=phone, error=error)

        # Форматируем номер
        formatted_phone = format_phone_number(cleaned_phone)
        return render_template('form_validation.html', phone=formatted_phone)

    return render_template('form_validation.html')


def format_phone_number(phone):
    """ Форматирует номер телефона в формат 8-***-***-**-** """
    if phone.startswith('+7'):
        phone = phone[2:]  # Убираем +7
    elif phone.startswith('8'):
        phone = phone[1:]  # Убираем 8

    # Преобразуем в формат 8-***-***-**-**
    formatted = f"8-{phone[:3]}-{phone[3:6]}-{phone[6:8]}-{phone[8:]}"
    return formatted


if __name__ == '__main__':
    app.run(debug=True)