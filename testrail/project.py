from datetime import datetime

from testrail.base import TestRailBase
from testrail.helper import ContainerIter, TestRailError


class Project(TestRailBase):
    def __init__(self, response=None):
        self._content = response or dict()

    def __str__(self):
        return self.name

    @property
    def announcement(self):
        """The description/announcement of the project"""
        return self._content.get('announcement')

    @announcement.setter
    def announcement(self, msg):
        if not isinstance(msg, str):
            raise TestRailError('input must be a string')
        self._content['announcement'] = msg

    @property
    def completed_on(self):
        """The date/time when the project was marked as completed"""
        if self.is_completed:
            return datetime.fromtimestamp(self._content.get('completed_on'))
        return None

    @property
    def id(self):
        """The unique ID of the project"""
        return self._content.get('id')

    @property
    def is_completed(self):
        """True if the project is marked as completed and false otherwise"""
        return self._content.get('is_completed', False)

    @is_completed.setter
    def is_completed(self, value):
        if not isinstance(value, bool):
            raise TestRailError('input must be a boolean')
        self._content['is_completed'] = value

    @property
    def name(self):
        """The name of the project"""
        return self._content.get('name')

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TestRailError('input must be a string')
        self._content['name'] = value

    @property
    def show_announcement(self):
        """True to show the announcement/description and false otherwise"""
        return self._content.get('show_announcement', False)

    @show_announcement.setter
    def show_announcement(self, value):
        if not isinstance(value, bool):
            raise TestRailError('input must be a boolean')
        self._content['show_announcement'] = value

    @property
    def suite_mode(self):
        """The suite mode of the project (1 for single suite mode,
           2 for single suite + baselines, 3 for multiple suites)
           (added with TestRail 4.0)
        """
        return self._content.get('suite_mode')

    @suite_mode.setter
    def suite_mode(self, mode):
        if not isinstance(mode, int):
            raise TestRailError('input must be an integer')
        if mode not in [1, 2, 3]:
            raise TestRailError('input must be a 1, 2, or 3')
        self._content['suite_mode'] = mode

    @property
    def url(self):
        """The address/URL of the project in the user interface"""
        return self._content.get('url')


class ProjectContainer(ContainerIter):
    def __init__(self, projects):
        super(ProjectContainer, self).__init__(projects)
        self._projects = projects

    def __iter__(self):
        return iter(self._projects)

    def __len__(self):
        return len(self._projects)

    def __getitem__(self, i):
        return self._projects[i]

    def completed(self):
        return filter(lambda p: p.is_completed is True, self._projects)

    def active(self):
        return filter(lambda p: p.is_completed is False, self._projects)
