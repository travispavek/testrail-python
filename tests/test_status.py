import mock
try:
    import unittest2 as unittest
except ImportError:
    import unittest

from testrail.status import Status

class TestStatus(unittest.TestCase):
    def setUp(self):
        self.mock_status_data = {
            "color_bright": 13684944,
            "color_dark": 0,
            "color_medium": 10526880,
            "id": 6,
            "is_final": False,
            "is_system": True,
            "is_untested": False,
            "label": "Mock Custom",
            "name": "mock_custom_status1"
        }
        self.status = Status(self.mock_status_data)

    def test_get_id_type(self):
        self.assertTrue(isinstance(self.status.id, int))

    def test_get_id(self):
        self.assertEqual(self.status.id, 6)

    def test_get_name_type(self):
        self.assertTrue(isinstance(self.status.name, str))

    def test_get_name(self):
        self.assertEqual(self.status.name, 'mock_custom_status1')

    def test_get_label_type(self):
        self.assertTrue(isinstance(self.status.label, str))

    def test_get_label(self):
        self.assertEqual(self.status.label, 'Mock Custom')

    def test_get_is_untested_type(self):
        self.assertTrue(isinstance(self.status.is_untested, bool))

    def test_get_is_untested(self):
        self.assertFalse(self.status.is_untested)

    def test_get_is_system_type(self):
        self.assertTrue(isinstance(self.status.is_system, bool))

    def test_get_is_system(self):
        self.assertTrue(self.status.is_system)

    def test_get_is_final_type(self):
        self.assertTrue(isinstance(self.status.is_final, bool))

    def test_get_is_final(self):
        self.assertFalse(self.status.is_final)

    def test_get_color_medium_type(self):
        self.assertTrue(isinstance(self.status.color_medium, int))

    def test_get_color_medium(self):
        self.assertEqual(self.status.color_medium, 10526880)

    def test_get_color_dark_type(self):
        self.assertTrue(isinstance(self.status.color_dark, int))

    def test_get_color_medium(self):
        self.assertEqual(self.status.color_dark, 0)

    def test_get_color_bright_type(self):
        self.assertTrue(isinstance(self.status.color_bright, int))

    def test_get_color_bright(self):
        self.assertEqual(self.status.color_bright, 13684944)
