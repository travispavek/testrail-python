import unittest
from datetime import datetime

import mock

from testrail.project import Project, ProjectContainer
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

    def tearDown(self):
            pass

    @mock.patch('testrail.api.requests.get')
    def test_get_projects(self, mock_get):
        mock_response = mock.Mock()
        url = 'https://<server>/index.php?/api/v2/get_projects'
        mock_response.json.return_value = self.mock_project_data
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        projects = self.client.projects()
        self.assertEqual(len(projects), 2)
        for project in projects:
            assert isinstance(project, Project)

    def test_project_announcement(self):
        project = Project(self.mock_project_data[0])
        self.assertEqual(project.announcement, '..')

    def test_project_completed_on(self):
        project = Project(self.mock_project_data[0])
        timestamp = datetime.fromtimestamp(1453504099)
        self.assertEqual(project.completed_on, timestamp)
