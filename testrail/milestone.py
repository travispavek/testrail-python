from datetime import datetime
from project import Project
import api
import time
from helper import ContainerIter


class Milestone(object):
    def __init__(self, content=None):
        self._content = content or dict()
        self.api = api.API()

    @property
    def completed_on(self):
        try:
            return datetime.fromtimestamp(int(self._content.get('created_on')))
        except TypeError:
            return None

    @property
    def description(self):
        return self._content.get('description')

    @description.setter
    def description(self, value):
        self._content['description'] = value

    @property
    def due_on(self):
        try:
            return datetime.fromtimestamp(int(self._content.get('due_on')))
        except TypeError:
            return None

    @due_on.setter
    def due_on(self, value):
        self._content['due_on'] = int(time.mktime(value.timetuple()))

    @property
    def id(self):
        return self._content.get('id')

    @property
    def is_completed(self):
        return bool(self._content.get('is_completed'))

    @is_completed.setter
    def is_completed(self, value):
        self._content['is_completed'] = value

    @property
    def name(self):
        return self._content.get('name')

    @name.setter
    def name(self, value):
        self._content['name'] = value

    @property
    def project(self):
        try:
            return Project(self.api.project_with_id(self._content.get('project_id')))
        except IndexError:
            return None

    @project.setter
    def project(self, value):
        self._content['project_id'] = value.id

    @property
    def url(self):
        return self._content.get('url')

    def raw_data(self):
        return self._content
