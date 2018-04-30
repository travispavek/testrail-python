from datetime import datetime
import sys

from testrail.base import TestRailBase
from testrail.api import API
from testrail.casetype import CaseType
from testrail.helper import custom_methods, TestRailError
from testrail.milestone import Milestone
from testrail.priority import Priority
from testrail.section import Section
from testrail.suite import Suite
from testrail.template import Template
from testrail.user import User

if sys.version_info >= (3,0):
    unicode = str

class Case(TestRailBase):
    def __init__(self, content=None):
        self._content = content or dict()
        self.api = API()
        self._custom_methods = custom_methods(self._content)

    def __getattr__(self, attr):
        if attr in self._custom_methods:
            return self._content.get(self._custom_methods[attr])
        raise AttributeError("'{}' object has no attribute '{}'".format(
            self.__class__.__name__, attr))

    def __str__(self):
        return self.title

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

    @estimate.setter
    def estimate(self, value):
        #TODO should have some logic to validate format of timespa
        if not isinstance(value, (str, unicode)):
            raise TestRailError('input must be a string')
        self._content['estimate'] = value

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

    @milestone.setter
    def milestone(self, value):
        if not isinstance(value, Milestone):
            raise TestRailError('input must be a Milestone')
        self._content['milestone_id'] = value.id

    
    @property
    def priority(self):
        p = self.api.priority_with_id(self._content.get('priority_id'))
        return Priority(p) if p else Priority()

    @priority.setter
    def priority(self, value):
        if not isinstance(value, Priority):
            raise TestRailError('input must be a Priority')
        self._content['priority_id'] = value.id

    @property
    def refs(self):
        refs = self._content.get('refs')
        return refs.split(',') if refs else list()

    @refs.setter
    def refs(self, value):
        if not isinstance(value, list):
            raise TestRailError('input must be a list')
        self._content['refs'] = ','.join(value)

    
    @property
    def section(self):
        s = self.api.section_with_id(self._content.get('section_id'))
        return Section(s) if s else Section()

    @section.setter
    def section(self, value):
        if not isinstance(value, Section):
            raise TestRailError('input must be a Section')
        self._content['section_id'] = value.id
    
    @property
    def suite(self):
        s = self.api.suite_with_id(self._content.get('suite_id'))
        return Suite(s) if s else Suite()

    @suite.setter
    def suite(self, value):
        if not isinstance(value, Suite):
            raise TestRailError('input must be a Suite')
        self._content['suite_id'] = value.id

    @property
    def title(self):
        return self._content.get('title')

    @title.setter
    def title(self, value):
        if not isinstance(value, (str, unicode)):
            raise TestRailError('input must be a string')
        self._content['title'] = value

    @property
    def type(self):
        t = self.api.case_type_with_id(self._content.get('type_id'))
        return CaseType(t) if t else CaseType()

    @type.setter
    def type(self, value):
        if not isinstance(value, CaseType):
            raise TestRailError('input must be a CaseType')
        self._content['type_id'] = value.id


    @property
    def updated_by(self):
        user_id = self._content.get('updated_by')
        return User(self.api.user_by_id(user_id))

    @property
    def updated_on(self):
        return datetime.fromtimestamp(int(self._content.get('updated_on')))

    @property
    def template(self):
        # we don't get the template, on needed as a setter
        raise NotImplementedError

    @template.setter
    def template(self, value):
        if not isinstance(value, Template):
            raise TestRailError('input must be a Template')
        self._content['template_id'] = value.id
    
    def raw_data(self):
        return self._content
