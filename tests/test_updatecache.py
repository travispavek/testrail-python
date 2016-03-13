from copy import deepcopy
from builtins import dict

try:
    import unittest2 as unittest
except ImportError:
    import unittest

import mock

from testrail.api import UpdateCache
from testrail.helper import TestRailError


class TestUpdateCache(unittest.TestCase):
    def setUp(self):
        self.mock_cache = {
            0: {
                'value': [
                    {'id': 'id00', 'val': 'oldval'},
                    {'id': 'id01', 'val': 'oldval'},
                    {'id': 'id02', 'val': 'oldval'},
                    {'id': 'id03', 'val': 'oldval'},
                    {'id': 'id04', 'val': 'oldval'}
                ]
            },
            1: {
                'value': [
                    {'id': 'id10', 'val': 'oldval'},
                    {'id': 'id11', 'val': 'oldval'},
                    {'id': 'id12', 'val': 'oldval'},
                    {'id': 'id13', 'val': 'oldval'},
                    {'id': 'id14', 'val': 'oldval'}
                ]
            }
        }

    def tearDown(self):
            pass

    def test_cache_add(self,):
        add_cache = deepcopy(self.mock_cache)
        add_obj = {'id': 'id15', 'val': 'test_cache_add', 'project_id': 1}
 
        @UpdateCache(add_cache)
        def cache_add_func():
            return add_obj

        cache_add_func()

        self.assertEqual(len(add_cache[0]['value']), 5)
        self.assertEqual(len(add_cache[1]['value']), 6)
        self.assertEqual(add_cache[1]['value'][-1], add_obj)

    def test_cache_update(self,):
        update_cache = deepcopy(self.mock_cache)
        update_obj = {'id': 'id12', 'val': 'test_cache_update', 'project_id': 1}
 
        @UpdateCache(update_cache)
        def cache_update_func():
            return update_obj

        cache_update_func()

        self.assertEqual(len(update_cache[0]['value']), 5)
        self.assertEqual(len(update_cache[1]['value']), 5)
        self.assertEqual(update_cache[1]['value'][2], update_obj)

    def test_cache_delete(self,):
        delete_cache = deepcopy(self.mock_cache)
        delete_obj = {}
        id_to_delete = 'id13'
 
        @UpdateCache(delete_cache)
        def cache_delete_func(val):
            return delete_obj

        cache_delete_func(id_to_delete)

        self.assertEqual(len(delete_cache[0]['value']), 5)
        self.assertEqual(len(delete_cache[1]['value']), 4)
        for project in delete_cache.values():
            for obj in project['value']:
                self.assertNotEqual(id_to_delete, obj['id'])

    def test_cache_raises_error(self,):
        raise_cache = deepcopy(self.mock_cache)
        raise_obj = {}
        id_to_delete = 'id23'
 
        @UpdateCache(raise_cache)
        def cache_raise_func(val):
            return raise_obj

        with self.assertRaises(TestRailError) as e:
            cache_raise_func(id_to_delete)

        self.assertEqual(len(raise_cache[0]['value']), 5)
        self.assertEqual(len(raise_cache[1]['value']), 5)
        exp_exc_str = "could not locate item with id {0}".format(id_to_delete)
        self.assertIn(exp_exc_str, str(e.exception))


