import api
from suite import Suite


class Section(object):
    def __init__(self, content):
        self._content = content
        self.api = api.API()

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

    @property
    def parent(self):
        return self._content.get('parent_id')

    @property
    def name(self):
        return self._content.get('name')

    @property
    def suite(self):
        s = self.api.suite_with_id(self._content.get('suite_id'))
        if s:
            return Suite(s)
        return None
