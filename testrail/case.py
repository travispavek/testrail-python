from user import User
from milestone import Milestone
from priority import Priority
from suite import Suite
from section import Section
from casetype import CaseType
import api
from datetime import datetime


class Case(object):
    def __init__(self, content):
        self._content = content
        self.api = api.API()

    @property
    def created_by(self):
        user_id = self._content.get('created_by')
        return User(self.api.user_by_id(user_id))

    @property
    def created_on(self):
        return datetime.fromtimestamp(int(self._content.get('created_on')))

    @property
    def estimate(self):
        return self._content.get('estimate')

    @property
    def estimated_forecast(self):
        return self._content.get('estimated_forecast')

    @property
    def id(self):
        return self._content.get('id')

    @property
    def milestone(self):
        m = self.api.milestone_with_id(self._content.get('milestone_id'))
        if m:
            return Milestone(m)
        else:
            return None

    @property
    def priority(self):
        p = self.api.priority_with_id(self._content.get('priority_id'))
        if p:
            return Priority(p)
        return None

    @property
    def refs(self):
        return self._content.get('refs')

    @property
    def section(self):
        s = self.api.section_with_id(self._content.get('section_id'))
        if s:
            return Section(s)
        return None

    @property
    def suite(self):
        s = self.api.suite_with_id(self._content.get('suite_id'))
        if s:
            return Suite(s)
        return None

    @property
    def title(self):
        return self._content.get('title')

    @property
    def type(self):
        t = self.api.case_type_with_id(self._content.get('type_id'))
        if t:
            return CaseType(t)
        return None

    @property
    def updated_by(self):
        user_id = self._content.get('updated_by')
        return User(self.api.user_by_id(user_id))

    @property
    def updated_on(self):
        return datetime.fromtimestamp(int(self._content.get('updated_on')))
