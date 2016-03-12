from datetime import datetime

from testrail.api import API
from testrail.helper import ContainerIter
from testrail.milestone import Milestone
import testrail.plan
from testrail.project import Project
from testrail.user import User


class Run(object):
    def __init__(self, content=None):
        self._content = content or dict()
        self.api = API()

    @property
    def assigned_to(self):
        return User(self.api.user_with_id(self._content.get('assignedto_id')))

    @property
    def blocked_count(self):
        return self._content.get('blocked_count')

    @property
    def completed_on(self):
        try:
            return datetime.fromtimestamp(
                int(self._content.get('completed_on')))
        except TypeError:
            return None

    @property
    def config(self):
        return self._content.get('config')

    @property
    def config_ids(self):
        return self._content.get('config_ids')

    @property
    def created_on(self):
        try:
            return datetime.fromtimestamp(int(self._content.get('created_on')))
        except TypeError:
            return None

    @property
    def created_by(self):
        return User(self.api.user_with_id(self._content.get('created_by')))

    @property
    def custom_status_count(self):
        return self._content.get('custom_status_count')

    @property
    def description(self):
        return self._content.get('description')

    @property
    def failed_count(self):
        return self._content.get('failed_count')

    @property
    def id(self):
        return self._content.get('id')

    @property
    def is_completed(self):
        return self._content.get('is_completed')

    @property
    def include_all(self):
        return self._content.get('include_all')

    @property
    def milestone(self):
        return Milestone(self.api.milestone_with_id(self._content.get(
            'milestone_id'), self._content.get('project_id')))

    @property
    def plan(self):
        return plan.Plan(self.api.plan_with_id(self._content.get('plan_id')))

    @property
    def name(self):
        return self._content.get('name')

    @name.setter
    def name(self, value):
        if type(value) != str:
            raise TestRailError('input must be a string')
        self._content['name'] = value

    @property
    def passed_count(self):
        return self._content.get('passed_count')

    @property
    def project(self):
        return Project(self.api.project_with_id(self._content.get('project_id')))

    @project.setter
    def project(self, value):
        if type(value) != Project:
            raise TestRailError('input must be a Project')
        self.api.project_with_id(value.id)  # verify project is valid
        self._content['project_id'] = value.id

    @property
    def retest_count(self):
        return self._content.get('retest_count')

    @property
    def untested_count(self):
        return self._content.get('untested_count')

    @property
    def url(self):
        return self._content.get('url')

    def raw_data(self):
        return self._content


class RunContainer(ContainerIter):
    def __init__(self, runs):
        super(RunContainer, self).__init__(runs)
        self._runs = runs

    def latest(self):
        self._runs.sort(key=lambda x: x.created_on)
        return self._runs[-1]

    def oldest(self):
        self._runs.sort(key=lambda x: x.created_on)
        return self._runs[0]

    def completed(self):
        return filter(lambda m: m.is_completed is True, self._runs)

    def active(self):
        return filter(lambda m: m.is_completed is False, self._runs)
