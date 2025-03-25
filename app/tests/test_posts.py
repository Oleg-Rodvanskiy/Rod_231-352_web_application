import pytest
from app import app  # Импортируем функцию для создания приложения

@pytest.fixture
def client():
    app = app()  # Создаём приложение
    app.config['TESTING'] = True  # Включаем режим тестирования
    with app.test_client() as client:
        yield client

def test_index_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert "Последние посты" in response.get_data(as_text=True)  # Проверяем наличие заголовка

def test_posts_page(client):
    response = client.get('/posts')
    assert response.status_code == 200
    assert "Посты" in response.get_data(as_text=True)  # Проверяем заголовок страницы

def test_render_post_template(client):
    response = client.get('/posts/0')
    assert response.status_code == 200
    assert '<h1>' in response.get_data(as_text=True)  # Проверяем, что рендерится HTML

def test_post_data(client):
    response = client.get('/posts/0')
    assert response.status_code == 200
    assert "Заголовок поста" in response.get_data(as_text=True)  # Проверьте наличие заголовка поста

def test_post_author(client):
    response = client.get('/posts/0')
    assert response.status_code == 200
    assert "Автор:" in response.get_data(as_text=True)  # Проверяем наличие имени автора

def test_post_date(client):
    response = client.get('/posts/0')
    assert response.status_code == 200
    assert "Дата публикации" in response.get_data(as_text=True)  # Проверяем наличие даты публикации

def test_post_content(client):
    response = client.get('/posts/0')
    assert response.status_code == 200
    assert "параграф" in response.get_data(as_text=True)  # Проверяем наличие текста поста

def test_post_image(client):
    response = client.get('/posts/0')
    assert response.status_code == 200
    assert '<img src=' in response.get_data(as_text=True)  # Проверяем, что изображение присутствует

def test_comment_form_present(client):
    response = client.get('/posts/0')
    assert response.status_code == 200
    assert "Оставьте комментарий" in response.get_data(as_text=True)  # Проверяем наличие формы комментария

def test_add_comment_response(client):
    response = client.post('/posts/0/comment', data={'comment': 'Тестовый комментарий'})
    assert response.status_code == 302  # Проверяем, что происходит редирект

def test_comment_added(client):
    client.post('/posts/0/comment', data={'comment': 'Тестовый комментарий'})
    response = client.get('/posts/0')
    assert 'Тестовый комментарий' in response.get_data(as_text=True)  # Проверяем, что комментарий отобразился

def test_nonexistent_post_404(client):
    response = client.get('/posts/999')  # Не существующий идентификатор
    assert response.status_code == 404  # Проверка кода состояния 404

def test_template_used_for_posts(client):
    response = client.get('/posts/0')
    assert response.status_code == 200
    assert response.get_data(as_text=True).count('<h1>') == 1  # Один заголовок должно быть в посте

def test_page_title_contains_post_title(client):
    response = client.get('/posts/0')
    assert "Заголовок поста" in response.get_data(as_text=True)  # Проверяем присутствие заголовка в данных страницы

def test_post_date_format(client):
    response = client.get('/posts/0')
    assert response.status_code == 200
    # Проверка корректности формата даты
    date_text = 'Дата публикации: 12.12.2021'  # Убедитесь, что формат даты совпадает
    assert date_text in response.get_data(as_text=True)

def test_posts_count_on_posts_page(client):
    response = client.get('/posts')
    assert response.status_code == 200
    # Проверка, что по крайней мере один пост отображается на странице
    assert "Заголовок поста" in response.get_data(as_text=True)

if __name__ == "__main__":
    pytest.main()