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
from testrail.project import Project
from testrail.milestone import Milestone
from testrail.helper import TestRailError


class TestRun(unittest.TestCase):
    def setUp(self):
        self.mock_run_data = [
            {
                "assignedto_id": 6,
                "blocked_count": 1,
                "case_ids": [
                    8,
                    9
                ],
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

        self.mock_run_user = [
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
                "completed_on": 1389968184,
                "description": "Mock milestone description",
                "due_on": 1391968184,
                "id": 9,
                "is_completed": True,
                "name": "Release 1.5",
                "project_id": 1,
                "url": "http://<server>/testrail/index.php?/milestones/view/1"
            }
                
        ]

        self.mock_plan_data = [{"id": 80, }, ]
        self.mock_project_data = [{"id": 1, }, {"id": 99, }]

        self.run = Run(self.mock_run_data[0])
        self.run2 = Run(self.mock_run_data[1])

    @mock.patch('testrail.api.API._refresh')
    @mock.patch('testrail.api.requests.get')
    def test_get_run_assigned_to_type(self, mock_get, refresh_mock):
        refresh_mock.return_value = True
        mock_response = mock.Mock()
        mock_response.json.return_value = copy.deepcopy(self.mock_run_user)
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        self.assertTrue(isinstance(self.run.assigned_to, User))

    @mock.patch('testrail.api.API._refresh')
    @mock.patch('testrail.api.requests.get')
    def test_run_assigned_to(self, mock_get, refresh_mock):
        refresh_mock.return_value = True
        mock_response = mock.Mock()
        mock_response.json.return_value = copy.deepcopy(self.mock_run_user)
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        self.assertEqual(self.run.assigned_to.id, 6)

    def test_get_blocked_count_type(self):
        self.assertTrue(isinstance(self.run.blocked_count, int))

    def test_get_blocked_count(self):
        self.assertEqual(self.run.blocked_count, 1)

    def test_get_case_ids_container_type(self):
        self.assertTrue(isinstance(self.run.case_ids, list))

    def test_get_case_ids_type(self):
        int_check = lambda val: isinstance(val, int)
        self.assertTrue(all(map(int_check, self.run.case_ids)))

    def test_set_case_ids(self):
        new_case_ids = [10, 11]
        self.run.case_ids = new_case_ids
        self.assertEqual(self.run.case_ids, new_case_ids)

    def test_set_case_ids_to_none(self):
        new_case_ids = None
        self.run.case_ids = new_case_ids
        self.assertEqual(self.run.case_ids, new_case_ids)

    def test_set_case_ids_invalid_container_type(self):
        with self.assertRaises(TestRailError) as e:
            self.run.case_ids = "asdf"
        self.assertEqual(str(e.exception), 'case_ids must be an iterable of integers')

    def test_set_case_ids_invalid_value_type(self):
        with self.assertRaises(TestRailError) as e:
            self.run.case_ids = [1, 2, 'gg']
        self.assertEqual(str(e.exception), 'case_ids must be an iterable of integers')

    def test_get_completed_on_no_ts_type(self):
        self.assertEqual(self.run.completed_on, None)

    def test_get_completed_on_with_ts_type(self):
        self.assertTrue(isinstance(self.run2.completed_on, datetime.datetime))

    def test_get_completed_on_with_ts(self):
        self.assertEqual(
            self.run2.completed_on, datetime.datetime.fromtimestamp(100000))

    def test_get_config_type(self):
        self.assertTrue(isinstance(self.run.config, str))

    def test_get_config(self):
        self.assertEqual(self.run.config, "Mock Config")

    def test_get_config_ids_type(self):
        self.assertTrue(isinstance(self.run.config_ids, list))

    def test_get_config_ids(self):
        self.assertEqual(self.run.config_ids, [2, 6])

    def test_get_created_on_no_ts_type(self):
        self.assertEqual(self.run2.created_on, None)

    def test_get_created_on_with_ts_type(self):
        self.assertTrue(isinstance(self.run.created_on, datetime.datetime))

    def test_get_created_on_with_ts(self):
        self.assertEqual(
            self.run.created_on, datetime.datetime.fromtimestamp(1393845644))

    @mock.patch('testrail.api.API._refresh')
    @mock.patch('testrail.api.requests.get')
    def test_get_created_by_type(self, mock_get, refresh_mock):
        refresh_mock.return_value = True
        mock_response = mock.Mock()
        mock_response.json.return_value = copy.deepcopy(self.mock_run_user)
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        self.assertTrue(isinstance(self.run.created_by, User))

    @mock.patch('testrail.api.API._refresh')
    @mock.patch('testrail.api.requests.get')
    def test_created_by(self, mock_get2, refresh_mock):
        refresh_mock.return_value = True
        mock_response = mock.Mock()
        mock_response.json.return_value = copy.deepcopy(self.mock_run_user)
        mock_response.status_code = 200
        mock_get2.return_value = mock_response
        self.assertEqual(self.run.created_by.id, 5)

    def test_get_description_type(self):
        self.assertTrue(isinstance(self.run.description, str))

    def test_description(self):
        self.assertEqual(self.run.description, "Mock description")

    def test_get_failed_count_type(self):
        self.assertTrue(isinstance(self.run.failed_count, int))

    def test_failed_count(self):
        self.assertEqual(self.run.failed_count, 2)

    def test_get_id_type(self):
        self.assertTrue(isinstance(self.run.id, int))

    def test_get_id(self):
        self.assertEqual(self.run.id, 81)

    def test_get_include_all_type(self):
        self.assertTrue(isinstance(self.run.include_all, bool))

    def test_get_include_all(self):
        self.assertEqual(self.run.include_all, False)

    def test_set_include_all(self):
        self.run.include_all = True
        self.assertTrue(self.run.include_all)

    def test_set_include_all_invalid_type(self):
        with self.assertRaises(TestRailError) as e:
            self.run.include_all = "asdf"
        self.assertEqual(str(e.exception), 'include_all must be a boolean')

    def test_get_is_completed_type(self):
        self.assertTrue(isinstance(self.run.is_completed, bool))

    def test_is_completed(self):
        self.assertEqual(self.run.is_completed, False)

    @mock.patch('testrail.api.API._refresh')
    @mock.patch('testrail.api.requests.get')
    def test_get_milestone_type(self, mock_get, refresh_mock):
        refresh_mock.return_value = True
        mock_response = mock.Mock()
        mock_response.json.return_value = copy.deepcopy(self.mock_mstone_data)
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        self.assertTrue(isinstance(self.run.milestone, Milestone))

    @mock.patch('testrail.api.API._refresh')
    @mock.patch('testrail.api.requests.get')
    def test_milestone(self, mock_get, refresh_mock):
        refresh_mock.return_value = True
        mock_response = mock.Mock()
        mock_response.json.return_value = copy.deepcopy(self.mock_mstone_data)
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        self.assertEqual(self.run.milestone.id, 9)

    @mock.patch('testrail.api.API._refresh')
    @mock.patch('testrail.api.requests.get')
    def test_get_plan_type(self, mock_get, refresh_mock):
        refresh_mock.return_value = True
        mock_response = mock.Mock()
        mock_response.json.return_value = copy.deepcopy(self.mock_plan_data)
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        self.assertTrue(isinstance(self.run.plan, Plan))

    @mock.patch('testrail.api.API._refresh')
    @mock.patch('testrail.api.requests.get')
    def test_plan(self, mock_get, refresh_mock):
        refresh_mock.return_value = True
        mock_response = mock.Mock()
        mock_response.json.return_value = copy.deepcopy(self.mock_plan_data)
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        self.assertEqual(self.run.plan.id, 80)

    def test_get_name_type(self):
        self.assertTrue(isinstance(self.run.name, str))

    def test_get_name(self):
        self.assertEqual(self.run.name, "Mock Name")

    def test_set_name(self):
        name = "Mock New Name"
        self.run.name = name
        self.assertEqual(self.run.name, name)

    def test_set_name_invalid_type(self):
        with self.assertRaises(TestRailError) as e:
            self.run.name = 394
        self.assertEqual(str(e.exception), 'input must be a string')

    def test_get_passed_count_type(self):
        self.assertTrue(isinstance(self.run.passed_count, int))

    def test_passed_count(self):
        self.assertEqual(self.run.passed_count, 3)

    @mock.patch('testrail.api.API._refresh')
    @mock.patch('testrail.api.requests.get')
    def test_get_project_type(self, mock_get, refresh_mock):
        refresh_mock.return_value = True
        mock_response = mock.Mock()
        mock_response.json.return_value = copy.deepcopy(self.mock_project_data)
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        self.assertTrue(isinstance(self.run.project, Project))

    @mock.patch('testrail.api.API._refresh')
    @mock.patch('testrail.api.requests.get')
    def test_project(self, mock_get, refresh_mock):
        refresh_mock.return_value = True
        mock_response = mock.Mock()
        mock_response.json.return_value = copy.deepcopy(self.mock_project_data)
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        self.assertEqual(self.run.project.id, 1)

    @mock.patch('testrail.api.API._refresh')
    @mock.patch('testrail.api.requests.get')
    def test_set_project(self, mock_get, refresh_mock):
        refresh_mock.return_value = True
        mock_response = mock.Mock()
        mock_response.json.return_value = copy.deepcopy(self.mock_project_data)
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        project = Project(self.mock_project_data[1])
        self.run.project = project
        self.assertEqual(self.run.project.id, 99)

    def test_set_project_invalid_type(self):
        with self.assertRaises(TestRailError) as e:
            self.run.project = 394
        self.assertEqual(str(e.exception), 'input must be a Project')

    def test_get_project_id_type(self):
        self.assertTrue(isinstance(self.run.project_id, int))

    def test_project_id(self):
        self.assertEqual(self.run.project_id, 1)

    def test_get_retest_count_type(self):
        self.assertTrue(isinstance(self.run.retest_count, int))

    def test_retest_count(self):
        self.assertEqual(self.run.retest_count, 7)

    def test_get_untested_count_type(self):
        self.assertTrue(isinstance(self.run.untested_count, int))

    def test_untested_count(self):
        self.assertEqual(self.run.untested_count, 17)

    def test_get_url_type(self):
        self.assertTrue(isinstance(self.run.url, str))

    def test_url(self):
        self.assertTrue(self.run.url.startswith("http://"))

    def test_get_raw_data_type(self):
        self.assertTrue(isinstance(self.run.raw_data(), dict))

    def test_raw_data(self):
        self.assertEqual(self.run.raw_data(), self.mock_run_data[0])
