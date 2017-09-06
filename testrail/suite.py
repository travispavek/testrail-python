from datetime import datetime

from testrail.base import TestRailBase
from testrail import api
from testrail.helper import TestRailError
from testrail.project import Project


class Suite(TestRailBase):
    def __init__(self, content=None):
        self._content = content or dict()
        self.api = api.API()

    def __str__(self):
        return self.name

    @property
    def id(self):
        return self._content.get('id')

    @property
    def completed_on(self):
        try:
            return datetime.fromtimestamp(
                int(self._content.get('completed_on')))
        except TypeError:
            return None

    @property
    def description(self):
        return self._content.get('description')

    @description.setter
    def description(self, value):
        if not isinstance(value, str):
            raise TestRailError('input must be a string')
        self._content['description'] = value

    @property
    def is_baseline(self):
        return self._content.get('is_baseline')

    @property
    def is_completed(self):
        return self._content.get('is_completed')

    @property
    def is_master(self):
        return self._content.get('is_master')

    @property
    def name(self):
        return self._content.get('name')

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TestRailError('input must be a string')
        self._content['name'] = value

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
    def url(self):
        return self._content.get('url')

    def raw_data(self):
        return self._content
