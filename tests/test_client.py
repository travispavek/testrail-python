try:
    import unittest2 as unittest
except ImportError:
    import unittest

import mock

from testrail.project import Project
from testrail.run import RunContainer, Run
import testrail


class TestProject(unittest.TestCase):
    def setUp(self):
        self.client = testrail.TestRail(1)
        self.mock_project_data = [
            {
                "announcement": "..",
                "completed_on": "1453504099",
                "id": 1,
                "is_completed": True,
                "name": "Project1",
                "show_announcement": True,
                "url": "http://<server>/index.php?/projects/overview/1"
            },
            {
                "announcement": "..",
                "completed_on": None,
                "id": 2,
                "is_completed": False,
                "name": "Project2",
                "show_announcement": True,
                "url": "http://<server>/index.php?/projects/overview/2"
            }
        ]

        self.mock_runs_data = [
	    {
                'assignedto_id': None,
                'blocked_count': 0,
                'completed_on': None,
                'config': None,
                'config_ids': [],
                'created_by': 2,
                'created_on': 1457761236,
                'custom_status1_count': 0,
                'description': None,
                'failed_count': 0,
                'id': 111,
                'include_all': True,
                'is_completed': False,
                'milestone_id': None,
                'name': 'Test Run Mock',
                'passed_count': 0,
                'plan_id': None,
                'project_id': 1,
                'retest_count': 0,
                'suite_id': 1,
                'untested_count': 3,
                'url': 'https://<server>/index.php?/runs/view/111'
            },
	    {
                'assignedto_id': None,
                'blocked_count': 0,
                'completed_on': None,
                'config': None,
                'config_ids': [],
                'created_by': 2,
                'created_on': 1457761237,
                'custom_status1_count': 0,
                'description': None,
                'failed_count': 0,
                'id': 222,
                'include_all': True,
                'is_completed': True,
                'milestone_id': None,
                'name': 'Test Run Mock',
                'passed_count': 0,
                'plan_id': None,
                'project_id': 1,
                'retest_count': 0,
                'suite_id': 1,
                'untested_count': 3,
                'url': 'https://<server>/index.php?/runs/view/222'
            },
        ]

    def tearDown(self):
            pass

    @mock.patch('testrail.api.requests.get')
    def test_get_projects(self, mock_get):
        mock_response = mock.Mock()
        mock_response.json.return_value = self.mock_project_data
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        projects = self.client.projects()
        self.assertEqual(len(projects), 2)
        for project in projects:
            assert isinstance(project, Project)

    @mock.patch('testrail.api.requests.get')
    def test_get_runs_returns_runcontainer(self, mock_get):
        mock_response = mock.Mock()
        mock_response.json.return_value = self.mock_runs_data
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        runs = self.client.runs()
        assert isinstance(runs, RunContainer)
        self.assertEqual(len(runs), 2)

    @mock.patch('testrail.api.requests.get')
    def test_runcontainer_contains_only_run_objects(self, mock_get):
        mock_response = mock.Mock()
        mock_response.json.return_value = self.mock_runs_data
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        runs = self.client.runs()
        self.assertTrue(all([isinstance(r, Run) for r in runs]))

    @mock.patch('testrail.api.requests.get')
    def test_runcontainer_active_runs(self, mock_get):
        mock_response = mock.Mock()
        mock_response.json.return_value = self.mock_runs_data
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        active_runs = list(self.client.runs().active())
        self.assertEqual(len(active_runs), 1)
        self.assertEqual(active_runs[0].id, 111)

    @mock.patch('testrail.api.requests.get')
    def test_runcontainer_completed_runs(self, mock_get):
        mock_response = mock.Mock()
        mock_response.json.return_value = self.mock_runs_data
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        completed_runs = list(self.client.runs().completed())
        self.assertEqual(len(completed_runs), 1)
        self.assertEqual(completed_runs[0].id, 222)

    @mock.patch('testrail.api.requests.get')
    def test_runcontainer_latest_runs(self, mock_get):
        mock_response = mock.Mock()
        mock_response.json.return_value = self.mock_runs_data
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        latest_run = self.client.runs().latest()
        self.assertEqual(latest_run.id, 222)

    @mock.patch('testrail.api.requests.get')
    def test_runcontainer_oldest_runs(self, mock_get):
        mock_response = mock.Mock()
        mock_response.json.return_value = self.mock_runs_data
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        oldest_run = self.client.runs().oldest()
        self.assertEqual(oldest_run.id, 111)
