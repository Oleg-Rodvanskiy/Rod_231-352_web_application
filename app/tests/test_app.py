import pytest
from app import app
@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_index(client):
    response = client.get('/')
    assert 'Welcome to Flask App' in response.get_data(as_text=True)


def test_url_params(client):
    response = client.get('/url-params?name=John&age=30')
    assert 'name: John' in response.get_data(as_text=True)
    assert 'age: 30' in response.get_data(as_text=True)


def test_headers(client):
    response = client.get('/headers')
    assert 'Host' in response.headers  # Проверка наличия заголовка Host
    assert 'User-Agent' in response.headers  # Проверка наличия заголовка User-Agent


def test_cookies(client):
    response = client.get('/cookies')
    assert 'Куки не установлены.' in response.get_data(as_text=True)

    response = client.post('/cookies')
    assert 'Текущее значение куки: cookie_value' in response.get_data(as_text=True)

    response = client.get('/cookies?delete=true')
    assert 'Куки не установлены.' in response.get_data(as_text=True)


def test_form_validation_invalid_length(client):
    response = client.post('/form-validation', data={'phone': '123'})
    assert 'Недопустимый ввод. Неверное количество цифр.' in response.get_data(as_text=True)


def test_form_validation_invalid_characters(client):
    response = client.post('/form-validation', data={'phone': '123abc456'})
    assert 'Недопустимый ввод. В номере телефона встречаются недопустимые символы.' in response.get_data(as_text=True)


def test_form_validation_valid_phone(client):
    response = client.post('/form-validation', data={'phone': '+7 (123) 456-75-90'})
    assert '8-123-456-75-90' in response.get_data(as_text=True)


def test_format_phone_number(client):
    response = client.post('/form-validation', data={'phone': '8(123)4567590'})
    assert '8-123-456-75-90' in response.get_data(as_text=True)


def test_phone_form_with_white_spaces(client):
    response = client.post('/form-validation', data={'phone': ' 8 ( 123 ) 456 - 75 - 90 '})
    assert '8-123-456-75-90' in response.get_data(as_text=True)


def test_invalid_country_code(client):
    response = client.post('/form-validation', data={'phone': '+1 (123) 456-75-90'})
    assert 'Недопустимый ввод. Неверное количество цифр.' in response.get_data(as_text=True)


def test_empty_phone_number(client):
    response = client.post('/form-validation', data={'phone': ''})
    assert 'Недопустимый ввод. Неверное количество цифр.' in response.get_data(as_text=True)


if __name__ == "__main__":
    pytest.main()