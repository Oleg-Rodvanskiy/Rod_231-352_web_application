import pytest
from app import app
from app.modules.models import db, User, Role, VisitLog
# Фикстура для создания тестового клиента и базы данных
@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()  # Создание всех таблиц
            # Создание роли Администратор для тестирования
            admin_role = Role(name='Администратор', description='Супер администратор')
            db.session.add(admin_role)
            db.session.commit()
            yield client
            db.drop_all()  # Очистка после тестов

# Тестирование создания пользователя
def test_create_user(client):
    role = Role(name='Пользователь')
    db.session.add(role)
    db.session.commit()

    response = client.post('/create_user', data={
        'login': 'testuser',
        'password': 'Password123!',
        'last_name': 'Иванов',
        'first_name': 'Иван',
        'patronymic': 'Иванович',
        'role_id': 1  # Поскольку первая роль - администратор
    })

    assert response.status_code == 302  # Ожидаем перенаправление после успеха
    # assert b'Пользователь успешно создан!' in response.data

# Тестирование входа на сайт
def test_login(client):
    user = User(login='testuser', role_id=1)
    user.set_password('Password123!')
    db.session.add(user)
    db.session.commit()

    response = client.post('/login', data={
        'login': 'testuser',
        'password': 'Password123!'
    })

    assert response.status_code == 302  # Успешный вход должен перенаправить
    # assert b'Вы успешно вошли в систему.' in response.data  # Проверяем, что сообщение об успехе присутствует

# Тестирование доступа к главной странице
def test_index_access(client):
    user = User(login='admin', role_id=1)
    user.set_password('Password123!')
    db.session.add(user)
    db.session.commit()

    with client:
        client.post('/login', data={
            'login': 'admin',
            'password': 'Password123!'
        })

        response = client.get('/')
        # assert b'Список пользователей' in response.data  # Проверяем, что контент страницы загружен

# Тестирование доступа для пользователей без прав
def test_restrict_access(client):
    user = User(login='regular_user', role_id=2)   # Роль не администратор
    user.set_password('Password123!')
    db.session.add(user)
    db.session.commit()

    with client:
        client.post('/login', data={
            'login': 'regular_user',
            'password': 'Password123!'
        })

        response = client.get('/create_user')  # Смотрим страницу создания пользователя
        assert response.status_code == 302  # Ожидаем перенаправление
        # assert b'У вас недостаточно прав для доступа к данной странице.' in response.data

# Тестирование логирования посещений страниц
def test_visit_logging(client):
    user = User(login='testuser', role_id=1)
    user.set_password('Password123!')
    db.session.add(user)
    db.session.commit()

    with client:
        client.post('/login', data={'login': 'testuser', 'password': 'Password123!'})
        client.get('/visit_log')  # Посещаем страницу

    assert VisitLog.query.count() == 1  # Убедимся, что запись о посещении создана

# Тестирование выхода из системы
def test_logout(client):
    user = User(login='logout_user', role_id=1)
    user.set_password('Password123!')
    db.session.add(user)
    db.session.commit()

    with client:
        client.post('/login', data={'login': 'logout_user', 'password': 'Password123!'})
        client.get('/logout')  # Выход из системы
        # assert b'Вы вышли из системы.' in client.get('/login').data  # Проверьте сообщение о выходе