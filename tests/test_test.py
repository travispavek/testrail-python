import mock
import datetime
try:
    import unittest2 as unittest
except ImportError:
    import unittest

from testrail.api import API
from testrail.run import Run
from testrail.case import Case
from testrail.test import Test
from testrail.user import User
from testrail.status import Status
from testrail.milestone import Milestone
from testrail.suite import Suite


class TestTest(unittest.TestCase):
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
        ]

        self.mock_status_data = [
            {
                "color_bright": 13684944,
                "color_dark": 0,
                "color_medium": 10526880,
                "id": 5,
                "is_final": False,
                "is_system": True,
                "is_untested": False,
                "label": "Mock Custom",
                "name": "mock_custom_status1"
            },
        ]

        self.mock_user_data = [
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

        self.mock_case_data = [
            {
                "created_by": 5,
                "created_on": 1392300984,
                'estimate': '1w 3d 6h 2m 30s',
                "estimate_forecast": None,
                "id": 8,
                "milestone_id": 9,
                "priority_id": 2,
                "refs": "RF-1, RF-2",
                "section_id": 1,
                "suite_id": 1,
                "title": "Change document attributes (author, title, organization)",
                "type_id": 4,
                "updated_by": 6,
                "updated_on": 1393586511
            },
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

        self.mock_test_data = [
            {
                "assignedto_id": 5,
                "case_id": 8,
                'estimate': '1w 1d 1h 1m 1s',
                "estimate_forecast": '2w 2d 2h 2m 2s',
                "id": 100,
                "milestone_id": 9,
                "priority_id": 2,
                "refs": "REF1,REF2,REF3",
                "run_id": 81,
                "status_id": 5,
                "title": "Mock Test Title 1",
                "type_id": 4
            },
            {
                "assignedto_id": 5,
                "case_id": 8,
                'estimate': None,
                "estimate_forecast": None,
                "id": 200,
                "milestone_id": None,
                "priority_id": 2,
                "run_id": 1,
                "status_id": 5,
                "title": "Mock Test Title 2",
                "type_id": 4
            },
        ]

        self.test = Test(self.mock_test_data[0])
        self.test2 = Test(self.mock_test_data[1])

    @mock.patch('testrail.api.API._refresh')
    @mock.patch('testrail.api.requests.get')
    def test_get_test_assigned_to_type(self, mock_get, refresh_mock):
        refresh_mock.return_value = True
        mock_response = mock.Mock()
        mock_response.json.return_value = self.mock_user_data
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        self.assertTrue(isinstance(self.test.assigned_to, User))

    @mock.patch('testrail.api.API._refresh')
    @mock.patch('testrail.api.requests.get')
    def test_get_test_assigned_to(self, mock_get, refresh_mock):
        refresh_mock.return_value = True
        mock_response = mock.Mock()
        mock_response.json.return_value = self.mock_user_data
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        self.assertEqual(self.test.assigned_to.id, 5)

    @mock.patch('testrail.test.Test.run')
    @mock.patch('testrail.api.API._refresh')
    @mock.patch('testrail.api.requests.get')
    def test_get_test_case_type(self, mock_get, refresh_mock, _):
        refresh_mock.return_value = True
        mock_response = mock.Mock()
        mock_response.json.return_value = self.mock_case_data
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        self.assertTrue(isinstance(self.test.case, Case))

    @mock.patch('testrail.test.Test.run')
    @mock.patch('testrail.api.API._refresh')
    @mock.patch('testrail.api.requests.get')
    def test_get_test_case(self, mock_get, refresh_mock, _):
        refresh_mock.return_value = True
        mock_response = mock.Mock()
        mock_response.json.return_value = self.mock_case_data
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        self.assertEqual(self.test.case.id, 8)

    def test_get_test_estimate_type(self):
        self.assertTrue(isinstance(self.test.estimate, datetime.timedelta))

    def test_get_test_estimate_null(self):
        self.assertEqual(self.test2.estimate, None)

    def test_get_test_estimate(self):
        expected_timedelta = datetime.timedelta(
            weeks=1, days=1, hours=1, minutes=1, seconds=1)

        self.assertEqual(self.test.estimate, expected_timedelta)

    def test_get_test_estimate_forecast_type(self):
        self.assertTrue(isinstance(self.test.estimate_forecast, datetime.timedelta))

    def test_get_test_estimate_forecast_null(self):
        self.assertEqual(self.test2.estimate_forecast, None)

    def test_get_test_estimate_forecast(self):
        expected_timedelta = datetime.timedelta(
            weeks=2, days=2, hours=2, minutes=2, seconds=2)

        self.assertEqual(self.test.estimate_forecast, expected_timedelta)

    def test_get_test_id_type(self):
        self.assertTrue(isinstance(self.test.id, int))

    def test_get_test_id(self):
        self.assertEqual(self.test.id, 100)

    @mock.patch('testrail.api.API._refresh')
    @mock.patch('testrail.api.requests.get')
    def test_get_test_milestone_type(self, mock_get, refresh_mock):
        refresh_mock.return_value = True
        mock_response = mock.Mock()
        mock_response.json.return_value = self.mock_mstone_data[0]
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        self.assertTrue(isinstance(self.test.milestone, Milestone))

    def test_get_test_milestone_is_null(self):
        self.assertEqual(self.test2.milestone, None)

    @mock.patch('testrail.api.API._refresh')
    @mock.patch('testrail.api.requests.get')
    def test_get_test_milestone(self, mock_get, refresh_mock):
        refresh_mock.return_value = True
        mock_response = mock.Mock()
        mock_response.json.return_value = self.mock_mstone_data[0]
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        self.assertEqual(self.test.milestone.id, 9)

    def test_get_test_refs_type(self):
        self.assertTrue(isinstance(self.test.refs, str))

    def test_get_test_refs_is_null(self):
        self.assertEqual(self.test2.refs, None)

    def test_get_test_refs(self):
        self.assertIn("REF1", self.test.refs)

    @mock.patch('testrail.api.API._refresh')
    @mock.patch('testrail.api.requests.get')
    def test_get_test_run_type(self, mock_get, refresh_mock):
        refresh_mock.return_value = True
        mock_response = mock.Mock()
        mock_response.json.return_value = self.mock_run_data
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        self.assertTrue(isinstance(self.test.run, Run))

    @mock.patch('testrail.api.API._refresh')
    @mock.patch('testrail.api.requests.get')
    def test_get_test_run(self, mock_get, refresh_mock):
        refresh_mock.return_value = True
        mock_response = mock.Mock()
        mock_response.json.return_value = self.mock_run_data
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        self.assertEqual(self.test.run.id, 81)

    @mock.patch('testrail.api.API._refresh')
    @mock.patch('testrail.api.requests.get')
    def test_get_test_status_type(self, mock_get, refresh_mock):
        refresh_mock.return_value = True
        mock_response = mock.Mock()
        mock_response.json.return_value = self.mock_status_data
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        self.assertTrue(isinstance(self.test.status, Status))

    @mock.patch('testrail.api.API._refresh')
    @mock.patch('testrail.api.requests.get')
    def test_get_test_status(self, mock_get, refresh_mock):
        refresh_mock.return_value = True
        mock_response = mock.Mock()
        mock_response.json.return_value = self.mock_status_data
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        self.assertEqual(self.test.status.id, 5)

    def test_get_test_title_type(self):
        self.assertTrue(isinstance(self.test.title, str))

    def test_get_test_refs(self):
        self.assertIn("Mock Test Title 1", self.test.title)

    def test_get_raw_data_type(self):
        self.assertTrue(isinstance(self.test.raw_data(), dict))

    def test_raw_data(self):
        self.assertEqual(self.test.raw_data(), self.mock_test_data[0])
