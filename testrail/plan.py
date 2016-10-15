from datetime import datetime

from testrail.base import TestRailBase
import testrail.entry
from testrail.api import API
from testrail.user import User
from testrail.project import Project
from testrail.milestone import Milestone
from testrail.helper import ContainerIter, TestRailError


class Plan(TestRailBase):
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
            return datetime.fromtimestamp(int(
                self._content.get('completed_on')))
        except TypeError:
            return None

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

    @description.setter
    def description(self, value):
        if not isinstance(value, str):
            raise TestRailError('input must be a string')
        self._content['description'] = value

    @property
    def entries(self):
        # ToDo convert entries to run objects
        if not self._content.get('entries'):
            self._content['entries'] = self.api.plan_with_id(
                self.id, with_entries=True).get('entries')
        return list(map(testrail.entry.Entry, self._content.get('entries')))

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
    def milestone(self):
        milestone_id = self._content.get('milestone_id')
        project_id = self._content.get('project_id')
        if milestone_id is None:
            return Milestone()
        return Milestone(self.api.milestone_with_id(milestone_id, project_id))

    @milestone.setter
    def milestone(self, v):
        if not isinstance(v, Milestone):
            raise TestRailError('input must be a Milestone')
        self._content['milestone_id'] = v.id

    @property
    def name(self):
        return self._content.get('name')

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TestRailError('input must be a string')
        self._content['name'] = value

    @property
    def passed_count(self):
        return self._content.get('passed_count')

    @property
    def project(self):
        return Project(
            self.api.project_with_id(self._content.get('project_id')))

    @project.setter
    def project(self, value):
        if not isinstance(value, Project):
            raise TestRailError('input must be a Project')
        self.api.project_with_id(value.id)  # verify project is valid
        self._content['project_id'] = value.id

    @property
    def project_id(self):
        return self._content.get('project_id')

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


class PlanContainer(ContainerIter):
    def __init__(self, plans):
        super(PlanContainer, self).__init__(plans)
        self._plans = plans

    def completed(self):
        return list(filter(lambda p: p.is_completed is True, self._plans))

    def active(self):
        return list(filter(lambda p: p.is_completed is False, self._plans))

    def created_after(self, dt):
        if not isinstance(dt, datetime):
            raise TestRailError("Must pass in a datetime object")
        return list(filter(lambda p: p.created_on > dt, self._plans))

    def created_before(self, dt):
        if not isinstance(dt, datetime):
            raise TestRailError("Must pass in a datetime object")
        return list(filter(lambda p: p.created_on < dt, self._plans))

    def created_by(self, user):
        if not isinstance(user, User):
            raise TestRailError("Must pass in a User object")
        return list(filter(lambda p: p.created_by.id == user.id, self._plans))

    def latest(self):
        self._plans.sort(key=lambda x: x.created_on)
        return self._plans[-1]

    def oldest(self):
        self._plans.sort(key=lambda x: x.created_on)
        return self._plans[0]

    def name(self, name):
        if not isinstance(name, str):
            raise TestRailError("Must pass in a string")

        def comp_func(p):
            return p.name.lower() == name.lower()

        try:
            return list(filter(comp_func, self._plans)).pop(0)
        except IndexError:
            raise TestRailError("Plan with name '%s' was not found" % name)
