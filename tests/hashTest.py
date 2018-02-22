
import unittest

from main.model.user import User


class TestUser(unittest.TestCase):
    def test_init(self):
        user = User(username='admin', password='admin')
        self.assertEqual(user.username, "admin")
        self.assertNotEqual(user.password, None)
        self.assertNotEqual(user.salt, None)

    def test_login(self):
        user = User(username='admin', password='admin')


