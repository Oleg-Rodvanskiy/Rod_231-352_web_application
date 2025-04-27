import unittest
from app import app, db, User, Role
from flask import url_for


class UserManagementTestCase(unittest.TestCase):
    def setUp(self):
        # Настройка тестового приложения и базы данных
        self.app = app
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_users.db'
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()
            # Создаем роль для пользователей
            self.role = Role(name='Admin', description='Administrator role')
            db.session.add(self.role)
            db.session.commit()
            # Создаем тестового пользователя
            self.user = User(username='testuser', first_name='Иван', last_name='Иванов', middle_name='Иванович')
            self.user.set_password('StrongPassword123!')
            db.session.add(self.user)
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()

    def test_create_user(self):
        """Тестирование создания пользователя"""
        # Вход в приложение
        self.client.post('/login', data={'username': 'testuser', 'password': 'StrongPassword123!'})

        response = self.client.post('/user/create', data={
            'username': 'newuser',
            'last_name': 'Петров',
            'first_name': 'Петр',
            'middle_name': 'Петрович',
            'role_id': self.role.id,
            'password': 'NewPassword123!'
        })
        self.assertEqual(response.status_code, 302)  # Проверка перенаправления
        new_user = User.query.filter_by(username='newuser').first()
        self.assertIsNotNone(new_user, "Пользователь не был создан.")

    def test_edit_user(self):
        """Тестирование редактирования пользователя"""
        # Вход в приложение
        self.client.post('/login', data={'username': 'testuser', 'password': 'StrongPassword123!'})

        response = self.client.post(f'/user/edit/{self.user.id}', data={
            'last_name': 'Петров',
            'first_name': 'Петр',
            'middle_name': 'Петрович',
            'role_id': self.role.id
        })
        self.assertEqual(response.status_code, 302)  # Проверка перенаправления
        updated_user = User.query.get(self.user.id)
        self.assertEqual(updated_user.last_name, 'Петров', "Фамилия пользователя не была обновлена.")

    def test_delete_user(self):
        """Тестирование удаления пользователя"""
        # Вход в приложение
        self.client.post('/login', data={'username': 'testuser', 'password': 'StrongPassword123!'})

        response = self.client.post(f'/user/delete/{self.user.id}')
        self.assertEqual(response.status_code, 302)  # Проверка перенаправления
        deleted_user = User.query.get(self.user.id)
        self.assertIsNone(deleted_user, "Пользователь не был удалён.")

    def test_change_password(self):
        """Тестирование смены пароля"""
        # Вход в приложение
        self.client.post('/login', data={'username': 'testuser', 'password': 'StrongPassword123!'})

        response = self.client.post('/password_change', data={
            'old_password': 'StrongPassword123!',
            'new_password': 'NewStrongPassword123!',
            'confirm_password': 'NewStrongPassword123!'
        })
        self.assertEqual(response.status_code, 302)  # Проверка перенаправления

        # Проверка нового пароля
        user = User.query.get(self.user.id)
        self.assertTrue(user.check_password('NewStrongPassword123!'), "Пароль не был изменен правильно.")


if __name__ == '__main__':
    unittest.main()