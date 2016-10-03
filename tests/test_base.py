import mock
try:
    import unittest2 as unittest
except ImportError:
    import unittest

from testrail.base import TestRailBase


class TestBase(unittest.TestCase):
    def setUp(self):
        class Foo(TestRailBase):
            def __init__(self, id):
                self.id = id

        self.base = Foo(123)

    def test___str__(self):
        self.assertEqual(str(self.base), "Foo-123")

    def test___repr__(self):
        self.assertEqual(repr(self.base), "Foo-123")
