from testrail.base import TestRailBase


class User(TestRailBase):
    def __init__(self, content=None):
        self._content = content or dict()

    def __str__(self):
        return '%s <%s>' % (self.name, self.id)

    @property
    def email(self):
        return self._content.get('email')

    @property
    def id(self):
        return self._content.get('id')

    @property
    def is_active(self):
        return self._content.get('is_active')

    @property
    def name(self):
        return self._content.get('name')
