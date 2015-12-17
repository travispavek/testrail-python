class User(object):
    def __init__(self, content={}):
        self._content = content

    @property
    def email(self):
        return self._content.get('email')

    @property
    def id(self):
        return self._content.get('id')

    @property
    def is_active(self):
        return bool(self._content.get('is_active'))

    @property
    def name(self):
        return self._content.get('name')
