from testrail.base import TestRailBase
from testrail.api import API
from testrail.run import Run
from testrail.suite import Suite


class EntryRun(Run):
    def __init__(self, content):
        super(EntryRun, self).__init__(content)

    @property
    def entry_id(self):
        return self._content.get('entry_id')

    @property
    def entry_index(self):
        return self._content.get('entry_index')


class Entry(TestRailBase):
    def __init__(self, content):
        self._content = content
        self._api = API()

    @property
    def id(self):
        return self._content.get('id')

    @property
    def name(self):
        return self._content.get('name')

    @property
    def runs(self):
        return list(map(EntryRun, self._content.get('runs')))

    @property
    def suite(self):
        return Suite(self._api.suite_with_id(self._content.get('suite_id')))
