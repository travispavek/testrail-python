from testrail.base import TestRailBase
from testrail import api
from testrail.helper import TestRailError
from testrail.suite import Suite


class Section(TestRailBase):
    def __init__(self, content=None):
        self._content = content or dict()
        self.api = api.API()

    def __str__(self):
        return self.name

    @property
    def id(self):
        return self._content.get('id')

    @property
    def depth(self):
        return self._content.get('depth')

    @property
    def display_order(self):
        return self._content.get('display_order')

    @property
    def description(self):
        return self._content.get('description')

    @description.setter
    def description(self, value):
        if not isinstance(value, str):
            raise TestRailError('input must be a string')
        self._content['description'] = value

    @property
    def parent(self):
        return Section(
            self.api.section_with_id(self._content.get('parent_id')))

    @parent.setter
    def parent(self, section):
        if not isinstance(section, Section):
            raise TestRailError('input must be a Section')
        self.api.section_with_id(section.id)  # verify section is valid
        self._content['parent_id'] = section.id

    @property
    def name(self):
        return self._content.get('name')

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TestRailError('input must be a string')
        self._content['name'] = value

    @property
    def suite(self):
        if self._content.get('suite_id') is None:
            return Suite()
        return Suite(self.api.suite_with_id(self._content.get('suite_id')))

    @suite.setter
    def suite(self, suite_obj):
        if not isinstance(suite_obj, Suite):
            raise TestRailError('input must be a Suite')
        self.api.suite_with_id(suite_obj.id)  # verify suite is valid
        self._content['suite_id'] = suite_obj.id

    def raw_data(self):
        return self._content
