import unittest

from testrail.priority import Priority


class TestCaseType(unittest.TestCase):
    def setUp(self):
        self.priority = Priority(
            {
                "id": 4,
                "is_default": True,
                "name": "4 - Must Test",
                "priority": 4,
                "short_name": "4 - Must"
            }
        )

    def test_get_id_type(self):
        self.assertEqual(type(self.priority.id), int)

    def test_get_id(self):
        self.assertEqual(self.priority.id, 4)

    def test_get_is_default_type(self):
        self.assertEqual(type(self.priority.is_default), bool)

    def test_get_is_default(self):
        self.assertEqual(self.priority.is_default, True)

    def test_get_name_type(self):
        self.assertEqual(type(self.priority.name), str)

    def test_get_name(self):
        self.assertEqual(self.priority.name, '4 - Must Test')

    def test_get_short_name_type(self):
        self.assertEqual(type(self.priority.short_name), str)

    def test_get_short_name(self):
        self.assertEqual(self.priority.short_name, '4 - Must')

    def test_get_level_type(self):
        self.assertEqual(type(self.priority.level), int)

    def test_get_level(self):
        self.assertEqual(self.priority.level, 4)
