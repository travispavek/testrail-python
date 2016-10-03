from testrail.base import TestRailBase


class Status(TestRailBase):
    def __init__(self, content):
        self._content = content

    @property
    def id(self):
        return self._content.get('id')

    @property
    def name(self):
        return self._content.get('name')

    @property
    def label(self):
        return self._content.get('label')

    @property
    def is_untested(self):
        return self._content.get('is_untested')

    @property
    def is_system(self):
        return self._content.get('is_system')

    @property
    def is_final(self):
        return self._content.get('is_final')

    @property
    def color_medium(self):
        return self._content.get('color_medium')

    @property
    def color_dark(self):
        return self._content.get('color_dark')

    @property
    def color_bright(self):
        return self._content.get('color_bright')
