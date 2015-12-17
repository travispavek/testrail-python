import api
from project import Project
from datetime import datetime


class Suite(object):
    def __init__(self, content):
        self._content = content
        self.api = api.API()

    @property
    def id(self):
        return self._content.get('id')

    @property
    def completed_on(self):
        try:
            return datetime.fromtimestamp(int(self._content.get('completed_on')))
        except TypeError:
            return None

    @property
    def description(self):
        return self._content.get('description')

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

    @property
    def project(self):
        return Project(self.api.project_with_id(self._content.get('project_id')))

    @property
    def url(self):
        return self._content.get('url')
