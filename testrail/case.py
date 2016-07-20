from datetime import datetime

from testrail.api import API
from testrail.casetype import CaseType
from testrail.milestone import Milestone
from testrail.priority import Priority
from testrail.section import Section
from testrail.suite import Suite
from testrail.user import User


class Case(object):
    def __init__(self, content):
        self._content = content
        self.api = API()

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
        return Milestone(m) if m else Milestone()

    @property
    def priority(self):
        p = self.api.priority_with_id(self._content.get('priority_id'))
        return Priority(p) if p else Priority()

    @property
    def refs(self):
        return self._content.get('refs')

    @property
    def section(self):
        s = self.api.section_with_id(self._content.get('section_id'))
        return Section(s) if s else Section()

    @property
    def suite(self):
        s = self.api.suite_with_id(self._content.get('suite_id'))
        return Suite(s) if s else Suite()

    @property
    def title(self):
        return self._content.get('title')

    @property
    def type(self):
        t = self.api.case_type_with_id(self._content.get('type_id'))
        return CaseType(t) if t else CaseType()

    @property
    def updated_by(self):
        user_id = self._content.get('updated_by')
        return User(self.api.user_by_id(user_id))

    @property
    def updated_on(self):
        return datetime.fromtimestamp(int(self._content.get('updated_on')))

    def raw_data(self):
        return self._content
