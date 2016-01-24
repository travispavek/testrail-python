import unittest

from testrail.user import User


class TestUser(unittest.TestCase):
    def setUp(self):
        self.mock_user_data = {
            "email": "han@example.com",
            "id": 1,
            "is_active": True,
            "name": "Han Solo"}

        self.user = User(self.mock_user_data)

    def test_get_email(self):
        self.assertEqual(self.user.email, 'han@example.com')

    def test_email_type(self):
        self.assertEqual(str, type(self.user.email))

    def test_get_id(self):
        self.assertEqual(self.user.id, 1)

    def test_id_type(self):
        self.assertEqual(int, type(self.user.id))

    def test_get_is_active(self):
        self.assertEqual(self.user.is_active, True)

    def test_is_active_type(self):
        self.assertEqual(bool, type(self.user.is_active))

    def test_get_name(self):
        self.assertEqual(self.user.name, 'Han Solo')

    def test_name_type(self):
        self.assertEqual(str, type(self.user.name))
