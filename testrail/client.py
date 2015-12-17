
from project import Project
from user import User
from case import Case
from suite import Suite
from plan import Plan, PlanContainer
from run import Run, RunContainer
from test import Test
from result import Result
from milestone import Milestone
from status import Status
from configuration import Config, ConfigContainer
import api
from helper import methdispatch, singleresult
import re


class TestRail(object):
    def __init__(self, project_id=0):
        self.api = api.API()
        #project_id = self.project(project)
        self.api.set_project_id(project_id)
        self._project_id = project_id

    def set_project_id(self, project_id):
        self._project_id = project_id
        self._api.set_project_id(project_id)

    # Post generics
    @methdispatch
    def add(self, obj):
        raise NotImplementedError

    @methdispatch
    def update(self, obj):
        raise NotImplementedError

    @methdispatch
    def delete(self, obj):
        raise NotImplementedError

    # Project Methods
    def completed_projects(self):
        return map(Project, filter(lambda x: x['is_completed'] is True, self.api.projects()))

    def active_projects(self):
        return map(Project, filter(lambda x: x['is_completed'] is False, self.api.projects()))

    def projects(self):
        return map(Project, self.api.projects())

    @methdispatch
    def project(self):
        return Project()

    @project.register(str)
    @singleresult
    def _project_by_name(self, name):
        return filter(lambda p: p.name == name, self.projects())

    @project.register(int)
    @singleresult
    def _project_by_id(self, project_id):
        return filter(lambda p: p.id == project_id, self.projects())

    # User Methods
    def users(self):
        return map(User, self.api.users())

    @methdispatch
    def user(self):
        return User()

    @user.register(int)
    @singleresult
    def _user_by_id(self, identifier):
        return filter(lambda u: u.id == identifier, self.users())

    @user.register(str)
    @singleresult
    def _user_by_email_name(self, identifier):
        by_email = lambda u: u.email == identifier
        by_name = lambda u: u.name == identifier
        f = by_email if re.match('[^@]+@[^@]+\.[^@]+', identifier) else by_name
        return filter(f, self.users())

    def active_users(self):
        return filter(lambda u: u.is_active is True, self.users())

    def inactive_users(self):
        return filter(lambda u: u.is_active is False, self.users())

    # Suite Methods
    def suites(self):
        return map(Suite, self.api.suites(self._project_id))

    @methdispatch
    def suite(self):
        return Suite()

    @suite.register(str)
    @singleresult
    def _suite_by_name(self, name):
        return filter(lambda s: s.name.lower() == name.lower(), self.suites())

    @suite.register(int)
    @singleresult
    def _suite_by_id(self, suite_id):
        return filter(lambda s: s.id == suite_id, self.suites())

    def active_suites(self):
        return filter(lambda s: s.is_completed is False, self.suites())

    def completed_suites(self):
        return filter(lambda s: s.is_completed is True, self.suites())

    # Milestone Methods
    def milestones(self):
        return map(Milestone, self.api.milestones(self._project_id))

    @methdispatch
    def milestone(self):
        return Milestone()

    @milestone.register(str)
    @singleresult
    def _milestone_by_name(self, name):
        return filter(lambda m: m.name.lower() == name.lower(), self.milestones())

    @milestone.register(int)
    @singleresult
    def _milestone_by_id(self, milestone_id):
        return filter(lambda s: s.id == milestone_id, self.milestones())

    @add.register(Milestone)
    def _add_milestone(self, obj):
        obj.project = obj.project or self.project(self._project_id)
        self.api.add_milestone(obj.raw_data())

    @update.register(Milestone)
    def _update_milestone(self, obj):
        self.api.update_milestone(obj.raw_data())

    @delete.register(Milestone)
    def _delete_milestone(self, obj):
        self.api.delete_milestone(obj.id)

    # Plan Methods
    @methdispatch
    def plans(self):
        return map(Plan, self.api.plans(self._project_id))

    @plans.register(Milestone)
    def _plans_for_milestone(self, obj):
        return PlanContainer(filter(lambda p: p.milestone.id == obj.id, self.plans()))

    @methdispatch
    def plan(self):
        return Plan()

    @plan.register(str)
    @singleresult
    def _plan_by_name(self, name):
        return filter(lambda p: p.name.lower() == name.lower(), self.plans())

    @plan.register(int)
    @singleresult
    def _plan_by_id(self, plan_id):
        filter(lambda p: p.id == plan_id, self.plans())

    def completed_plans(self):
        return filter(lambda p: p.is_completed is True, self.plans())

    def active_plans(self):
        return filter(lambda p: p.is_completed is False, self.plans())

    # Run Methods
    @methdispatch
    def runs(self):
        return map(Run, self.api.runs(self._project_id))

    @runs.register(Milestone)
    def _runs_for_milestone(self, obj):
        return RunContainer(filter(lambda r: r.milestone.id == obj.id, self.runs()))

    @methdispatch
    def run(self):
        return Run()

    @run.register(str)
    @singleresult
    def _run_by_name(self, name):
        return filter(lambda p: p.name.lower() == name.lower(), self.runs())

    @run.register(int)
    @singleresult
    def _run_by_id(self, run_id):
        filter(lambda p: p.id == run_id, self.runs())

    # Case Methods
    def cases(self, suite):
        return map(Case, self.api.cases(self._project_id, suite.id))

    @methdispatch
    def case(self):
        return Case()

    @case.register(str)
    @singleresult
    def _case_by_title(self, title, suite):
        return filter(lambda c: c.title.lower() == title.lower(), self.cases(suite))

    @case.register(int)
    @singleresult
    def _case_by_id(self, case_id, suite=None):
        if suite is None:
            pass
        else:
            return filter(lambda c: c.id == case_id, self.cases(suite))

    # Test Methods
    def tests(self, run):
        return map(Test, self.api.tests(run.id))

    @methdispatch
    def test(self):
        return Test()

    @test.register(str)
    @singleresult
    def _test_by_name(self, name):
        return filter(lambda t: t.name.lower() == name.lower(), self.tests())

    @test.register(int)
    @singleresult
    def _test_by_id(self, test_id, run):
        return filter(lambda t: t.raw_data()['case_id'] == test_id, self.tests(run))

    # Result Methods
    def results(self, test_id):
        return map(Result, self.api.results(test_id))

    @methdispatch
    def result(self):
        return Result()

    @result.register(int)
    @singleresult
    def _result_by_id(self, result_id):
        return filter(lambda r: r.id == result_id, self.results())

    @add.register(Result)
    def _add_result(self, obj):
        self.api.add_result(obj.raw_data())

    @add.register(tuple)
    def _add_results(self, results):
        obj, value = results
        if isinstance(obj, Run):
            self.api.add_results(map(lambda x: x.raw_data(), value), obj.id)

    # Status Methods
    def statuses(self):
        return map(Status, self.api.statuses())

    @methdispatch
    def status(self):
        return Status()

    @status.register(str)
    @singleresult
    def _status_by_name(self, name):
        return filter(lambda s: s.name == name.lower(), self.statuses())

    @status.register(int)
    @singleresult
    def _status_by_id(self, status_id):
        return filter(lambda s: s.id == status_id, self.statuses())

    def configs(self):
        return ConfigContainer(map(Config, self.api.configs()))
