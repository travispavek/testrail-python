import copy
from datetime import datetime, timedelta
import mock
import unittest

from testrail.helper import TestRailError
from testrail.result import Result
from testrail.status import Status
from testrail.test import Test
from testrail.user import User


class TestUser(unittest.TestCase):

    def setUp(self):
        self.mock_result_data = {
            'assignedto_id': 1,
            'comment': 'All steps passed',
            'created_by': 2,
            'created_on': 1453504099,
            'defects': 'def1, def2, def3',
            'elapsed': '1w 3d 6h 2m 30s',
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

        self.mock_status_data = [
            {
                "color_bright": 12709313,
                "color_dark": 6667107,
                "color_medium": 9820525,
                "id": 1,
                "is_final": True,
                "is_system": True,
                "is_untested": True,
                "label": "Passed",
                "name": "passed"
            }
        ]

        self.mock_test_data = [
            {
                "assignedto_id": 1,
                "case_id": 1,
                "estimate": "1m 5s",
                "estimate_forecast": None,
                "id": 5,
                "priority_id": 2,
                "run_id": 1,
                "status_id": 5,
                "title": "Verify line spacing on multi-page document",
                "type_id": 4
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

    def test_get_assigned_to_null(self):
        self.result._content['assignedto_id'] = None
        self.assertEqual(self.result.assigned_to, None)

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

    def test_get_comment_null(self):
        self.result._content['comment'] = None
        self.assertEqual(self.result.comment, None)

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

    def test_get_elapsed_type(self):
        self.assertEqual(type(self.result.elapsed), timedelta)

    def test_get_elapsed_null(self):
        self.result._content['elapsed'] = None
        self.assertEqual(self.result.elapsed, None)

    def test_get_elapsed_weeks(self):
        self.result._content['elapsed'] = '10w'
        td = timedelta(weeks=10)
        self.assertEqual(self.result.elapsed, td)

    def test_get_elapsed_days(self):
        self.result._content['elapsed'] = '4d'
        td = timedelta(days=4)
        self.assertEqual(self.result.elapsed, td)

    def test_get_elapsed_hours(self):
        self.result._content['elapsed'] = '10h'
        td = timedelta(hours=10)
        self.assertEqual(self.result.elapsed, td)

    def test_get_elapsed_minutes(self):
        self.result._content['elapsed'] = '10m'
        td = timedelta(minutes=10)
        self.assertEqual(self.result.elapsed, td)

    def test_get_elapsed_seconds(self):
        self.result._content['elapsed'] = '120s'
        td = timedelta(minutes=2)
        self.assertEqual(self.result.elapsed, td)

    def test_get_elapsed_all(self):
        td = timedelta(weeks=1, days=3, hours=6, minutes=2, seconds=30)
        self.assertEqual(self.result.elapsed, td)

    def test_set_elapsed_invalid_type(self):
        with self.assertRaises(TestRailError) as e:
            self.result.elapsed = '5m'
        self.assertEqual(str(e.exception), 'input must be a timedelta')

    def test_set_elasped_invalid_value(self):
        with self.assertRaises(TestRailError) as e:
            self.result.elapsed = timedelta(weeks=10, seconds=1)
        self.assertEqual(str(e.exception), 'maximum elapsed time is 10 weeks')

    def test_set_elapsed(self):
        self.result.elapsed = timedelta(hours=2, seconds=30)
        self.assertEqual(self.result._content['elapsed'], 7230)

    def test_get_id_type(self):
        self.assertEqual(type(self.result.id), int)

    def test_get_id(self):
        self.assertEqual(self.result.id, 3)

    @mock.patch('testrail.api.requests.get')
    def test_get_status_type(self, mock_get):
        mock_response = mock.Mock()
        mock_response.json.return_value = copy.deepcopy(self.mock_status_data)
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        self.assertEqual(type(self.result.status), Status)

    @mock.patch('testrail.api.requests.get')
    def test_get_status(self, mock_get):
        mock_response = mock.Mock()
        mock_response.json.return_value = copy.deepcopy(self.mock_status_data)
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        self.assertEqual(self.result.status.label, 'Passed')

    @mock.patch('testrail.api.requests.get')
    def test_get_status_invalid_id(self, mock_get):
        mock_response = mock.Mock()
        mock_response.json.return_value = copy.deepcopy(self.mock_status_data)
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        self.result._content['status_id'] = 0
        with self.assertRaises(TestRailError) as e:
            self.result.status
        self.assertEqual(str(e.exception), "Status ID '0' was not found")

    def test_set_status_invalid_type(self):
        with self.assertRaises(TestRailError) as e:
            self.result.status = 'passed'
        self.assertEqual(str(e.exception), 'input must be a Status')

    @mock.patch('testrail.api.requests.get')
    def test_set_status(self, mock_get):
        mock_response = mock.Mock()
        mock_response.json.return_value = copy.deepcopy(self.mock_status_data)
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        self.result.status = Status({'id': 1})
        self.assertEqual(self.result._content['status_id'], 1)

    @mock.patch('testrail.api.requests.get')
    def test_set_status_invalid_id(self, mock_get):
        mock_response = mock.Mock()
        mock_response.json.return_value = copy.deepcopy(self.mock_status_data)
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        with self.assertRaises(TestRailError) as e:
            self.result.status = Status({'id': 0})
        self.assertEqual(str(e.exception), "Status ID '0' was not found")

    @mock.patch('testrail.api.requests.get')
    def test_get_test_type(self, mock_get):
        mock_response = mock.Mock()
        mock_response.json.return_value = copy.deepcopy(self.mock_test_data)
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        self.assertEqual(type(self.result.test), Test)

    @mock.patch('testrail.api.requests.get')
    def test_get_test(self, mock_get):
        mock_response = mock.Mock()
        mock_response.json.return_value = copy.deepcopy(self.mock_test_data)
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        self.assertEqual(self.result.test.id, 5)

    @mock.patch('testrail.api.requests.get')
    def test_get_test_invalid_id(self, mock_get):
        mock_response = mock.Mock()
        mock_response.json.return_value = copy.deepcopy(self.mock_test_data)
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        self.result._content['test_id'] = 100
        with self.assertRaises(TestRailError) as e:
            self.result.test
        self.assertEqual(str(e.exception), "Test ID '100' was not found")

    def test_set_test_invalid_type(self):
        with self.assertRaises(TestRailError) as e:
            self.result.test = 5
        self.assertEqual(str(e.exception), 'input must be a Test')

    @mock.patch('testrail.api.requests.get')
    def test_set_test(self, mock_get):
        mock_response = mock.Mock()
        mock_response.json.return_value = copy.deepcopy(self.mock_test_data)
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        self.result.test = Test({'id': 5, 'run_id': 1})
        self.assertEqual(self.result._content['test_id'], 5)

    @mock.patch('testrail.api.requests.get')
    def test_set_test_invalid_id(self, mock_get):
        mock_response = mock.Mock()
        mock_response.json.return_value = copy.deepcopy(self.mock_test_data)
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        with self.assertRaises(TestRailError) as e:
            self.result.test = Test({'id': 100, 'run_id': 1})
        self.assertEqual(str(e.exception), "Test ID '100' was not found")

    def test_get_version_type(self):
        self.assertEqual(type(self.result.version), str)

    def test_get_version_null(self):
        self.result._content['version'] = None
        self.assertEqual(self.result.version, None)

    def test_get_version(self):
        self.assertEqual(self.result.version, '1.0RC')

    def test_set_version_invalid_type(self):
        with self.assertRaises(TestRailError) as e:
            self.result.version = 1.0
        self.assertEqual(str(e.exception), 'input must be a string')

    def test_set_version(self):
        self.result.version = '2.0'
        self.assertEqual(self.result._content['version'], '2.0')

    def test_raw_data(self):
        self.assertEqual(self.result.raw_data(), self.mock_result_data)
