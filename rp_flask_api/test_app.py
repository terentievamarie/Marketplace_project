import unittest
from app import app, db, User


class FlaskAppTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_signup(self):
        response = self.app.post('/signup', json={'username': 'test_user', 'password': 'test_password'})
        self.assertEqual(response.status_code, 201)

    def test_login(self):
        # Зарегистрируем пользователя перед входом
        self.app.post('/signup', json={'username': 'test_user', 'password': 'test_password'})
        
        # Попытаемся войти с правильными учетными данными
        response = self.app.post('/login', json={'username': 'test_user', 'password': 'test_password'})
        self.assertEqual(response.status_code, 200)

        # Попытаемся войти с неправильными учетными данными
        response = self.app.post('/login', json={'username': 'test_user', 'password': 'wrong_password'})
        self.assertEqual(response.status_code, 401)

    def test_get_users(self):
        # Зарегистрируем пользователя перед запросом списка пользователей
        self.app.post('/signup', json={'username': 'test_user', 'password': 'test_password'})
        
        # Получим список пользователей
        response = self.app.get('/api/users')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data['users']), 1)


if __name__ == '__main__':
    unittest.main()
