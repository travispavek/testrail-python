import copy
from datetime import datetime
import mock
try:
    import unittest2 as unittest
except ImportError:
    import unittest

from testrail.helper import TestRailError
from testrail.project import Project
from testrail.suite import Suite


class TestSuite(unittest.TestCase):
    def setUp(self):

        self.mock_suite_data = {
            "description": "suite description",
            "id": 1,
            "name": "Setup & Installation",
            "project_id": 1,
            "url": "http://<server>/index.php?/suites/view/1",
            "is_baseline": False,
            "is_completed": True,
            "is_master": True,
            "completed_on": 1453504099
        }

        self.mock_project_data = [
            {
                "announcement": "..",
                "completed_on": 1653504099,
                "id": 1,
                "is_completed": False,
                "name": "Project1",
                "show_announcement": True,
                "url": "http://<server>/index.php?/projects/overview/1",
                "suite_mode": 3
            },
            {
                "announcement": "..",
                "completed_on": 1453504099,
                "id": 2,
                "is_completed": True,
                "name": "Project2",
                "show_announcement": True,
                "url": "http://<server>/index.php?/projects/overview/1",
                "suite_mode": 3
            }
        ]

        self.suite = Suite(self.mock_suite_data)

    def test_get_completed_on_type(self):
        self.assertEqual(type(self.suite.completed_on), datetime)

    def test_get_completed_on(self):
        date_obj = datetime.fromtimestamp(1453504099)
        self.assertEqual(self.suite.completed_on, date_obj)

    def test_get_completed_on_not_completed(self):
        self.suite._content['completed_on'] = None
        self.suite._content['is_completed'] = False
        self.assertEqual(self.suite.completed_on, None)

    def test_get_id_type(self):
        self.assertEqual(type(self.suite.id), int)

    def test_get_id(self):
        self.assertEqual(self.suite.id, 1)

    def test_get_is_baseline_type(self):
        self.assertEqual(type(self.suite.is_baseline), bool)

    def test_get_is_baseline(self):
        self.assertEqual(self.suite.is_baseline, False)

    def test_get_is_completed_type(self):
        self.assertEqual(type(self.suite.is_completed), bool)

    def test_get_is_completed(self):
        self.assertEqual(self.suite.is_completed, True)

    def test_get_is_master_type(self):
        self.assertEqual(type(self.suite.is_master), bool)

    def test_get_is_master(self):
        self.assertEqual(self.suite.is_master, True)

    def test_get_description_type(self):
        self.assertEqual(type(self.suite.description), str)

    def test_get_description(self):
        self.assertEqual(self.suite.description, 'suite description')

    def test_set_description(self):
        description = 'new description'
        self.suite.description = description
        self.assertEqual(self.suite.description, description)
        self.assertEqual(self.suite._content['description'], description)

    def test_set_description_invalid_type(self):
        with self.assertRaises(TestRailError) as e:
            self.suite.description = 394
        self.assertEqual(str(e.exception), 'input must be a string')

    def test_get_name_type(self):
        self.assertEqual(type(self.suite.name), str)

    def test_get_name(self):
        self.assertEqual(self.suite.name, 'Setup & Installation')

    def test_set_name(self):
        name = 'my new suite'
        self.suite.name = name
        self.assertEqual(self.suite.name, name)
        self.assertEqual(self.suite._content['name'], name)

    def test_set_name_invalid_type(self):
        with self.assertRaises(TestRailError) as e:
            self.suite.name = 394
        self.assertEqual(str(e.exception), 'input must be a string')

    def test_get_url_type(self):
        self.assertEqual(type(self.suite.url), str)

    def test_get_url(self):
        self.assertEqual(
            self.suite.url, 'http://<server>/index.php?/suites/view/1')

    @mock.patch('testrail.api.requests.get')
    def test_get_project_type(self, mock_get):
        mock_response = mock.Mock()
        mock_response.json.return_value = copy.deepcopy(self.mock_project_data)
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        self.assertEqual(type(self.suite.project), Project)

    @mock.patch('testrail.api.requests.get')
    def test_get_project(self, mock_get):
        mock_response = mock.Mock()
        mock_response.json.return_value = copy.deepcopy(self.mock_project_data)
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        self.assertEqual(self.suite.project.id, 1)

    @mock.patch('testrail.api.requests.get')
    def test_get_project_invalid_id(self, mock_get):
        mock_response = mock.Mock()
        mock_response.json.return_value = copy.deepcopy(self.mock_project_data)
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        self.suite._content['project_id'] = 200
        with self.assertRaises(TestRailError) as e:
            self.suite.project
        self.assertEqual(str(e.exception), "Project ID '200' was not found")

    @mock.patch('testrail.api.API._refresh')
    @mock.patch('testrail.api.requests.get')
    def test_set_project(self, mock_get, refresh_mock):
        refresh_mock.return_value = True
        mock_response = mock.Mock()
        mock_response.json.return_value = copy.deepcopy(self.mock_project_data)
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        self.assertEqual(self.suite.project.id, 1)
        self.suite.project = Project(self.mock_project_data[1])
        self.assertEqual(self.suite._content['project_id'], 2)
        self.assertEqual(self.suite.project.id, 2)

    def test_set_project_invalid_type(self):
        with self.assertRaises(TestRailError) as e:
            self.suite.project = 2
        self.assertEqual(str(e.exception), 'input must be a Project')

    @mock.patch('testrail.api.requests.get')
    def test_set_project_invalid_project(self, mock_get):
        mock_response = mock.Mock()
        mock_response.json.return_value = copy.deepcopy(self.mock_project_data)
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        project = Project()
        project._content['id'] = 5
        with self.assertRaises(TestRailError) as e:
            self.suite.project = project
        self.assertEqual(str(e.exception),
                         "Project ID '5' was not found")

    @mock.patch('testrail.api.requests.get')
    def test_set_project_empty_project(self, mock_get):
        mock_response = mock.Mock()
        mock_response.json.return_value = copy.deepcopy(self.mock_project_data)
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        with self.assertRaises(TestRailError) as e:
            self.suite.project = Project()
        self.assertEqual(str(e.exception),
                         "Project ID 'None' was not found")

    def test_raw_data(self):
        self.assertEqual(self.suite.raw_data(), self.mock_suite_data)

    def test_raw_data_type(self):
        self.assertEqual(type(self.suite.raw_data()), dict)
