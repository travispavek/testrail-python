from testrail.base import TestRailBase
from testrail import api
from testrail.case import Case
from testrail.casetype import CaseType
from testrail.milestone import Milestone
from testrail.project import Project
from testrail.run import Run
from testrail.status import Status
from testrail.user import User
from testrail.helper import testrail_duration_to_timedelta


class Test(TestRailBase):
    def __init__(self, content=None):
        self._content = content or dict()
        self.api = api.API()

    def __str__(self):
        return self.title

    @property
    def assigned_to(self):
        return User(self.api.user_with_id(self._content.get('assignedto_id')))

    @property
    def case(self):
        return Case(self.api.case_with_id(self._content.get('case_id'), suite_id=self.run.suite.id))

    @property
    def estimate(self):
        duration = self._content.get('estimate')
        if duration is None:
            return None
        return testrail_duration_to_timedelta(duration)

    @property
    def estimate_forecast(self):
        duration = self._content.get('estimate_forecast')
        if duration is None:
            return None
        return testrail_duration_to_timedelta(duration)

    @property
    def id(self):
        return self._content.get('id')

    @property
    def milestone(self):
        project_id = self._content.get('project_id')
        milestone_id = self._content.get('milestone_id')
        if milestone_id is None:
            return None
        return Milestone(self.api.milestone_with_id(milestone_id, project_id))

    @property
    def refs(self):
        return self._content.get('refs')

    @property
    def run(self):
        return Run(self.api.run_with_id(self._content.get('run_id')))

    @property
    def status(self):
        return Status(self.api.status_with_id(self._content.get('status_id')))

    @property
    def title(self):
        return self._content.get('title')

    def raw_data(self):
        return self._content
