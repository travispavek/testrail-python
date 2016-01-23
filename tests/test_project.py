import unittest
from datetime import datetime

from testrail.helper import TestRailError
from testrail.project import Project, ProjectContainer


class TestProject(unittest.TestCase):
    def setUp(self):
        self.mock_data_completed = {
            "announcement": "..",
            "completed_on": "1453504099",
            "id": 1,
            "is_completed": True,
            "name": "Project1",
            "show_announcement": True,
            "url": "http://<server>/index.php?/projects/overview/1",
            "suite_mode": 3
        }

        self.mock_data_incomplete = {
            "announcement": "..",
            "completed_on": None,
            "id": 1,
            "is_completed": False,
            "name": "Project1",
            "show_announcement": True,
            "url": "http://<server>/index.php?/projects/overview/1",
            "suite_mode": 3
        }
        self.project = Project(self.mock_data_completed)

    def test_get_announcement_type(self):
        self.assertEqual(type(self.project.announcement), str)

    def test_get_announcement(self):
        self.assertEqual(self.project.announcement, '..')

    def test_set_announcement(self):
        msg = 'test announcement'
        self.project.announcement = msg
        self.assertEqual(self.project.announcement, msg)

    def test_set_announcement_invalid(self):
        with self.assertRaises(TestRailError) as e:
            self.project.announcement = 23
        self.assertEqual(str(e.exception), 'input must be a string')

    def test_get_completed_on_type(self):
        self.assertEqual(type(self.project.completed_on), datetime)

    def test_get_completed_on(self):
        date_obj = datetime.fromtimestamp(1453504099)
        self.assertEqual(self.project.completed_on, date_obj)

    def test_get_completed_on_not_completed(self):
        project = Project(self.mock_data_incomplete)
        self.assertEqual(project.completed_on, None)

    def test_get_id_type(self):
        self.assertEqual(type(self.project.id), int)

    def test_get_id(self):
        self.assertEqual(self.project.id, 1)

    def test_get_is_completed_type(self):
        self.assertEqual(type(self.project.is_completed), bool)

    def test_get_is_completed(self):
        self.assertEqual(self.project.is_completed, True)

    def test_get_name_type(self):
        self.assertEqual(type(self.project.name), str)

    def test_get_name(self):
        self.assertEqual(self.project.name, 'Project1')

    def test_set_name(self):
        name = 'my new project'
        self.project.name = name
        self.assertEqual(self.project.name, name)
        self.assertEqual(self.project._content['name'], name)

    def test_set_name_invalid(self):
        with self.assertRaises(TestRailError) as e:
            self.project.name = 394
        self.assertEqual(str(e.exception), 'input must be a string')

    def test_get_show_announcement(self):
        self.assertEqual(self.project.show_announcement, True)

    def test_set_show_announcement(self):
        self.project.show_announcement = False
        self.assertEqual(self.project.show_announcement, False)
        self.assertEqual(self.project._content['show_announcement'], False)

    def test_set_show_announcement_invalid(self):
        with self.assertRaises(TestRailError) as e:
            self.project.show_announcement = 1
        self.assertEqual(str(e.exception), 'input must be a boolean')

    def test_get_suite_mode(self):
        self.assertEqual(self.project.suite_mode, 3)

    def test_set_suite_mode(self):
        for i in [1, 2, 3]:
            self.project.suite_mode = i
            self.assertEqual(self.project.suite_mode, i)
            self.assertEqual(self.project._content['suite_mode'], i)

    def test_set_suite_mode_invalid_type(self):
        with self.assertRaises(TestRailError) as e:
            self.project.suite_mode = '2'
        self.assertEqual(str(e.exception), 'input must be an integer')

    def test_suite_mode_invalid_num(self):
        for i in [0, 4]:
            with self.assertRaises(TestRailError) as e:
                self.project.suite_mode = i
            self.assertEqual(str(e.exception), 'input must be a 1, 2, or 3')

    def test_get_url(self):
        self.assertEqual(
            self.project.url, 'http://<server>/index.php?/projects/overview/1')

class TestProjectContainer(unittest.TestCase):
    def setUp(self):
        self.mock_data = [
            {
                "announcement": "..",
                "completed_on": "1453504099",
                "id": 1,
                "is_completed": True,
                "name": "Project1",
                "show_announcement": True,
                "url": "http://<server>/index.php?/projects/overview/1",
                "suite_mode": 3
            },
            {
                "announcement": "..",
                "completed_on": None,
                "id": 2,
                "is_completed": False,
                "name": "Project1",
                "show_announcement": True,
                "url": "http://<server>/index.php?/projects/overview/2",
                "suite_mode": 3
            }
        ]

        ptemp = list()
        for pdata in self.mock_data:
            ptemp.append(Project(pdata))
        self.projects = ProjectContainer(ptemp)

    def test_len(self):
        self.assertEqual(len(self.projects),  2)

    def test_completed(self):
        self.assertEqual(len(self.projects.completed()), 1)
        self.assertEqual(self.projects.completed()[0].id, 1)

    def test_active(self):
        self.assertEqual(len(self.projects.active()), 1)
        self.assertEqual(self.projects.active()[0].id, 2)

    def test_getitem(self):
        self.assertEqual(self.projects[0].id, 1)
