import unittest

from testrail.casetype import CaseType


class TestCaseType(unittest.TestCase):
    def setUp(self):
        self.casetype = CaseType(
            {
            	"id": 1,
            	"is_default": False,
            	"name": "Automated"
            }
        )

    def test_get_id_type(self):
        self.assertEqual(type(self.casetype.id), int)

    def test_get_id(self):
        self.assertEqual(self.casetype.id, 1)

    def test_get_is_default_type(self):
        self.assertEqual(type(self.casetype.is_default), bool)

    def test_get_is_default(self):
        self.assertEqual(self.casetype.is_default, False)

    def test_get_name_type(self):
        self.assertEqual(type(self.casetype.name), str)

    def test_get_name(self):
        self.assertEqual(self.casetype.name, 'Automated')
