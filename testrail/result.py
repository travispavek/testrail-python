from datetime import datetime, timedelta
import re

import api
from helper import TestRailError
from status import Status
from test import Test
from user import User


class Result(object):
    def __init__(self, content=None):
        self._content = content or {}
        self.api = api.API()

    @property
    def assigned_to(self):
        return User(self.api.user_with_id(self._content.get('assignedto_id')))

    @assigned_to.setter
    def assigned_to(self, user):
        if type(user) != User:
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
        if type(value) != str:
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
        if type(values) != list:
            raise TestRailError('input must be a list of strings')
        if not all(map(lambda x: type(x) == str, values)):
            raise TestRailError('input must be a list of strings')
        if len(values) > 0:
            self._content['defects'] = ','.join(values)
        else:
            self._content['defects'] = None

    @property
    def elapsed(self):
        span = lambda x: int(x.group(0)[:-1]) if x else 0
        ts = self._content.get('elapsed')
        if ts is None:
            return None
        duration = {
            'weeks': span(re.search('\d+w', ts)),
            'days': span(re.search('\d+d', ts)),
            'hours': span(re.search('\d+h', ts)),
            'minutes': span(re.search('\d+m', ts)),
            'seconds': span(re.search('\d+s', ts))
        }
        return timedelta(**duration)

    @elapsed.setter
    def elapsed(self, td):
        if type(td) != timedelta:
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
        if type(status_obj) != Status:
            raise TestRailError('input must be a Status')
        # verify id is valid
        self.api.status_with_id(status_obj.id)
        self._content['status_id'] = status_obj.id

    @property
    def test(self):
        return Test(self.api.test_with_id(self._content.get('test_id')))

    @test.setter
    def test(self, obj):
        self._content['test_id'] = obj.id

    @property
    def version(self):
        return self._content.get('version')

    @version.setter
    def version(self, value):
        self._content['version'] = value

    def raw_data(self):
        return self._content
