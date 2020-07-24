import re
import sys

from testrail.api import API
from testrail.case import Case
from testrail.configuration import Config, ConfigContainer
from testrail.helper import methdispatch, singleresult, TestRailError
from testrail.milestone import Milestone
from testrail.plan import Plan, PlanContainer
from testrail.project import Project, ProjectContainer
from testrail.result import Result, ResultContainer
from testrail.run import Run, RunContainer
from testrail.status import Status
from testrail.suite import Suite
from testrail.section import Section
from testrail.test import Test
from testrail.user import User

if sys.version_info >= (3,0):
    unicode = str

class TestRail(object):
    def __init__(self, project_id=0, email=None, key=None, url=None):
        self.api = API(email=email, key=key, url=url)
        self.api.set_project_id(project_id)
        self._project_id = project_id

    def set_project_id(self, project_id):
        self._project_id = project_id
        self.api.set_project_id(project_id)

    # Post generics
    @methdispatch
    def add(self, obj):
        raise NotImplementedError

    @methdispatch
    def update(self, obj):
        raise NotImplementedError

    @methdispatch
    def close(self, obj):
        raise NotImplementedError

    @methdispatch
    def delete(self, obj):
        raise NotImplementedError

    # Project Methods
    def projects(self):
        return ProjectContainer(list(map(Project, self.api.projects())))

    @methdispatch
    def project(self):
        return Project()

    @project.register(str)
    @project.register(unicode)
    @singleresult
    def _project_by_name(self, name):
        return filter(lambda p: p.name == name, self.projects())

    @project.register(int)
    @singleresult
    def _project_by_id(self, project_id):
        return filter(lambda p: p.id == project_id, self.projects())

    # User Methods
    def users(self):
        return list(map(User, self.api.users()))

    @methdispatch
    def user(self):
        return User()

    @user.register(int)
    @singleresult
    def _user_by_id(self, identifier):
        return filter(lambda u: u.id == identifier, self.users())

    @user.register(str)
    @user.register(unicode)
    @singleresult
    def _user_by_email_name(self, identifier):
        by_email = lambda u: u.email == identifier
        by_name = lambda u: u.name == identifier
        f = by_email if re.match('[^@]+@[^@]+\.[^@]+', identifier) else by_name
        return filter(f, self.users())

    def active_users(self):
        return list(filter(lambda u: u.is_active is True, self.users()))

    def inactive_users(self):
        return list(filter(lambda u: u.is_active is False, self.users()))

    # Suite Methods
    def suites(self):
        return list(map(Suite, self.api.suites(self._project_id)))

    @methdispatch
    def suite(self):
        return Suite()

    @suite.register(str)
    @suite.register(unicode)
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

    @add.register(Suite)
    def _add_suite(self, obj):
        obj.project = obj.project or self.project(self._project_id)
        return Suite(self.api.add_suite(obj.raw_data()))

    @update.register(Suite)
    def _update_suite(self, obj):
        return Suite(self.api.update_suite(obj.raw_data()))

    @delete.register(Suite)
    def _delete_suite(self, obj):
        return self.api.delete_suite(obj.id)

    # Milestone Methods
    def milestones(self):
        return list(map(Milestone, self.api.milestones(self._project_id)))

    @methdispatch
    def milestone(self):
        return Milestone()

    @milestone.register(str)
    @milestone.register(unicode)
    @singleresult
    def _milestone_by_name(self, name):
        return filter(
            lambda m: m.name.lower() == name.lower(), self.milestones())

    @milestone.register(int)
    @singleresult
    def _milestone_by_id(self, milestone_id):
        return filter(lambda s: s.id == milestone_id, self.milestones())

    @add.register(Milestone)
    def _add_milestone(self, obj):
        obj.project = obj.project or self.project(self._project_id)
        return Milestone(self.api.add_milestone(obj.raw_data()))

    @update.register(Milestone)
    def _update_milestone(self, obj):
        return Milestone(self.api.update_milestone(obj.raw_data()))

    @delete.register(Milestone)
    def _delete_milestone(self, obj):
        return self.api.delete_milestone(obj.id)

    # Plan Methods
    @methdispatch
    def plans(self):
        return PlanContainer(list(map(Plan, self.api.plans(self._project_id))))

    @plans.register(Milestone)
    def _plans_for_milestone(self, obj):
        plans = filter(lambda p: p.milestone is not None, self.plans())
        return PlanContainer(filter(lambda p: p.milestone.id == obj.id, plans))

    @methdispatch
    def plan(self):
        return Plan()

    @plan.register(str)
    @plan.register(unicode)
    @singleresult
    def _plan_by_name(self, name):
        return filter(lambda p: p.name.lower() == name.lower(), self.plans())

    @plan.register(int)
    @singleresult
    def _plan_by_id(self, plan_id):
        return filter(lambda p: p.id == plan_id, self.plans())

    def completed_plans(self):
        return filter(lambda p: p.is_completed is True, self.plans())

    def active_plans(self):
        return filter(lambda p: p.is_completed is False, self.plans())

    @add.register(Plan)
    def _add_plan(self, obj, milestone=None):
        obj.project = obj.project or self.project(self._project_id)
        obj.milestone = milestone or obj.milestone
        return Plan(self.api.add_plan(obj.raw_data()))

    @update.register(Plan)
    def _update_plan(self, obj):
        return Plan(self.api.update_plan(obj.raw_data()))

    @close.register(Plan)
    def _close_plan(self, obj):
        return Plan(self.api.close_plan(obj.id))

    @delete.register(Plan)
    def _delete_plan(self, obj):
        return self.api.delete_plan(obj.id)

    # Run Methods
    @methdispatch
    def runs(self):
        return RunContainer(list(map(Run, self.api.runs(self._project_id))))

    @runs.register(Milestone)
    def _runs_for_milestone(self, obj):
        return RunContainer(filter(
            lambda r: r.milestone.id == obj.id, self.runs()))

    @runs.register(str)
    @runs.register(unicode)
    def _runs_by_name(self, name):
        # Returns all Runs that match :name, in descending order by ID
        runs = list(filter(lambda r: r.name.lower() == name.lower(), self.runs()))
        return sorted(runs, key=lambda r: r.id)

    @methdispatch
    def run(self):
        return Run()

    @run.register(str)
    @run.register(unicode)
    @singleresult
    def _run_by_name(self, name):
        # Returns the most recently created Run that matches :name
        runs = list(filter(lambda r: r.name.lower() == name.lower(), self.runs()))
        return sorted(runs, key=lambda r: r.id)[:1]

    @run.register(int)
    @singleresult
    def _run_by_id(self, run_id):
        return filter(lambda p: p.id == run_id, self.runs())

    @add.register(Run)
    def _add_run(self, obj):
        obj.project = obj.project or self.project(self._project_id)
        return Run(self.api.add_run(obj.raw_data()))

    @update.register(Run)
    def _update_run(self, obj):
        return Run(self.api.update_run(obj.raw_data()))

    @close.register(Run)
    def _close_run(self, obj):
        return Run(self.api.close_run(obj.id))

    @delete.register(Run)
    def _delete_run(self, obj):
        return self.api.delete_run(obj.id)

    # Case Methods
    def cases(self, suite):
        return list(map(Case, self.api.cases(self._project_id, suite.id)))

    @methdispatch
    def case(self):
        return Case()

    @case.register(str)
    @case.register(unicode)
    @singleresult
    def _case_by_title(self, title, suite):
        return filter(
            lambda c: c.title.lower() == title.lower(), self.cases(suite))

    @case.register(int)
    @singleresult
    def _case_by_id(self, case_id, suite=None):
        if suite is None:
            pass
        else:
            return filter(lambda c: c.id == case_id, self.cases(suite))

    @add.register(Case)
    def _add_case(self, obj):
        return Case(self.api.add_case(obj.raw_data()))

    @update.register(Case)
    def _update_case(self, obj):
        return Case(self.api.update_case(obj.raw_data()))

    # Test Methods
    def tests(self, run):
        return list(map(Test, self.api.tests(run.id)))

    @methdispatch
    def test(self):
        return Test()

    @test.register(str)
    @test.register(unicode)
    @singleresult
    def _test_by_name(self, name, run):
        return filter(lambda t: t.title.lower() == name.lower(), self.tests(run))

    @test.register(int)
    @singleresult
    def _test_by_id(self, test_id, run):
        return filter(
            lambda t: t.raw_data()['id'] == test_id, self.tests(run))

    # Result Methods
    @methdispatch
    def results(self):
        raise TestRailError("Must request results by Run or Test")

    @results.register(Run)
    def _results_for_run(self, run):
        return ResultContainer(list(map(Result, self.api.results_by_run(run.id))))

    @results.register(Test)
    def _results_for_test(self, test):
        return ResultContainer(list(map(Result, self.api.results_by_test(test.id))))

    @methdispatch
    def result(self):
        return Result()

    @add.register(Result)
    def _add_result(self, obj):
        self.api.add_result(obj.raw_data())

    @add.register(tuple)
    def _add_results(self, results):
        obj, value = results
        if isinstance(obj, Run):
            self.api.add_results(list(map(lambda x: x.raw_data(), value)), obj.id)

    # Section Methods
    def sections(self, suite=None):
        return list(map(Section, self.api.sections(suite_id=suite.id)))

    @methdispatch
    def section(self):
        return Section()

    @section.register(int)
    def _section_by_id(self, section_id):
        return Section(self.api.section_with_id(section_id))

    @section.register(unicode)
    @section.register(str)
    @singleresult
    def _section_by_name(self, name, suite=None):
        return filter(lambda s: s.name == name, self.sections(suite))

    @add.register(Section)
    def _add_section(self, section):
        return Section(self.api.add_section(section.raw_data()))

    # Status Methods
    def statuses(self):
        return list(map(Status, self.api.statuses()))

    @methdispatch
    def status(self):
        return Status()

    @status.register(str)
    @status.register(unicode)
    @singleresult
    def _status_by_name(self, name):
        return filter(lambda s: s.name == name.lower(), self.statuses())

    @status.register(int)
    @singleresult
    def _status_by_id(self, status_id):
        return filter(lambda s: s.id == status_id, self.statuses())

    def configs(self):
        return ConfigContainer(list(map(Config, self.api.configs())))
