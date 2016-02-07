import copy
import mock
import unittest

from testrail.helper import TestRailError
from testrail.section import Section
from testrail.suite import Suite


class TestSuite(unittest.TestCase):
    def setUp(self):
        self.mock_suite_data = [
            {
                "description": "suite description",
                "id": 1,
                "name": "Setup & Installation",
                "project_id": 1,
                "url": "http://<server>/index.php?/suites/view/1",
                "is_baseline": False,
                "is_completed": True,
                "is_master": True,
                "completed_on": 1453504099
            },
            {
                "description": "suite description 2",
                "id": 2,
                "name": "Setup & Installation",
                "project_id": 1,
                "url": "http://<server>/index.php?/suites/view/1",
                "is_baseline": False,
                "is_completed": False,
                "is_master": True,
                "completed_on": None
            },
        ]
        self.mock_section_data = [
            {
                "depth": 0,
                "description": 'Some description',
                "display_order": 1,
                "id": 1,
                "name": "Prerequisites",
                "parent_id": None,
                "suite_id": 1
            },
            {
                "depth": 1,
                "description": 'some words',
                "display_order": 1,
                "id": 2,
                "name": "Prerequisites2",
                "parent_id": 1,
                "suite_id": 1
            }
        ]

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
        self.section = Section(self.mock_section_data[1])

    def test_get_id_type(self):
        self.assertEqual(type(self.section.id), int)

    def test_get_id(self):
        self.assertEqual(self.section.id, 2)

    def test_get_depth_type(self):
        self.assertEqual(type(self.section.depth), int)

    def test_get_depth(self):
        self.assertEqual(self.section.depth, 1)

    def test_get_display_order_type(self):
        self.assertEqual(type(self.section.display_order), int)

    def test_get_display_order(self):
        self.assertEqual(self.section.display_order, 1)

    def test_get_description_type(self):
        self.assertEqual(type(self.section.description), str)

    def test_get_description(self):
        self.assertEqual(self.section.description, 'some words')

    def test_set_description(self):
        description = 'new description'
        self.section.description = description
        self.assertEqual(self.section.description, description)
        self.assertEqual(self.section._content['description'], description)

    def test_set_description_invalid_type(self):
        with self.assertRaises(TestRailError) as e:
            self.section.description = 394
        self.assertEqual(str(e.exception), 'input must be a string')

    def test_get_name_type(self):
        self.assertEqual(type(self.section.name), str)

    def test_get_name(self):
        self.assertEqual(self.section.name, 'Prerequisites2')

    def test_set_name(self):
        name = 'my new suite'
        self.section.name = name
        self.assertEqual(self.section.name, name)
        self.assertEqual(self.section._content['name'], name)

    def test_set_name_invalid_type(self):
        with self.assertRaises(TestRailError) as e:
            self.section.name = 394
        self.assertEqual(str(e.exception), 'input must be a string')

    def test_raw_data(self):
        self.assertEqual(self.section.raw_data(), self.mock_section_data[1])

    def test_raw_data_type(self):
        self.assertEqual(type(self.section.raw_data()), dict)

    @mock.patch('testrail.api.requests.get')
    def test_get_suite_type(self, mock_get):
        mock_response = mock.Mock()
        mock_response.json.return_value = copy.deepcopy(self.mock_suite_data)
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        self.assertEqual(type(self.section.suite), Suite)

    @mock.patch('testrail.api.requests.get')
    def test_get_suite(self, mock_get):
        mock_response = mock.Mock()
        mock_response.json.return_value = copy.deepcopy(self.mock_suite_data)
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        self.assertEqual(self.section.suite.id, 1)

    @mock.patch('testrail.api.requests.get')
    def test_get_suite_invalid_id(self, mock_get):
        mock_response = mock.Mock()
        mock_response.json.return_value = copy.deepcopy(self.mock_suite_data)
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        self.section._content['suite_id'] = 200
        with self.assertRaises(TestRailError) as e:
            self.section.suite
        self.assertEqual(str(e.exception), "Suite ID '200' was not found")

    @mock.patch('testrail.api.requests.get')
    def test_set_suite(self, mock_get):
        mock_response = mock.Mock()
        mock_response.json.return_value = copy.deepcopy(self.mock_suite_data)
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        self.assertEqual(self.section.suite.id, 1)
        self.section.suite = Suite(self.mock_suite_data[1])
        self.assertEqual(self.section._content['suite_id'], 2)
        self.assertEqual(self.section.suite.id, 2)

    def test_set_suite_invalid_type(self):
        with self.assertRaises(TestRailError) as e:
            self.section.suite = 2
        self.assertEqual(str(e.exception), 'input must be a Suite')

    @mock.patch('testrail.api.requests.get')
    def test_set_suite_invalid_suite(self, mock_get):
        mock_response = mock.Mock()
        mock_response.json.return_value = copy.deepcopy(self.mock_suite_data)
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        suite = Suite()
        suite._content['id'] = 5
        with self.assertRaises(TestRailError) as e:
            self.section.suite = suite
        self.assertEqual(str(e.exception),
                         "Suite ID '5' was not found")

    @mock.patch('testrail.api.requests.get')
    def test_set_suite_empty_suite(self, mock_get):
        mock_response = mock.Mock()
        mock_response.json.return_value = copy.deepcopy(self.mock_suite_data)
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        with self.assertRaises(TestRailError) as e:
            self.section.suite = Suite()
        self.assertEqual(str(e.exception),
                         "Suite ID 'None' was not found")

    @mock.patch('testrail.api.requests.get')
    def test_get_parent_type(self, mock_get):
        mock_response = mock.Mock()
        mock_response.json.return_value = copy.deepcopy(self.mock_section_data)
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        self.assertEqual(type(self.section.parent), Section)

    @mock.patch('testrail.api.requests.get')
    def test_get_parent(self, mock_get):
        mock_response = mock.Mock()
        mock_response.json.return_value = copy.deepcopy(self.mock_section_data)
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        self.assertEqual(self.section.parent.id, 1)

    @mock.patch('testrail.api.requests.get')
    def test_get_parent_invalid_id(self, mock_get):
        mock_response = mock.Mock()
        mock_response.json.return_value = copy.deepcopy(self.mock_section_data)
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        self.section._content['parent_id'] = 200
        with self.assertRaises(TestRailError) as e:
            self.section.parent
        self.assertEqual(str(e.exception), "Section ID '200' was not found")

    @mock.patch('testrail.api.requests.get')
    def test_set_parent(self, mock_get):
        mock_response = mock.Mock()
        mock_response.json.return_value = copy.deepcopy(self.mock_section_data)
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        self.assertEqual(self.section.parent.id, 1)
        self.section.parent = Section(self.mock_section_data[1])
        self.assertEqual(self.section._content['parent_id'], 2)
        self.assertEqual(self.section.parent.id, 2)

    def test_set_parent_invalid_type(self):
        with self.assertRaises(TestRailError) as e:
            self.section.parent = 2
        self.assertEqual(str(e.exception), 'input must be a Section')

    @mock.patch('testrail.api.requests.get')
    def test_set_parent_invalid_section(self, mock_get):
        mock_response = mock.Mock()
        mock_response.json.return_value = copy.deepcopy(self.mock_section_data)
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        section = Section({})
        section._content['id'] = 5
        with self.assertRaises(TestRailError) as e:
            self.section.parent = section
        self.assertEqual(str(e.exception),
                         "Section ID '5' was not found")

    @mock.patch('testrail.api.requests.get')
    def test_set_parent_empty_section(self, mock_get):
        mock_response = mock.Mock()
        mock_response.json.return_value = copy.deepcopy(self.mock_section_data)
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        with self.assertRaises(TestRailError) as e:
            self.section.parent = Section({})
        self.assertEqual(str(e.exception),
                         "Section ID 'None' was not found")
