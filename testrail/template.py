class Template(object):
    def __init__(self, content):
        self._content = content

    @property
    def id(self):
        return self._content.get('id')

    @property
    def name(self):
        return self._content.get('name')

    @property
    def is_default(self):
        return self._content.get('is_default')
