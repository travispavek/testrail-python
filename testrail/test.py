import api
from user import User
from case import Case
from milestone import Milestone
from project import Project
from run import Run
from status import Status
from casetype import CaseType


class Test(object):
    def __init__(self, content={}):
        self._content = content
        self.api = api.API()

    @property
    def assignedto(self):
        return User(self.api.user_with_id(self._content.get('assignedto_id')))

    @property
    def case(self):
        return Case(self.api.case_with_id(self._content.get('case_id')))

    @property
    def estimate(self):
        return self._content.get('estimate')

    @property
    def estimate_forecast(self):
        return self._content.get('estimate_forecast')

    @property
    def id(self):
        return self._content.get('id')

    @property
    def milestone(self):
        return Milestone(self.api.milestone_with_id(self._content.get('milestone_id'), self._content.get('project_id')))

    @property
    def project(self):
        return Project(self.api.project_with_id(self._content.get('project_id')))

    @property
    def refs(self):
        return self._content.get('refs')

    @property
    def run(self):
        return Run(self.api.run_with_id(self._content.get('run')))

    @property
    def status(self):
        return Status(self.api.status_with_id(self._content.get('status_id')))

    @property
    def title(self):
        return self._content.get('title')

    @property
    def case_type(self):
        return CaseType(self.api.case_type_with_id(self._content.get('type_id')))

    def raw_data(self):
        return self._content
