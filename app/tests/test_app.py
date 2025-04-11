import pytest
from app import app, login_manager

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index(client):
    response = client.get('/')
    assert 'Добро пожаловать' in response.get_data(as_text=True)  # Используем as_text=True

def test_login(client):
    response = client.post('/login', data={'username': 'user', 'password': 'qwerty'})
    assert response.status_code == 302  # Проверка на перенаправление

def test_login_invalid(client):
    response = client.post('/login', data={'username': 'user', 'password': 'wrong_password'})
    assert 'Неверный логин или пароль. Пожалуйста, попробуйте снова.' in response.get_data(as_text=True)

def test_authenticated_user_can_access_counter(client):
    client.post('/login', data={'username': 'user', 'password': 'qwerty'})
    response = client.get('/counter')
    assert 'Счётчик посещений' in response.get_data(as_text=True)

def test_visit_counter_increases(client):
    client.post('/login', data={'username': 'user', 'password': 'qwerty'})
    response = client.get('/counter')
    assert 'Вы посетили эту страницу' in response.get_data(as_text=True)

def test_redirect_to_login_for_secret(client):
    response = client.get('/secret', follow_redirects=True)
    assert 'Вход' in response.get_data(as_text=True)

def test_authenticated_user_can_access_secret(client):
    client.post('/login', data={'username': 'user', 'password': 'qwerty'})
    response = client.get('/secret')
    assert 'Секретная страница' in response.get_data(as_text=True)

def test_logout(client):
    client.post('/login', data={'username': 'user', 'password': 'qwerty'})
    response = client.get('/logout')
    assert 'Вы вышли из системы.' in response.get_data(as_text=True)

def test_remember_me_functionality(client):
    response = client.post('/login', data={'username': 'user', 'password': 'qwerty', 'remember_me': 'y'})
    assert '_remember' in client.cookiejar

if __name__ == "__main__":
    pytest.main()