import copy
import mock
import datetime
try:
    import unittest2 as unittest
except ImportError:
    import unittest

from testrail.api import API
from testrail.run import Run
from testrail.user import User
from testrail.plan import Plan
from testrail.entry import Entry
from testrail.project import Project
from testrail.milestone import Milestone
from testrail.helper import TestRailError


class TestPlan(unittest.TestCase):
    def setUp(self):
        API.flush_cache()

        self.mock_run_data = [
            {
                "assignedto_id": 6,
                "blocked_count": 1,
                "completed_on": None,
                "config": "Mock Config",
                "config_ids": [
                    2,
                    6
                ],
                "created_by": 5,
                "created_on": 1393845644,
                "custom_status1_count": 0,
                "custom_status2_count": 0,
                "custom_status3_count": 0,
                "custom_status4_count": 0,
                "custom_status5_count": 0,
                "custom_status6_count": 0,
                "custom_status7_count": 0,
                "description": "Mock description",
                "failed_count": 2,
                "id": 81,
                "include_all": False,
                "is_completed": False,
                "milestone_id": 9,
                "name": "Mock Name",
                "passed_count": 3,
                "plan_id": 80,
                "project_id": 1,
                "retest_count": 7,
                "suite_id": 4,
                "untested_count": 17,
                "url": "http://mock_server/testrail/index.php?/runs/view/81"
            },
            {
                "assignedto_id": 7,
                "blocked_count": 1,
                "completed_on": 100000,
                "config": "Mock Config",
                "config_ids": [
                    2,
                    6
                ],
                "created_by": 1,
                "created_on": None,
                "custom_status1_count": 0,
                "custom_status2_count": 0,
                "custom_status3_count": 0,
                "custom_status4_count": 0,
                "custom_status5_count": 0,
                "custom_status6_count": 0,
                "custom_status7_count": 0,
                "description": None,
                "failed_count": 2,
                "id": 81,
                "include_all": False,
                "is_completed": False,
                "milestone_id": 7,
                "name": "Mock Name",
                "passed_count": 2,
                "plan_id": 80,
                "project_id": 1,
                "retest_count": 1,
                "suite_id": 4,
                "untested_count": 3,
                "url": "http://mock_server/testrail/index.php?/runs/view/81"
            }
        ]

        self.mock_entries = [
            {
                "id": "mock-id-1",
                "name": "Mock entry",
                "runs": self.mock_run_data,
                "suite_id": 4
            },
            {
                "id": "mock-id-2",
                "name": "Mock entry 2",
                "runs": self.mock_run_data,
                "suite_id": 4
            }
        ]

        self.mock_entries2 = copy.deepcopy(self.mock_entries)
        self.mock_entries2[0]['id'] = "new-mock-id-1"
        self.mock_entries2[1]['id'] = "new-mock-id-1"

        mock_plan1 = {
            "assignedto_id": 6,
            "blocked_count": 2,
            "completed_on": None,
            "created_by": 6,
            "created_on": None,
            "custom_status1_count": 0,
            "custom_status2_count": 0,
            "custom_status3_count": 0,
            "custom_status4_count": 0,
            "custom_status5_count": 0,
            "custom_status6_count": 0,
            "custom_status7_count": 0,
            "description": "Mock plan description",
            "entries": self.mock_entries,
            "failed_count": 4,
            "id": 88,
            "is_completed": False,
            "milestone_id": 7,
            "name": "Mock Plan Name",
            "passed_count": 5,
            "project_id": 1,
            "retest_count": 20,
            "untested_count": 63,
            "url": "http://<server>/testrail/index.php?/plans/view/80"
        }

        mock_plan2 = copy.deepcopy(mock_plan1)
        mock_plan2.update({
            'completed_on': 20000,
            "created_on": 30000,
            'entries': list(),
            'id': 999,
            "milestone_id": None,
        })
        self.mock_plan_data = [mock_plan1, mock_plan2]

        self.mock_users = [
            {
                "email": "mock1@email.com",
                "id": 5,
                "is_active": True,
                "name": "Mock Name 1"
            },
            {
                "email": "mock2@email.com",
                "id": 6,
                "is_active": True,
                "name": "Mock Name 2"
            }
        ]

        self.mock_mstone_data = [
            {
                "completed_on": 1389968888,
                "description": "Mock milestone1 description",
                "due_on": 1391968184,
                "id": 9,
                "is_completed": True,
                "name": "Release 1.5",
                "project_id": 1,
                "url": "http://<server>/testrail/index.php?/milestones/view/1"
            },
            {
                "completed_on": 1389969999,
                "description": "Mock milestone2 description",
                "due_on": 1391968184,
                "id": 7,
                "is_completed": False,
                "name": "Release 1.5",
                "project_id": 1,
                "url": "http://<server>/testrail/index.php?/milestones/view/1"
            }

        ]

        self.mock_project_data = [{"id": 1, }, {"id": 99, }]

        self.plan = Plan(self.mock_plan_data[0])
        self.plan2 = Plan(self.mock_plan_data[1])

    @mock.patch('testrail.api.requests.get')
    def test_get_plan_assigned_to_type(self, mock_get):
        mock_response = mock.Mock()
        mock_response.json.return_value = copy.deepcopy(self.mock_users)
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        self.assertTrue(isinstance(self.plan.assigned_to, User))

    @mock.patch('testrail.api.requests.get')
    def test_run_assigned_to(self, mock_get):
        mock_response = mock.Mock()
        mock_response.json.return_value = copy.deepcopy(self.mock_users)
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        self.assertEqual(self.plan.assigned_to.id, 6)

    def test_get_blocked_count_type(self):
        self.assertTrue(isinstance(self.plan.blocked_count, int))

    def test_get_blocked_count(self):
        self.assertEqual(self.plan.blocked_count, 2)

    def test_get_completed_on_no_ts_type(self):
        self.assertEqual(self.plan.completed_on, None)

    def test_get_completed_on_with_ts_type(self):
        self.assertTrue(isinstance(self.plan2.completed_on, datetime.datetime))

    def test_get_completed_on_with_ts(self):
        self.assertEqual(
            self.plan2.completed_on, datetime.datetime.fromtimestamp(20000))

    def test_get_created_on_no_ts_type(self):
        self.assertEqual(self.plan.created_on, None)

    def test_get_created_on_with_ts_type(self):
        self.assertTrue(isinstance(self.plan2.created_on, datetime.datetime))

    def test_get_created_on_with_ts(self):
        self.assertEqual(
            self.plan2.created_on, datetime.datetime.fromtimestamp(30000))

    @mock.patch('testrail.api.requests.get')
    def test_get_created_by_type(self, mock_get):
        mock_response = mock.Mock()
        mock_response.json.return_value = copy.deepcopy(self.mock_users)
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        self.assertTrue(isinstance(self.plan.created_by, User))

    @mock.patch('testrail.api.requests.get')
    def test_created_by(self, mock_get2):
        mock_response = mock.Mock()
        mock_response.json.return_value = copy.deepcopy(self.mock_users)
        mock_response.status_code = 200
        mock_get2.return_value = mock_response
        self.assertEqual(self.plan.created_by.id, 6)

    def test_get_description_type(self):
        self.assertTrue(isinstance(self.plan.description, str))

    def test_description(self):
        self.assertEqual(self.plan.description, "Mock plan description")

    def test_set_description(self):
        self.plan.description = "New plan description"
        self.assertEqual(self.plan.description, "New plan description")

    def test_set_description_invalid_type(self):
        with self.assertRaises(TestRailError) as e:
            self.plan.description = 194
        self.assertEqual(str(e.exception), 'input must be a string')

    def test_get_entries_type(self):
        self.assertTrue(
            all([lambda e: isinstance(e, Entry) for e in self.plan.entries]))

    def test_get_entries_type(self):
        def entry_checker(e):
            return e.id.startswith("mock-id")
        self.assertTrue(all([entry_checker(e) for e in self.plan.entries]))
    """
    @mock.patch('testrail.api.requests.get')
    def test_get_entries_if_none(self, mock_get):
        mock_response = mock.Mock()
        mock_response.json.return_value = copy.deepcopy(self.mock_plan_data)
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        self.assertTrue(
            all([lambda e: isinstance(e, Entry) for e in self.plan2.entries]))
    """

    def test_get_failed_count_type(self):
        self.assertTrue(isinstance(self.plan.failed_count, int))

    def test_failed_count(self):
        self.assertEqual(self.plan.failed_count, 4)

    def test_get_id_type(self):
        self.assertTrue(isinstance(self.plan.id, int))

    def test_get_id(self):
        self.assertEqual(self.plan.id, 88)

    def test_get_is_completed_type(self):
        self.assertTrue(isinstance(self.plan.is_completed, bool))

    def test_is_completed(self):
        self.assertEqual(self.plan.is_completed, False)

    @mock.patch('testrail.api.requests.get')
    def test_no_milestone(self, mock_get):
        mock_response = mock.Mock()
        mock_response.json.return_value = copy.deepcopy(self.mock_mstone_data)
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        self.assertEqual(self.plan2.milestone.id, None)
        self.assertEqual(type(self.plan2.milestone), Milestone)

    @mock.patch('testrail.api.requests.get')
    def test_get_milestone_type(self, mock_get):
        mock_response = mock.Mock()
        mock_response.json.return_value = copy.deepcopy(self.mock_mstone_data)
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        self.assertTrue(isinstance(self.plan.milestone, Milestone))

    @mock.patch('testrail.api.requests.get')
    def test_milestone(self, mock_get):
        mock_response = mock.Mock()
        mock_response.json.return_value = copy.deepcopy(self.mock_mstone_data)
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        self.assertEqual(self.plan.milestone.id, 7)

    def test_get_name_type(self):
        self.assertTrue(isinstance(self.plan.name, str))

    def test_get_name(self):
        self.assertEqual(self.plan.name, "Mock Plan Name")

    def test_set_name(self):
        name = "Mock New Name"
        self.plan.name = name
        self.assertEqual(self.plan.name, name)

    def test_set_name_invalid_type(self):
        with self.assertRaises(TestRailError) as e:
            self.plan.name = 394
        self.assertEqual(str(e.exception), 'input must be a string')

    def test_get_passed_count_type(self):
        self.assertTrue(isinstance(self.plan.passed_count, int))

    def test_passed_count(self):
        self.assertEqual(self.plan.passed_count, 5)

    @mock.patch('testrail.api.requests.get')
    def test_get_project_type(self, mock_get):
        mock_response = mock.Mock()
        mock_response.json.return_value = copy.deepcopy(self.mock_project_data)
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        self.assertTrue(isinstance(self.plan.project, Project))

    @mock.patch('testrail.api.requests.get')
    def test_project(self, mock_get):
        mock_response = mock.Mock()
        mock_response.json.return_value = copy.deepcopy(self.mock_project_data)
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        self.assertEqual(self.plan.project.id, 1)

    @mock.patch('testrail.api.requests.get')
    def test_set_project(self, mock_get):
        mock_response = mock.Mock()
        mock_response.json.return_value = copy.deepcopy(self.mock_project_data)
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        project = Project(self.mock_project_data[1])
        self.plan.project = project
        self.assertEqual(self.plan.project.id, 99)

    def test_set_project_invalid_type(self):
        with self.assertRaises(TestRailError) as e:
            self.plan.project = 394
        self.assertEqual(str(e.exception), 'input must be a Project')

    @mock.patch('testrail.api.requests.get')
    def test_set_milestone(self, mock_get):
        mock_response = mock.Mock()
        mock_response.json.return_value = copy.deepcopy(self.mock_project_data)
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        milestone = Milestone(self.mock_mstone_data[1])
        self.plan.milestone = milestone
        self.assertEqual(self.plan._content['milestone_id'], 7)

    def test_set_milestone_invalid_type(self):
        with self.assertRaises(TestRailError) as e:
            self.plan.milestone = 994
        self.assertEqual(str(e.exception), 'input must be a Milestone')

    def test_get_project_id_type(self):
        self.assertTrue(isinstance(self.plan.project_id, int))

    def test_project_id(self):
        self.assertEqual(self.plan.project_id, 1)

    def test_get_retest_count_type(self):
        self.assertTrue(isinstance(self.plan.retest_count, int))

    def test_retest_count(self):
        self.assertEqual(self.plan.retest_count, 20)

    def test_get_untested_count_type(self):
        self.assertTrue(isinstance(self.plan.untested_count, int))

    def test_untested_count(self):
        self.assertEqual(self.plan.untested_count, 63)

    def test_get_url_type(self):
        self.assertTrue(isinstance(self.plan.url, str))

    def test_url(self):
        self.assertTrue(self.plan.url.startswith("http://"))

    def test_get_raw_data_type(self):
        self.assertTrue(isinstance(self.plan.raw_data(), dict))

    def test_raw_data(self):
        self.assertEqual(self.plan.raw_data(), self.mock_plan_data[0])
