import copy
from datetime import datetime
import mock
import unittest

from testrail.helper import TestRailError
from testrail.result import Result
from testrail.user import User


class TestUser(unittest.TestCase):

    def setUp(self):
        self.mock_result_data = {
            'assignedto_id': 1,
            'comment': 'All steps passed',
            'created_by': 2,
            'created_on': 1453504099,
            'defects': 'def1, def2, def3',
            'elapsed': '2m 30s',
            'id': 3,
            'status_id': 1,
            'test_id': 5,
            'version': '1.0RC'}

        self.mock_user_data = [
            {
                "email": "han@example.com",
                "id": 1,
                "is_active": True,
                "name": "Han Solo"
            },
            {
                "email": "jabba@example.com",
                "id": 2,
                "is_active": True,
                "name": "Jabba the Hutt"
            }
        ]

        self.result = Result(self.mock_result_data)

    @mock.patch('testrail.api.requests.get')
    def test_get_assigned_to_type(self, mock_get):
        mock_response = mock.Mock()
        mock_response.json.return_value = copy.deepcopy(self.mock_user_data)
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        user = self.result.assigned_to
        self.assertEqual(type(user), User)

    @mock.patch('testrail.api.requests.get')
    def test_get_assigned_to(self, mock_get):
        mock_response = mock.Mock()
        mock_response.json.return_value = copy.deepcopy(self.mock_user_data)
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        user = self.result.assigned_to
        self.assertEqual(user._content, self.mock_user_data[0])

    @mock.patch('testrail.api.requests.get')
    def test_set_assigned_to(self, mock_get):
        mock_response = mock.Mock()
        mock_response.json.return_value = copy.deepcopy(self.mock_user_data)
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        user = User(self.mock_user_data[1])
        self.assertEqual(self.result.assigned_to.id, 1)
        self.result.assigned_to = user
        self.assertEqual(self.result._content['assignedto_id'], 2)
        self.assertEqual(self.result.assigned_to.id, 2)

    def test_set_assigned_to_invalid_type(self):
        with self.assertRaises(TestRailError) as e:
            self.result.assigned_to = 2
        self.assertEqual(str(e.exception), 'input must be a User object')

    @mock.patch('testrail.api.requests.get')
    def test_set_assigned_to_invalid_user(self, mock_get):
        mock_response = mock.Mock()
        mock_response.json.return_value = copy.deepcopy(self.mock_user_data)
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        user = User()
        user._content['id'] = 5
        with self.assertRaises(TestRailError) as e:
            self.result.assigned_to = user
        self.assertEqual(str(e.exception),
                         "User with ID '%s' is not valid" % user.id)

    @mock.patch('testrail.api.requests.get')
    def test_set_assigned_to_empty_user(self, mock_get):
        mock_response = mock.Mock()
        mock_response.json.return_value = copy.deepcopy(self.mock_user_data)
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        user = User()
        with self.assertRaises(TestRailError) as e:
            self.result.assigned_to = user
        self.assertEqual(str(e.exception),
                         "User with ID '%s' is not valid" % user.id)

    def test_get_comment_type(self):
        self.assertEqual(type(self.result.comment), str)

    def test_get_comment(self):
        self.assertEqual(self.result.comment, 'All steps passed')

    def test_set_comment(self):
        self.assertEqual(self.result.comment, 'All steps passed')
        self.result.comment = 'tests failed'
        self.assertEqual(self.result._content['comment'], 'tests failed')
        self.assertEqual(self.result.comment, 'tests failed')

    def test_set_comment_invalid_type(self):
        with self.assertRaises(TestRailError) as e:
            self.result.comment = True
        self.assertEqual(str(e.exception), 'input must be a string')

    def test_get_created_type(self):
        self.assertEqual(type(self.result.created_by), User)

    @mock.patch('testrail.api.requests.get')
    def test_get_created_by(self, mock_get):
        mock_response = mock.Mock()
        mock_response.json.return_value = copy.deepcopy(self.mock_user_data)
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        user = self.result.created_by
        self.assertEqual(user._content, self.mock_user_data[1])

    def test_get_created_by_no_id(self):
        result = Result()
        with self.assertRaises(TestRailError) as e:
            result.created_by
        self.assertEqual(str(e.exception), "User ID 'None' was not found")

    def test_get_created_by_invalid_id(self):
        result = Result()
        result._content['created_by'] = 900
        with self.assertRaises(TestRailError) as e:
            result.created_by
        self.assertEqual(str(e.exception), "User ID '900' was not found")

    def test_get_created_on_type(self):
        self.assertEqual(type(self.result.created_on), datetime)

    def test_get_created_on(self):
        date_obj = datetime.fromtimestamp(1453504099)
        self.assertEqual(self.result.created_on, date_obj)

    def test_get_created_on_no_ts(self):
        self.assertEqual(Result().created_on, None)

    def test_get_defects_type(self):
        self.assertEqual(type(self.result.defects), list)

    def test_get_defects(self):
        self.assertEqual(
            self.result.defects, self.mock_result_data['defects'].split(','))

    def test_get_defects_empty(self):
        self.result._content['defects'] = None
        self.assertEqual(self.result.defects, list())

    def test_set_defects_invalid_type(self):
        with self.assertRaises(TestRailError) as e:
            self.result.defects = 'one, two'
        self.assertEqual(str(e.exception), 'input must be a list of strings')

    def test_set_defects_invalid_input(self):
        with self.assertRaises(TestRailError) as e:
            self.result.defects = ['one', 4]
        self.assertEqual(str(e.exception), 'input must be a list of strings')

    def test_set_defects(self):
        self.result.defects = ['1', 'b', '43']
        self.assertEqual(self.result._content['defects'], '1,b,43')

    def test_set_defects_empty_list(self):
        self.result.defects = list()
        self.assertEqual(self.result._content['defects'], None)
