from datetime import datetime as dt
try:
    import unittest2 as unittest
except ImportError:
    import unittest

import mock

import testrail
from testrail.api import API
from testrail.user import User
from testrail.project import Project
from testrail.milestone import Milestone
from testrail.helper import TestRailError
from testrail.run import RunContainer, Run
from testrail.plan import PlanContainer, Plan
from testrail.result import ResultContainer, Result


class TestProject(unittest.TestCase):
    def setUp(self):
        API.flush_cache()
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
            }
        ]

        self.mock_plans_data = [
            {
                "assignedto_id": 1,
                "blocked_count": 1,
                "completed_on": None,
                "created_by": 1,
                "created_on": 1457761111,
                "custom_status1_count": 0,
                "custom_status2_count": 0,
                "custom_status3_count": 0,
                "custom_status4_count": 0,
                "custom_status5_count": 0,
                "custom_status6_count": 0,
                "custom_status7_count": 0,
                "description": "Mock plan description",
                "entries": [],
                "failed_count": 1,
                "id": 11,
                "is_completed": True,
                "milestone_id": 1,
                "name": "Mock Plan1 Name",
                "passed_count": 1,
                "project_id": 1,
                "retest_count": 1,
                "untested_count": 1,
                "url": "http://<server>/testrail/index.php?/plans/view/11"
            },
            {
                "assignedto_id": 2,
                "blocked_count": 2,
                "completed_on": None,
                "created_by": 2,
                "created_on": 1457762222,
                "custom_status1_count": 0,
                "custom_status2_count": 0,
                "custom_status3_count": 0,
                "custom_status4_count": 0,
                "custom_status5_count": 0,
                "custom_status6_count": 0,
                "custom_status7_count": 0,
                "description": "Mock plan description",
                "entries": [],
                "failed_count": 2,
                "id": 22,
                "is_completed": False,
                "milestone_id": 2,
                "name": "Mock Plan2 Name",
                "passed_count": 2,
                "project_id": 1,
                "retest_count": 2,
                "untested_count": 2,
                "url": "http://<server>/testrail/index.php?/plans/view/22"
            },
            {
                "assignedto_id": 3,
                "blocked_count": 3,
                "completed_on": None,
                "created_by": 3,
                "created_on": 1457763333,
                "custom_status1_count": 0,
                "custom_status2_count": 0,
                "custom_status3_count": 0,
                "custom_status4_count": 0,
                "custom_status5_count": 0,
                "custom_status6_count": 0,
                "custom_status7_count": 0,
                "description": "Mock plan description",
                "entries": [],
                "failed_count": 3,
                "id": 33,
                "is_completed": False,
                "milestone_id": 3,
                "name": "Mock Plan3 Name",
                "passed_count": 3,
                "project_id": 1,
                "retest_count": 3,
                "untested_count": 3,
                "url": "http://<server>/testrail/index.php?/plans/view/33"
            },
            {
                "assignedto_id": 3,
                "blocked_count": 3,
                "completed_on": None,
                "created_by": 3,
                "created_on": 1457793333,
                "custom_status1_count": 0,
                "custom_status2_count": 0,
                "custom_status3_count": 0,
                "custom_status4_count": 0,
                "custom_status5_count": 0,
                "custom_status6_count": 0,
                "custom_status7_count": 0,
                "description": "Mock plan description",
                "entries": [],
                "failed_count": 3,
                "id": 44,
                "is_completed": False,
                "milestone_id": 1,
                "name": "Mock Plan3 Name",
                "passed_count": 3,
                "project_id": 1,
                "retest_count": 3,
                "untested_count": 3,
                "url": "http://<server>/testrail/index.php?/plans/view/44"
            }
        ]

        self.mock_results_data = [
            {
                "assignedto_id": 2,
                "comment": "This test passed: ..",
                "created_by": 1,
                "created_on": 1393851901,
                "defects": "TR-1",
                "elapsed": "5m",
                "id": 11,
                "status_id": 1,
                "test_id": 111,
                "version": "1.0RC1"
            },
            {
                "assignedto_id": 2,
                "comment": "This test blocked: ..",
                "created_by": 1,
                "created_on": 1393851701,
                "defects": "TR-1",
                "elapsed": "5m",
                "id": 22,
                "status_id": 2,
                "test_id": 222,
                "version": "1.0RC1"
            },
            {
                "assignedto_id": 2,
                "comment": "This test untested: ..",
                "created_by": 1,
                "created_on": 1393851751,
                "defects": "TR-1",
                "elapsed": "5m",
                "id": 33,
                "status_id": 3,
                "test_id": 333,
                "version": "1.0RC1"
            },
            {
                "assignedto_id": 2,
                "comment": "This test is retest ..",
                "created_by": 1,
                "created_on": 1393852041,
                "defects": "TR-1",
                "elapsed": "5m",
                "id": 44,
                "status_id": 4,
                "test_id": 444,
                "version": "1.0RC1"
            },
            {
                "assignedto_id": 2,
                "comment": "This test failed: ..",
                "created_by": 2,
                "created_on": 1393851801,
                "defects": "TR-1",
                "elapsed": "5m",
                "id": 55,
                "status_id": 5,
                "test_id": 555,
                "version": "1.0RC1"
            },
        ]

        self.mock_status_data = [
            {
                'color_bright': 12709313,
                'color_dark': 6667107,
                'color_medium': 9820525,
                'id': 1,
                'is_final': True,
                'is_system': True,
                'is_untested': False,
                'label': 'Passed',
                'name': 'passed'
            },
            {
                'color_bright': 14737632,
                'color_dark': 9474192,
                'color_medium': 13684944,
                'id': 2,
                'is_final': True,
                'is_system': True,
                'is_untested': False,
                'label': 'Blocked',
                'name': 'blocked'
            },
            {
                'color_bright': 15790320,
                'color_dark': 11579568,
                'color_medium': 15395562,
                'id': 3,
                'is_final': False,
                'is_system': True,
                'is_untested': True,
                'label': 'Untested',
                'name': 'untested'
            },
            {
                'color_bright': 16448182,
                'color_dark': 13026868,
                'color_medium': 15593088,
                'id': 4,
                'is_final': False,
                'is_system': True,
                'is_untested': False,
                'label': 'Retest',
                'name': 'retest'
            },
            {
                'color_bright': 16631751,
                'color_dark': 14250867,
                'color_medium': 15829135,
                'id': 5,
                'is_final': True,
                'is_system': True,
                'is_untested': False,
                'label': 'Failed',
                'name': 'failed'},

        ]

        self.mock_users = [
            {
                "email": "mock1@email.com",
                "id": 1,
                "is_active": True,
                "name": "Mock Name 1"
            },
            {
                "email": "mock2@email.com",
                "id": 2,
                "is_active": True,
                "name": "Mock Name 2"
            },
            {
                "email": "mock3@email.com",
                "id": 3,
                "is_active": True,
                "name": "Mock Name 3"
            }
        ]

        self.mock_milestone_data = [
            {
                "completed_on": 1389968184,
                "description": "foo",
                "due_on": 1391968184,
                "id": 1,
                "is_completed": False,
                "name": "Release 1.5",
                "project_id": 1,
                "url": "http://<server>/index.php?/milestones/view/1"
            },
            {
                "completed_on": 1389968184,
                "description": "foo",
                "due_on": 1391968184,
                "id": 2,
                "is_completed": True,
                "name": "Release 1.5",
                "project_id": 1,
                "url": "http://<server>/index.php?/milestones/view/1"
            }
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
        active_runs = self.client.runs().active()
        self.assertEqual(len(active_runs), 1)
        self.assertEqual(active_runs[0].id, 111)

    @mock.patch('testrail.api.requests.get')
    def test_runcontainer_completed_runs(self, mock_get):
        mock_response = mock.Mock()
        mock_response.json.return_value = self.mock_runs_data
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        completed_runs = self.client.runs().completed()
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

    @mock.patch('testrail.api.requests.get')
    def test_plancontainer_contains_only_plan_objects(self, mock_get):
        mock_response = mock.Mock()
        mock_response.json.return_value = self.mock_plans_data
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        plans = self.client.plans()
        self.assertTrue(all([isinstance(r, Plan) for r in plans]))

    @mock.patch('testrail.api.requests.get')
    def test_plancontainer_active_plans(self, mock_get):
        mock_response = mock.Mock()
        mock_response.json.return_value = self.mock_plans_data
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        active_plans = self.client.plans().active()
        ids = [p.id for p in active_plans]
        self.assertEqual(len(ids), 3)
        self.assertTrue([lambda x: isinstance(x, Plan) for x in active_plans])
        self.assertNotEqual(ids[0], ids[1], ids[2])
        self.assertIn(22, ids)
        self.assertIn(33, ids)
        self.assertIn(44, ids)

    @mock.patch('testrail.api.requests.get')
    def test_plancontainer_completed_plans(self, mock_get):
        mock_response = mock.Mock()
        mock_response.json.return_value = self.mock_plans_data
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        completed_plans = self.client.plans().completed()
        self.assertTrue([lambda x: isinstance(x, Plan) for x in completed_plans])
        self.assertEqual(len(completed_plans), 1)
        self.assertEqual(completed_plans[0].id, 11)

    @mock.patch('testrail.api.requests.get')
    def test_plancontainer_latest_plan(self, mock_get):
        mock_response = mock.Mock()
        mock_response.json.return_value = self.mock_plans_data
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        latest_plan = self.client.plans().latest()
        self.assertTrue(isinstance(latest_plan, Plan))
        self.assertEqual(latest_plan.id, 44)

    @mock.patch('testrail.api.requests.get')
    def test_plancontainer_oldest_plan(self, mock_get):
        mock_response = mock.Mock()
        mock_response.json.return_value = self.mock_plans_data
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        oldest_plan = self.client.plans().oldest()
        self.assertTrue(isinstance(oldest_plan, Plan))
        self.assertEqual(oldest_plan.id, 11)

    @mock.patch('testrail.api.requests.get')
    def test_plancontainer_created_after_error(self, mock_get):
        mock_response = mock.Mock()
        mock_response.json.return_value = self.mock_plans_data
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        after_date = 1457762222
        with self.assertRaises(TestRailError) as e:
            created_after = self.client.plans().created_after(after_date)
        self.assertEqual(str(e.exception), 'Must pass in a datetime object')

    @mock.patch('testrail.api.requests.get')
    def test_plancontainer_created_after(self, mock_get):
        mock_response = mock.Mock()
        mock_response.json.return_value = self.mock_plans_data
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        after_date = dt.fromtimestamp(1457762222)
        created_after = self.client.plans().created_after(after_date)
        self.assertTrue([lambda x: isinstance(x, Plan) for x in created_after])
        self.assertEqual(len(created_after), 1)
        self.assertEqual(created_after[0].id, 33)

    @mock.patch('testrail.api.requests.get')
    def test_plancontainer_created_before_error(self, mock_get):
        mock_response = mock.Mock()
        mock_response.json.return_value = self.mock_plans_data
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        before_date = 1457762222
        with self.assertRaises(TestRailError) as e:
            created_before = self.client.plans().created_before(before_date)
        self.assertEqual(str(e.exception), 'Must pass in a datetime object')

    @mock.patch('testrail.api.requests.get')
    def test_plancontainer_created_before(self, mock_get):
        mock_response = mock.Mock()
        mock_response.json.return_value = self.mock_plans_data
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        before_date = dt.fromtimestamp(1457762222)
        created_before = self.client.plans().created_before(before_date)
        self.assertTrue([lambda x: isinstance(x, Plan) for x in created_before])
        self.assertEqual(len(created_before), 1)
        self.assertEqual(created_before[0].id, 11)

    @mock.patch('testrail.api.requests.get')
    def test_plancontainer_created_by_error(self, mock_get):
        API.flush_cache()
        mock_response = mock.Mock()
        mock_response.json.side_effect = [self.mock_plans_data, self.mock_users]
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        user = 3
        with self.assertRaises(TestRailError) as e:
            created_by = self.client.plans().created_by(user)
        self.assertEqual(str(e.exception), 'Must pass in a User object')

    @mock.patch('testrail.api.requests.get')
    def test_plancontainer_created_by(self, mock_get):
        API.flush_cache()
        mock_response = mock.Mock()
        mock_response.json.side_effect = [self.mock_plans_data, self.mock_users]
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        user = User({'id': 3})
        created_by = self.client.plans().created_by(user)
        self.assertTrue([lambda x: isinstance(x, Plan) for x in created_by])
        self.assertEqual(len(created_by), 1)
        self.assertEqual(created_by[0].id, 33)

    @mock.patch('testrail.api.requests.get')
    def test_plancontainer_plan_with_name_error(self, mock_get):
        mock_response = mock.Mock()
        mock_response.json.return_value = self.mock_plans_data
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        name = 3
        with self.assertRaises(TestRailError) as e:
            by_name = self.client.plans().name(name)
        self.assertEqual(str(e.exception), 'Must pass in a string')

    @mock.patch('testrail.api.requests.get')
    def test_plancontainer_plan_with_name_not_found(self, mock_get):
        mock_response = mock.Mock()
        mock_response.json.return_value = self.mock_plans_data
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        name = "3"
        with self.assertRaises(TestRailError) as e:
            by_name = self.client.plans().name(name)
        self.assertEqual(str(e.exception), "Plan with name '3' was not found")

    @mock.patch('testrail.api.requests.get')
    def test_plancontainer_with_name(self, mock_get):
        mock_response = mock.Mock()
        mock_response.json.return_value = self.mock_plans_data
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        plan_name = "Mock Plan2 Name"
        plan = self.client.plans().name(plan_name)
        self.assertTrue(isinstance(plan, Plan))
        self.assertEqual(plan.id, 22)

    @mock.patch('testrail.api.requests.get')
    def test_plancontainer_for_milestone(self, mock_get):
        mock_response = mock.Mock()
        mock_response.json.return_value = filter(
            lambda x: x['milestone_id'] == 1, self.mock_plans_data)
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        milestone = Milestone(self.mock_milestone_data[0])
        plans = self.client.plans(milestone)
        self.assertTrue(isinstance(plans, PlanContainer))
        self.assertTrue([isinstance(p, Plan) for p in plans])
        self.assertTrue([p._content['milestone_id'] == 1 for p in plans])

    @mock.patch('testrail.api.requests.get')
    def test_resultcontainer_contains_only_result_objects(self, mock_get):
        mock_response = mock.Mock()
        mock_response.json.return_value = self.mock_results_data
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        results = self.client.results(Run(self.mock_runs_data[0]))
        self.assertTrue(all([isinstance(r, Result) for r in results]))

    @mock.patch('testrail.api.requests.get')
    def test_resultcontainer_blocked_results(self, mock_get):
        mock_response = mock.Mock()
        mock_response.json.side_effect = [self.mock_results_data,
                                          self.mock_status_data]
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        results = self.client.results(Run(self.mock_runs_data[0]))

        blocked = results.blocked()

        self.assertEqual(len(blocked), 1)
        self.assertTrue([lambda x: isinstance(x, Result) for x in blocked])
        self.assertEqual(blocked[0].id, 22)

    @mock.patch('testrail.api.requests.get')
    def test_resultcontainer_failed_results(self, mock_get):
        mock_response = mock.Mock()
        mock_response.json.side_effect = [self.mock_results_data,
                                          self.mock_status_data]
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        results = self.client.results(Run(self.mock_runs_data[0]))

        failed = results.failed()

        self.assertEqual(len(failed), 1)
        self.assertTrue([lambda x: isinstance(x, Result) for x in failed])
        self.assertEqual(failed[0].id, 55)

    @mock.patch('testrail.api.requests.get')
    def test_resultcontainer_passed_results(self, mock_get):
        mock_response = mock.Mock()
        mock_response.json.side_effect = [self.mock_results_data,
                                          self.mock_status_data]
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        results = self.client.results(Run(self.mock_runs_data[0]))

        passed = results.passed()

        self.assertEqual(len(passed), 1)
        self.assertTrue([lambda x: isinstance(x, Result) for x in passed])
        self.assertEqual(passed[0].id, 11)

    @mock.patch('testrail.api.requests.get')
    def test_resultcontainer_retest_results(self, mock_get):
        mock_response = mock.Mock()
        mock_response.json.side_effect = [self.mock_results_data,
                                          self.mock_status_data]
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        results = self.client.results(Run(self.mock_runs_data[0]))

        retest = results.retest()

        self.assertEqual(len(retest), 1)
        self.assertTrue([lambda x: isinstance(x, Result) for x in retest])
        self.assertEqual(retest[0].id, 44)

    @mock.patch('testrail.api.requests.get')
    def test_resultcontainer_untested_results(self, mock_get):
        mock_response = mock.Mock()
        mock_response.json.side_effect = [self.mock_results_data,
                                          self.mock_status_data]
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        results = self.client.results(Run(self.mock_runs_data[0]))

        untested = results.untested()

        self.assertEqual(len(untested), 1)
        self.assertTrue([lambda x: isinstance(x, Result) for x in untested])
        self.assertEqual(untested[0].id, 33)

    @mock.patch('testrail.api.requests.get')
    def test_resultcontainer_latest_plan(self, mock_get):
        mock_response = mock.Mock()
        mock_response.json.return_value = self.mock_results_data
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        results = self.client.results(Run(self.mock_runs_data[0]))
        latest_result = results.latest()

        self.assertTrue(isinstance(latest_result, Result))
        self.assertEqual(latest_result.id, 44)

    @mock.patch('testrail.api.requests.get')
    def test_resultcontainer_oldest_plan(self, mock_get):
        mock_response = mock.Mock()
        mock_response.json.return_value = self.mock_results_data
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        results = self.client.results(Run(self.mock_runs_data[0]))
        oldest_result = results.oldest()

        self.assertTrue(isinstance(oldest_result, Result))
        self.assertEqual(oldest_result.id, 22)
