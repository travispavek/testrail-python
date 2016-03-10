import copy
from datetime import datetime
import mock
try:
    import unittest2 as unittest
except ImportError:
    import unittest

from testrail.helper import TestRailError
from testrail.milestone import Milestone
from testrail.project import Project


class TestCaseType(unittest.TestCase):
    def setUp(self):
        self.mock_milestone_data = {
            "completed_on": 1389968184,
            "description": "foo",
            "due_on": 1391968184,
            "id": 1,
            "is_completed": True,
            "name": "Release 1.5",
            "project_id": 1,
            "url": "http://<server>/index.php?/milestones/view/1"
        }

        self.mock_project_data = [
            {
                "announcement": "..",
                "completed_on": 1453504099,
                "id": 1,
                "is_completed": True,
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

        self.milestone = Milestone(self.mock_milestone_data)

    def test_get_completed_on_type(self):
        self.assertEqual(type(self.milestone.completed_on), datetime)

    def test_get_completed_on(self):
        date_obj = datetime.fromtimestamp(1389968184)
        self.assertEqual(self.milestone.completed_on, date_obj)

    def test_get_completed_on_not_completed(self):
        milestone = Milestone({})
        self.assertEqual(milestone.completed_on, None)

    def test_get_description_type(self):
        self.assertEqual(type(self.milestone.description), str)

    def test_get_description(self):
        self.assertEqual(self.milestone.description, 'foo')

    def test_get_description_none(self):
        self.milestone._content['description'] = None
        self.assertEqual(self.milestone.description, None)

    def test_set_description_invalid_type(self):
        with self.assertRaises(TestRailError) as e:
            self.milestone.description = 2
        self.assertEqual(str(e.exception), 'input must be string or None')

    def test_set_description(self):
        self.milestone.description = 'bar'
        self.assertEqual(self.milestone._content['description'], 'bar')

    def test_set_description_none(self):
        self.milestone.description = None
        self.assertEqual(self.milestone._content['description'], None)

    def test_get_due_on_type(self):
        self.assertEqual(type(self.milestone.due_on), datetime)

    def test_get_due_on(self):
        date_obj = datetime.fromtimestamp(1391968184)
        self.assertEqual(self.milestone.due_on, date_obj)

    def test_get_due_on_none(self):
        milestone = Milestone({})
        self.assertEqual(milestone.due_on, None)

    def test_set_due_on_invalid_type(self):
        with self.assertRaises(TestRailError) as e:
            self.milestone.due_on = 'friday'
        self.assertEqual(str(e.exception), 'input must be a datetime or None')

    def test_set_due_on(self):
        ts = 1392468184
        self.milestone.due_on = datetime.fromtimestamp(ts)
        self.assertEqual(self.milestone._content['due_on'], ts)

    def test_set_due_on_none(self):
        self.milestone.due_on = None
        self.assertEqual(self.milestone._content['due_on'], None)

    def test_get_id_type(self):
        self.assertEqual(type(self.milestone.id), int)

    def test_get_id(self):
        self.assertEqual(self.milestone.id, 1)

    def test_get_is_completed_type(self):
        self.assertEqual(type(self.milestone.is_completed), bool)

    def test_get_is_completed(self):
        self.assertEqual(self.milestone.is_completed, True)

    def test_set_is_completed_type(self):
        with self.assertRaises(TestRailError) as e:
            self.milestone.is_completed = 1
        self.assertEqual(str(e.exception), 'input must be a boolean')

    def test_set_is_completed(self):
        self.milestone.is_completed = False
        self.assertEqual(self.milestone._content['is_completed'], False)

    def test_get_name_type(self):
        self.assertEqual(type(self.milestone.name), str)

    def test_get_name(self):
        self.assertEqual(self.milestone.name, 'Release 1.5')

    def test_set_name(self):
        name = 'new milestone'
        self.milestone.name = name
        self.assertEqual(self.milestone._content['name'], name)

    def test_set_name_invalid(self):
        with self.assertRaises(TestRailError) as e:
            self.milestone.name = 394
        self.assertEqual(str(e.exception), 'input must be a string')

    @mock.patch('testrail.api.requests.get')
    def test_get_project_type(self, mock_get):
        mock_response = mock.Mock()
        mock_response.json.return_value = copy.deepcopy(self.mock_project_data)
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        self.assertEqual(type(self.milestone.project), Project)

    @mock.patch('testrail.api.requests.get')
    def test_get_project(self, mock_get):
        mock_response = mock.Mock()
        mock_response.json.return_value = copy.deepcopy(self.mock_project_data)
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        self.assertEqual(self.milestone.project.id, 1)

    @mock.patch('testrail.api.requests.get')
    def test_get_project_invalid_id(self, mock_get):
        mock_response = mock.Mock()
        mock_response.json.return_value = copy.deepcopy(self.mock_project_data)
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        self.milestone._content['project_id'] = 200
        with self.assertRaises(TestRailError) as e:
            self.milestone.project
        self.assertEqual(str(e.exception), "Project ID '200' was not found")

    @mock.patch('testrail.api.requests.get')
    def test_set_project(self, mock_get):
        mock_response = mock.Mock()
        mock_response.json.return_value = copy.deepcopy(self.mock_project_data)
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        self.assertEqual(self.milestone.project.id, 1)
        self.milestone.project = Project(self.mock_project_data[1])
        self.assertEqual(self.milestone._content['project_id'], 2)
        self.assertEqual(self.milestone.project.id, 2)

    def test_set_project_invalid_type(self):
        with self.assertRaises(TestRailError) as e:
            self.milestone.project = 2
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
            self.milestone.project = project
        self.assertEqual(str(e.exception),
                         "Project ID '5' was not found")

    @mock.patch('testrail.api.requests.get')
    def test_set_project_empty_project(self, mock_get):
        mock_response = mock.Mock()
        mock_response.json.return_value = copy.deepcopy(self.mock_project_data)
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        with self.assertRaises(TestRailError) as e:
            self.milestone.project = Project()
        self.assertEqual(str(e.exception),
                         "Project ID 'None' was not found")

    def test_get_url_type(self):
        self.assertEqual(type(self.milestone.url), str)

    def test_get_url(self):
        self.assertEqual(self.milestone.url,
                         'http://<server>/index.php?/milestones/view/1')

    def test_raw_data(self):
        self.assertEqual(self.milestone.raw_data(), self.mock_milestone_data)
