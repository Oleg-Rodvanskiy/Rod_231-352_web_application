import pytest
from app import app  # Импортируем функцию для создания приложения

@pytest.fixture
def client():
    app = app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def mock_posts(mocker):
    return [
        {
            'id': 1,
            'title': 'Первый пост',
            'text': 'Текст первого поста.',
            'author': 'Автор 1',
            'date': '2023-01-01',
            'image_id': 'image1.jpg',
            'comments': [{'author': 'Комментатор 1', 'text': 'Комментарий 1'}]
        },
        {
            'id': 2,
            'title': 'Второй пост',
            'text': 'Текст второго поста.',
            'author': 'Автор 2',
            'date': '2023-01-02',
            'image_id': 'image2.jpg',
            'comments': []
        }
    ]

# Тест на правильный URL и рендеринг главной страницы
def test_index_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert "Лабораторная работа № 1" in response.get_data(as_text=True)

# Тест на правильный рендеринг страницы постов
def test_posts_page(client):
    response = client.get('/posts')
    assert response.status_code == 200
    assert "Посты" in response.get_data(as_text=True)

# Проверка на то, что используется правильный шаблон
def test_render_posts_template(client):
    response = client.get('/posts')
    assert response.status_code == 200
    assert b'posts.html' in response.data

# Проверка передачи данных о посте в шаблон
def test_post_template_data(client, mock_posts, mocker):
    mocker.patch("app.get_posts", return_value=mock_posts)
    response = client.get('/posts/1')
    assert response.status_code == 200
    assert "Первый пост" in response.get_data(as_text=True)
    assert "Автор 1" in response.get_data(as_text=True)
    assert "Текст первого поста." in response.get_data(as_text=True)
    assert "01.01.2023" in response.get_data(as_text=True)

# Проверка на правильный рендеринг даты
def test_post_date_format(client, mock_posts, mocker):
    mocker.patch("app.get_posts", return_value=mock_posts)
    response = client.get('/posts/1')
    assert response.status_code == 200
    assert "01.01.2023" in response.get_data(as_text=True)

# Проверка на наличие изображения в посте
def test_post_image_present(client, mock_posts, mocker):
    mocker.patch("app.get_posts", return_value=mock_posts)
    response = client.get('/posts/1')
    assert response.status_code == 200
    assert 'src="/static/images/image1.jpg"' in response.get_data(as_text=True)

# Проверка на наличие комментариев на странице поста
def test_comments_present(client, mock_posts, mocker):
    mocker.patch("app.get_posts", return_value=mock_posts)
    response = client.get('/posts/1')
    assert response.status_code == 200
    assert "Комментарий 1" in response.get_data(as_text=True)

# Проверка подключения формы для комментариев
def test_comment_form_present(client, mock_posts, mocker):
    mocker.patch("app.get_posts", return_value=mock_posts)
    response = client.get('/posts/1')
    assert response.status_code == 200
    assert "Оставьте комментарий" in response.get_data(as_text=True)

# Тест на отсутствие поста по несуществующему идентификатору
def test_nonexistent_post_404(client):
    response = client.get('/posts/999')
    assert response.status_code == 404

# Проверка редиректа после добавления комментария
def test_add_comment_redirect(client, mock_posts, mocker):
    mocker.patch("app.get_posts", return_value=mock_posts)
    mocker.patch("app.add_comment_to_database")
    response = client.post('/posts/1/comment', data={'comment': 'Новый комментарий'})
    assert response.status_code == 302

# Проверка добавления комментария на страницу поста
def test_comment_added(client, mock_posts, mocker):
    mocker.patch("app.get_posts", return_value=mock_posts)
    mocker.patch("app.add_comment_to_database")
    client.post('/posts/1/comment', data={'comment': 'Новый комментарий'})
    response = client.get('/posts/1')
    assert "Новый комментарий" in response.get_data(as_text=True)

# Проверка количества_post_title на странице с постами
def test_post_count_on_posts_page(client, mock_posts, mocker):
    mocker.patch("app.get_posts", return_value=mock_posts)
    response = client.get('/posts')
    assert response.status_code == 200
    assert response.get_data(as_text=True).count('Первый пост') == 1  # Проверяем, что первый пост присутствует
    assert response.get_data(as_text=True).count('Второй пост') == 1  # Проверяем, что второй пост присутствует

# Проверка корректного рендеринга страницы "Об авторе"
def test_about_page(client):
    response = client.get('/about')
    assert response.status_code == 200
    assert "Об авторе" in response.get_data(as_text=True)

# Проверка использования правильного шаблона для страницы "Об авторе"
def test_render_about_template(client):
    response = client.get('/about')
    assert response.status_code == 200
    assert b'base.html' in response.data  # Проверяем, что используется базовый шаблон

# Проверка на наличие аватара на странице "Об авторе"
def test_avatar_present_on_about_page(client):
    response = client.get('/about')
    assert response.status_code == 200
    assert 'src="/static/images/avatar.jpg"' in response.get_data(as_text=True)

# Проверка наличия обязательных текстов на странице "Об авторе"
def test_about_page_text_present(client):
    response = client.get('/about')
    assert response.status_code == 200
    assert "Lorem ipsum" in response.get_data(as_text=True)  # Проверяем наличие текста об авторе

if __name__ == "__main__":
    pytest.main()