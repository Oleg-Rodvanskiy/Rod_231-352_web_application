from datetime import datetime
import pytest
from flask import template_rendered
from contextlib import contextmanager
from app import app as application

@pytest.fixture
def app():
    return application

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
@contextmanager
def captured_templates(app):
    recorded = []
    def record(sender, template, context, **extra):
        recorded.append((template, context))
    template_rendered.connect(record, app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, app)

@pytest.fixture
def posts_list():
    return [
        {
            'title': 'Заголовок поста',
            'text': 'Текст поста',
            'author': 'Иванов Иван Иванович',
            'date': datetime(2025, 3, 10),
            'image_id': '123.jpg',
            'comments': []
        }
    ]

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