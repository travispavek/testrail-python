import mock
import unittest
from testrail.api import API
from testrail.helper import TestRailError
import copy
import ast
from datetime import datetime, timedelta
import util


class TestHTTPMethod(unittest.TestCase):
    def setUp(self):
        self.client = API()

    @mock.patch('testrail.api.requests.get')
    def test_get_ok(self, mock_get):
        mock_response = mock.Mock()
        return_value = {
            "announcement": "..",
            "completed_on": None,
            "id": 1,
            "is_completed": False,
            "name": "Datahub",
            "show_announcement": True,
            "url": "http://<server>/index.php?/projects/overview/1"
        }

        expected_response = copy.deepcopy(return_value)
        mock_response.json.return_value = return_value
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        url = 'https://<server>/index.php?/api/v2/get_project/1'
        actual_response = self.client._get('get_project/1')
        mock_get.assert_called_once_with(
            url,
            headers={'Content-Type': 'application/json'},
            params=None,
            auth=('user@yourdomain.com', 'your_api_key')
        )
        self.assertEqual(1, mock_response.json.call_count)
        self.assertEqual(expected_response, actual_response)

    @mock.patch('testrail.api.requests.get')
    def test_get_bad_no_params(self, mock_get):
        mock_response = mock.Mock()
        expected_response = {
            'url': 'https://<server>/index.php?/api/v2/get_plan/200',
            'status_code': 400,
            'payload': None,
            'error': 'Invalid or unknown test plan'
        }
        url = 'https://<server>/index.php?/api/v2/get_plan/200'
        mock_response.json.return_value = {
            'error': 'Invalid or unknown test plan'
        }
        mock_response.status_code = 400
        mock_response.url = url
        mock_get.return_value = mock_response

        with self.assertRaises(TestRailError) as e:
            self.client._get('get_plan/200')
        mock_get.assert_called_once_with(
            url,
            headers={'Content-Type': 'application/json'},
            params=None,
            auth=('user@yourdomain.com', 'your_api_key')
        )
        self.assertEqual(1, mock_response.json.call_count)
        self.assertEqual(expected_response, ast.literal_eval(str(e.exception)))


class TestUser(unittest.TestCase):
    def setUp(self):
        self.client = API()
        self.mock_user_data = [
            {
                "email": "han@example.com",
                "id": 1,
                "is_active": 'true',
                "name": "Han Solo"
            },
            {
                "email": "jabba@example.com",
                "id": 2,
                "is_active": 'true',
                "name": "Jabba the Hutt"
            }
        ]

        self.users = copy.deepcopy(self.mock_user_data)

    def tearDown(self):
        util.reset_shared_state(self.client)

    @mock.patch('testrail.api.requests.get')
    def test_get_users(self, mock_get):
        mock_response = mock.Mock()
        expected_response = self.users
        url = 'https://<server>/index.php?/api/v2/get_users'
        mock_response.json.return_value = self.mock_user_data
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        actual_response = self.client.users()
        timeout = self.client._timeout
        # set timeout to 1 second from now
        delta = timedelta(seconds=timeout-1)
        self.client._users['ts'] = datetime.now() - delta
        actual_response = self.client.users()  # verify cache hit
        mock_get.assert_called_once_with(
            url,
            headers={'Content-Type': 'application/json'},
            params=None,
            auth=('user@yourdomain.com', 'your_api_key')
        )
        self.assertEqual(1, mock_response.json.call_count)
        self.assertEqual(expected_response, actual_response)

    @mock.patch('testrail.api.requests.get')
    def test_get_users_cache_timeout(self, mock_get):
        self.client = API()
        mock_response = mock.Mock()
        expected_response = self.users
        url = 'https://<server>/index.php?/api/v2/get_users'
        mock_response.json.return_value = self.mock_user_data
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        actual_response = self.client.users()
        timeout = self.client._timeout
        self.client._users['ts'] = datetime.now() - timedelta(seconds=timeout)
        actual_response = self.client.users()  # verity cache timed out
        mock_get.assert_called_twice_with(
            url,
            headers={'Content-Type': 'application/json'},
            params=None,
            auth=('user@yourdomain.com', 'your_api_key')
        )
        self.assertEqual(2, mock_response.json.call_count)
        self.assertEqual(expected_response, actual_response)

    @mock.patch('testrail.api.requests.get')
    def test_get_user_with_id(self, mock_get):
        mock_response = mock.Mock()
        expected_response = filter(
            lambda x: x if x['id'] == 2 else None, self.users)[0]
        url = 'https://<server>/index.php?/api/v2/get_users'
        mock_response.json.return_value = self.mock_user_data
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        actual_response = self.client.user_with_id(2)
        actual_response = self.client.user_with_id(2)  # verify cache hit
        mock_get.assert_called_once_with(
            url,
            headers={'Content-Type': 'application/json'},
            params=None,
            auth=('user@yourdomain.com', 'your_api_key')
        )
        self.assertEqual(1, mock_response.json.call_count)
        self.assertEqual(expected_response, actual_response)

    @mock.patch('testrail.api.requests.get')
    def test_get_user_invalid_id(self, mock_get):
        mock_response = mock.Mock()
        mock_response.json.return_value = self.mock_user_data
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        with self.assertRaises(TestRailError) as e:
            self.client.user_with_id(300)
        err_msg = "User ID '300' was not found"
        self.assertEqual(err_msg, str(e.exception))

    @mock.patch('testrail.api.requests.get')
    def test_get_user_with_email(self, mock_get):
        mock_response = mock.Mock()
        expected_response = filter(
            lambda x: x if x['email'] == 'han@example.com' else None,
            self.users)[0]
        url = 'https://<server>/index.php?/api/v2/get_users'
        mock_response.json.return_value = self.mock_user_data
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        actual_response = self.client.user_with_email('han@example.com')
        # verify cache hit
        actual_response = self.client.user_with_email('han@example.com')
        mock_get.assert_called_once_with(
            url,
            headers={'Content-Type': 'application/json'},
            params=None,
            auth=('user@yourdomain.com', 'your_api_key')
        )
        self.assertEqual(1, mock_response.json.call_count)
        self.assertEqual(expected_response, actual_response)

    @mock.patch('testrail.api.requests.get')
    def test_get_user_invalid_email(self, mock_get):
        mock_response = mock.Mock()
        mock_response.json.return_value = self.mock_user_data
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        with self.assertRaises(TestRailError) as e:
            self.client.user_with_email('invalid@example.com')
        err_msg = "User email 'invalid@example.com' was not found"
        self.assertEqual(err_msg, str(e.exception))


class TestProject(unittest.TestCase):
    def setUp(self):
        self.client = API()
        self.mock_project_data = [
            {
                "announcement": "..",
                "completed_on": None,
                "id": 1,
                "is_completed": False,
                "name": "Project1",
                "show_announcement": True,
                "url": "http://<server>/testrail/index.php?/projects/overview/1"
            },
            {
                "announcement": "..",
                "completed_on": False,
                "id": 2,
                "is_completed": True,
                "name": "Project2",
                "show_announcement": True,
                "url": "http://<server>/testrail/index.php?/projects/overview/2"
            }
        ]

        self.projects = copy.deepcopy(self.mock_project_data)

    def tearDown(self):
        util.reset_shared_state(self.client)

    @mock.patch('testrail.api.requests.get')
    def test_get_projects(self, mock_get):
        mock_response = mock.Mock()
        expected_response = self.projects
        url = 'https://<server>/index.php?/api/v2/get_projects'
        mock_response.json.return_value = self.mock_project_data
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        actual_response = self.client.projects()
        timeout = self.client._timeout
        # set timeout to 1 second from now
        delta = timedelta(seconds=timeout-1)
        self.client._users['ts'] = datetime.now() - delta
        actual_response = self.client.projects()  # verify cache hit
        mock_get.assert_called_once_with(
            url,
            headers={'Content-Type': 'application/json'},
            params=None,
            auth=('user@yourdomain.com', 'your_api_key')
        )
        self.assertEqual(1, mock_response.json.call_count)
        self.assertEqual(expected_response, actual_response)

    @mock.patch('testrail.api.requests.get')
    def test_get_projects_cache_timeout(self, mock_get):
        mock_response = mock.Mock()
        expected_response = self.projects
        url = 'https://<server>/index.php?/api/v2/get_projects'
        mock_response.json.return_value = self.mock_project_data
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        actual_response = self.client.projects()
        timeout = self.client._timeout
        self.client._projects['ts'] = datetime.now() - timedelta(
            seconds=timeout)
        actual_response = self.client.projects()  # verify cache hit
        mock_get.assert_called_twice_with(
            url,
            headers={'Content-Type': 'application/json'},
            params=None,
            auth=('user@yourdomain.com', 'your_api_key')
        )
        self.assertEqual(2, mock_response.json.call_count)
        self.assertEqual(expected_response, actual_response)

    @mock.patch('testrail.api.requests.get')
    def test_get_project_id(self, mock_get):
        mock_response = mock.Mock()
        expected_response = filter(
            lambda x: x if x['id'] == 1 else None, self.projects)[0]
        url = 'https://<server>/index.php?/api/v2/get_projects'
        mock_response.json.return_value = self.mock_project_data
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        actual_response = self.client.project_with_id(1)
        actual_response = self.client.project_with_id(1)  # verify cache hit
        mock_get.assert_called_once_with(
            url,
            headers={'Content-Type': 'application/json'},
            params=None,
            auth=('user@yourdomain.com', 'your_api_key')
        )
        self.assertEqual(1, mock_response.json.call_count)
        self.assertEqual(expected_response, actual_response)

    @mock.patch('testrail.api.requests.get')
    def test_get_project_invalid_id(self, mock_get):
        mock_response = mock.Mock()
        mock_response.json.return_value = self.mock_project_data
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        with self.assertRaises(TestRailError) as e:
            self.client.project_with_id(300)
        err_msg = "Project ID '300' was not found"
        self.assertEqual(err_msg, str(e.exception))

class TestSuite(unittest.TestCase):
    def setUp(self):
        self.client = API()
        self.client._project_id = 1
        self.mock_suites_data_1 = [
            {
                "description": "..",
                "id": 1,
                "name": "Setup & Installation",
                "project_id": 1,
                "url": "http://<server>/testrail/index.php?/suites/view/1"
            },
            {
                "description": "..",
                "id": 2,
                "name": "Setup & Installation",
                "project_id": 1,
                "url": "http://<server>/testrail/index.php?/suites/view/2"
            }]
        self.mock_suites_data_2 = [
            {
                "description": "..",
                "id": 3,
                "name": "Setup & Installation",
                "project_id": 2,
                "url": "http://<server>/testrail/index.php?/suites/view/1"
            },
            {
                "description": "..",
                "id": 4,
                "name": "Setup & Installation",
                "project_id": 2,
                "url": "http://<server>/testrail/index.php?/suites/view/2"
            }
        ]

        self.suites_1 = copy.deepcopy(self.mock_suites_data_1)
        self.suites_2 = copy.deepcopy(self.mock_suites_data_2)

    def tearDown(self):
        util.reset_shared_state(self.client)

    @mock.patch('testrail.api.requests.get')
    def test_get_suites(self, mock_get):
        mock_response = mock.Mock()
        expected_response = self.suites_1
        url = 'https://<server>/index.php?/api/v2/get_suites/1'
        mock_response.json.return_value = self.mock_suites_data_1
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        actual_response = self.client.suites()
        actual_response = self.client.suites()  # verify cache hit
        mock_get.assert_called_once_with(
            url,
            headers={'Content-Type': 'application/json'},
            params=None,
            auth=('user@yourdomain.com', 'your_api_key')
        )
        self.assertEqual(1, mock_response.json.call_count)
        self.assertEqual(expected_response, actual_response)

    @mock.patch('testrail.api.requests.get')
    def test_get_suites_with_project(self, mock_get):
        mock_response = mock.Mock()
        expected_response = self.suites_2
        url = 'https://<server>/index.php?/api/v2/get_suites/2'
        mock_response.json.return_value = self.mock_suites_data_2
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        actual_response = self.client.suites(2)
        actual_response = self.client.suites(2)  # verify cache hit
        mock_get.assert_called_once_with(
            url,
            headers={'Content-Type': 'application/json'},
            params=None,
            auth=('user@yourdomain.com', 'your_api_key')
        )
        self.assertEqual(1, mock_response.json.call_count)
        self.assertEqual(expected_response, actual_response)

    @mock.patch('testrail.api.requests.get')
    def test_get_suites_invalid_project(self, mock_get):
        mock_response = mock.Mock()
        mock_response.json.return_value = {}
        mock_response.status_code = 400
        mock_get.return_value = mock_response
        with self.assertRaises(TestRailError):
            self.client.suites(20)

    @mock.patch('testrail.api.requests.get')
    def test_get_suites_cache_timeout(self, mock_get):
        mock_response = mock.Mock()
        expected_response = self.suites_1
        url = 'https://<server>/index.php?/api/v2/get_suites/1'
        mock_response.json.return_value = self.mock_suites_data_1
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        self.client.suites()
        timeout = self.client._timeout
        self.client._suites[1]['ts'] = datetime.now() - timedelta(
            seconds=timeout)
        actual_response = self.client.suites()  # verify cache timeout
        mock_get.assert_called_twice_with(
            url,
            headers={'Content-Type': 'application/json'},
            params=None,
            auth=('user@yourdomain.com', 'your_api_key')
        )
        self.assertEqual(2, mock_response.json.call_count)
        self.assertEqual(expected_response, actual_response)

    @mock.patch('testrail.api.requests.get')
    def test_get_suites_different_projects_no_cache_hit(self, mock_get):
        mock_response = mock.Mock()
        expected_response = self.suites_1
        url = 'https://<server>/index.php?/api/v2/get_suites/1'
        mock_response.json.return_value = self.mock_suites_data_1
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        actual_response = self.client.suites()
        actual_response = self.client.suites(2)  # verify cache not hit
        mock_get.assert_called_twice_with(
            url,
            headers={'Content-Type': 'application/json'},
            params=None,
            auth=('user@yourdomain.com', 'your_api_key')
        )
        self.assertEqual(2, mock_response.json.call_count)
        self.assertEqual(expected_response, actual_response)

    @mock.patch('testrail.api.requests.get')
    def test_get_suite_with_id(self, mock_get):
        mock_response = mock.Mock()
        expected_response = filter(
            lambda x: x if x['id'] == 2 else None, self.suites_1)[0]
        url = 'https://<server>/index.php?/api/v2/get_suites/1'
        mock_response.json.return_value = self.mock_suites_data_1
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        actual_response = self.client.suite_with_id(2)
        actual_response = self.client.suite_with_id(2)  # verify cache hit
        mock_get.assert_called_once_with(
            url,
            headers={'Content-Type': 'application/json'},
            params=None,
            auth=('user@yourdomain.com', 'your_api_key')
        )
        self.assertEqual(1, mock_response.json.call_count)
        self.assertEqual(expected_response, actual_response)

    @mock.patch('testrail.api.requests.get')
    def test_get_suites_invalid_suite_id(self, mock_get):
        mock_response = mock.Mock()
        mock_response.json.return_value = {}
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        with self.assertRaises(TestRailError) as e:
            self.client.suite_with_id(20)
        self.assertEqual(str(e.exception), "Suite ID '20' was not found")


if __name__ == "__main__":
    unittest.main()
