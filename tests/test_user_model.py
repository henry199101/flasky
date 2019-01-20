from tests.base import BasicTestCase
from app import create_app, db
from app.models import User


class UserModelTestCase(BasicTestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_1_password_setter(self):
        u = User(password='cat')
        self.assertIsNotNone(u.password_hash)

    def test_2_no_password_getter(self):
        u = User(password='cat')
        with self.assertRaises(AttributeError):
            u.password

    def test_3_right_password(self):
        u = User(password='cat')
        self.assertTrue(u.verify_password('cat'))

    def test_4_wrong_password(self):
        u = User(password='cat')
        self.assertFalse(u.verify_password('dog'))

    def test_5_password_salts_are_random(self):
        u1 = User(password='cat')
        u2 = User(password='dog')
        self.assertNotEqual(u1.password_hash, u2.password_hash)

    def test_6_create_user(self):
        email = 'lucy@163.com'
        u = User(email=email, username='Lucy', password='cat')
        db.session.add(u)
        db.session.commit()
        u = User.query.filter_by(email=email).first()
        self.assertIsNotNone(u)
