from datetime import datetime
import time

from testrail.base import TestRailBase
from testrail import api
from testrail.project import Project
from testrail.helper import TestRailError


class Milestone(TestRailBase):
    def __init__(self, content=None):
        self._content = content or dict()
        self.api = api.API()

    def __str__(self):
        return self.name

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
        if value is not None:
            if not isinstance(value, str):
                raise TestRailError('input must be string or None')
        self._content['description'] = value

    @property
    def due_on(self):
        try:
            return datetime.fromtimestamp(int(self._content.get('due_on')))
        except TypeError:
            return None

    @due_on.setter
    def due_on(self, value):
        if value is None:
            due = None
        else:
            if not isinstance(value, datetime):
                raise TestRailError('input must be a datetime or None')
            due = int(time.mktime(value.timetuple()))
        self._content['due_on'] = due

    @property
    def id(self):
        return self._content.get('id')

    @property
    def is_completed(self):
        return bool(self._content.get('is_completed'))

    @is_completed.setter
    def is_completed(self, value):
        if not isinstance(value, bool):
            raise TestRailError('input must be a boolean')
        self._content['is_completed'] = value

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
