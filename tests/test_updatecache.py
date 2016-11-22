from copy import deepcopy
from builtins import dict
from datetime import datetime as dt

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
                'ts': dt.now(),
                'value': [
                    {'id': 'id00', 'val': 'oldval'},
                    {'id': 'id01', 'val': 'oldval'},
                    {'id': 'id02', 'val': 'oldval'},
                    {'id': 'id03', 'val': 'oldval'},
                    {'id': 'id04', 'val': 'oldval'}
                ]
            },
            1: {
                'ts': dt.now(),
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

    def test_cache_add_when_no_timestamp(self,):
        no_ts_cache = deepcopy(self.mock_cache)
        no_ts_cache[1]['ts'] = None
        no_ts_obj = {'id': 'id11', 'val': 'test_cache_update', 'project_id': 1}

        @UpdateCache(no_ts_cache)
        def cache_update_func():
            return no_ts_obj

        cache_update_func()

        self.assertEqual(len(no_ts_cache[0]['value']), 5)
        self.assertEqual(len(no_ts_cache[1]['value']), 5)
        self.assertEqual(no_ts_cache[1]['value'][1]['val'], 'oldval')

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

    def test_cache_update_when_no_timestamp(self,):
        no_ts_cache = deepcopy(self.mock_cache)
        no_ts_cache[1]['ts'] = None
        no_ts_obj = {'id': 'id15', 'val': 'test_cache_update', 'project_id': 1}

        @UpdateCache(no_ts_cache)
        def cache_update_func():
            return no_ts_obj

        cache_update_func()

        self.assertEqual(len(no_ts_cache[0]['value']), 5)
        self.assertEqual(len(no_ts_cache[1]['value']), 5)

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

    def test_cache_refresh(self,):
        refresh_cache = deepcopy(self.mock_cache)
        force_refresh_obj = {}
        id_to_delete = 'id23'

        @UpdateCache(refresh_cache)
        def cache_refresh_func(val):
            return force_refresh_obj

        cache_refresh_func(id_to_delete)

        self.assertEqual(len(refresh_cache[0]['value']), 5)
        self.assertEqual(len(refresh_cache[1]['value']), 5)
        self.assertTrue(all([x['ts'] is None for x in refresh_cache.values()]))
