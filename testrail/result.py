from datetime import datetime, timedelta
import re

from testrail.base import TestRailBase
from testrail import api
from testrail.helper import custom_methods, ContainerIter, TestRailError
from testrail.status import Status
from testrail.test import Test
from testrail.user import User
from testrail.helper import testrail_duration_to_timedelta


class Result(TestRailBase):
    def __init__(self, content=None):
        self._content = content or dict()
        self.api = api.API()
        self._custom_methods = custom_methods(self._content)

    def __getattr__(self, attr):
        if attr in self._custom_methods:
            return self._content.get(self._custom_methods[attr])
        raise AttributeError("'{}' object has no attribute '{}'".format(
            self.__class__.__name__, attr))

    @property
    def assigned_to(self):
        user_id = self._content.get('assignedto_id')
        return User(self.api.user_with_id(user_id)) if user_id else User()

    @assigned_to.setter
    def assigned_to(self, user):
        if not isinstance(user, User):
            raise TestRailError('input must be a User object')
        try:
            self.api.user_with_id(user.id)
        except TestRailError:
            raise TestRailError("User with ID '%s' is not valid" % user.id)
        self._content['assignedto_id'] = user.id

    @property
    def comment(self):
        return self._content.get('comment')

    @comment.setter
    def comment(self, value):
        if not isinstance(value, str):
            raise TestRailError('input must be a string')
        self._content['comment'] = value

    @property
    def created_by(self):
        return User(self.api.user_with_id(self._content.get('created_by')))

    @property
    def created_on(self):
        try:
            return datetime.fromtimestamp(int(self._content.get('created_on')))
        except TypeError:
            return None

    @property
    def defects(self):
        defects = self._content.get('defects')
        return defects.split(',') if defects else list()

    @defects.setter
    def defects(self, values):
        if not isinstance(values, list):
            raise TestRailError('input must be a list of strings')
        if not all(map(lambda x, : isinstance(x, str), values)):
            raise TestRailError('input must be a list of strings')
        if len(values) > 0:
            self._content['defects'] = ','.join(values)
        else:
            self._content['defects'] = None

    @property
    def elapsed(self):
        duration = self._content.get('elapsed')
        if duration is None:
            return None

        if isinstance(duration, int):
            return timedelta(seconds=duration)
        return testrail_duration_to_timedelta(duration)

    @elapsed.setter
    def elapsed(self, td):
        if not isinstance(td, timedelta):
            raise TestRailError('input must be a timedelta')
        if td > timedelta(weeks=10):
            raise TestRailError('maximum elapsed time is 10 weeks')
        self._content['elapsed'] = td.seconds

    @property
    def id(self):
        return self._content.get('id')

    @property
    def status(self):
        return Status(self.api.status_with_id(self._content.get('status_id')))

    @status.setter
    def status(self, status_obj):
        # TODO: Should I accept string name as well?
        if not isinstance(status_obj, Status):
            raise TestRailError('input must be a Status')
        # verify id is valid
        self.api.status_with_id(status_obj.id)
        self._content['status_id'] = status_obj.id

    @property
    def test(self):
        test_id = self._content.get('test_id')
        return Test(self.api.test_with_id(test_id)) if test_id else Test()

    @test.setter
    def test(self, test_obj):
        if not isinstance(test_obj, Test):
            raise TestRailError('input must be a Test')
        # verify id is valid
        self.api.test_with_id(
            test_obj._content['id'], test_obj._content['run_id'])
        self._content['test_id'] = test_obj.id

    @property
    def version(self):
        return self._content.get('version')

    @version.setter
    def version(self, ver):
        if not isinstance(ver, str):
            raise TestRailError('input must be a string')
        self._content['version'] = ver

    def raw_data(self):
        return self._content


class ResultContainer(ContainerIter):
    def __init__(self, results):
        super(ResultContainer, self).__init__(results)
        self._results = results

    def blocked(self):
        return list(filter(lambda r: r.status.name == "blocked", self._results))

    def failed(self):
        return list(filter(lambda r: r.status.name == "failed", self._results))

    def latest(self):
        return sorted(self._results, key=lambda r: r.created_on)[-1]

    def oldest(self):
        return sorted(self._results, key=lambda r: r.created_on)[0]

    def passed(self):
        return list(filter(lambda r: r.status.name == "passed", self._results))

    def retest(self):
        return list(filter(lambda r: r.status.name == "retest", self._results))

    def untested(self):
        return list(filter(lambda r: r.status.name == "untested", self._results))
