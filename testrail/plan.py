import api
from user import User
from milestone import Milestone
from project import Project
from datetime import datetime
from helper import ContainerIter
import entry


class Plan(object):
    def __init__(self, content):
        self._content = content
        self.api = api.API()

    @property
    def assigned_to(self):
        return User(self.api.user_with_id(self._content.get('assignedto_id')))

    @property
    def blocked_count(self):
        return self._content.get('blocked_count')

    @property
    def completed_on(self):
        try:
            return datetime.fromtimestamp(int(self._content.get('completed_on')))
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

    @property
    def entries(self):
        # ToDo convert entries to run objects
        if self._content.get('entries') is None:
            self._content['entries'] = self.api.plan_with_id(self.id).get('entries')
        return map(entry.Entry, self._content.get('entries'))

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
        return Milestone(self.api.milestone_with_id(self._content.get('milestone_id'), self._content.get('project_id')))

    @property
    def name(self):
        return self._content.get('name')

    @property
    def passed_count(self):
        return self._content.get('passed_count')

    @property
    def project(self):
        return Project(self.api.project_with_id(self._content.get('project_id')))

    @property
    def retest_count(self):
        return self._content.get('retest_count')

    @property
    def untested_count(self):
        return self._content.get('untested_count')

    @property
    def url(self):
        return self._content.get('url')


class PlanContainer(ContainerIter):
    def __init__(self, plans):
        super(PlanContainer, self).__init__(plans)
        self._plans = plans

    def completed(self):
        return filter(lambda p: p.is_completed is True, self._plans)

    def active(self):
        return filter(lambda p: p.is_completed is False, self._plans)

    def created_after(self, dt):
        return filter(lambda p: p.created_on > dt, self._plans)

    def created_before(self, dt):
        return filter(lambda p: p.created_on < dt, self._plans)

    def created_by(self, user):
        return filter(lambda p: p.created_by.id == user.id, self._plans)

    def latest(self):
        self._plans.sort(key=lambda x: x.created_on)
        return self._plans[-1]

    def oldest(self):
        self._plans.sort(key=lambda x: x.created_on)
        return self._plans[0]

    def name(self, name):
        return filter(lambda p: p.name.lower() == name.lower(), self._plans)
