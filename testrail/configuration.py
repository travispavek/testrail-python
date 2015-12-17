from project import Project
from helper import ContainerIter, methdispatch, singleresult


class _InnerConfig(object):
    def __init__(self, content=dict()):
        self._content = content

    @property
    def id(self):
        return self._content.get('id')

    @property
    def group_id(self):
        return self._content.get('group_id')

    @property
    def name(self):
        return self._content.get('name')


class Config(object):
    def __init__(self, content=None):
        self._content = content or dict()

    @property
    def id(self):
        return self._content.get('id')

    @property
    def name(self):
        return self._content.get('name')

    @property
    def project(self):
        return Project(self._content.get('project_id'))

    @property
    def configs(self):
        return _InnerConfigContainer(map(_InnerConfig, self._content.get('configs')))


class ConfigContainer(ContainerIter):
    def __init__(self, configs):
        super(ConfigContainer, self).__init__(configs)
        self._configs = configs

    @methdispatch
    @singleresult
    def group(self, gid):
        return filter(lambda g: g.id == gid, self._configs)

    @group.register(str)
    @singleresult
    def _group_by_name(self, gname):
        return filter(lambda g: g.name == gname, self._configs)


class _InnerConfigContainer(ContainerIter):
    def __init__(self, configs):
        super(_InnerConfigContainer, self).__init__(configs)
        self._configs = configs

    @singleresult
    def id(self, config_id):
        return filter(lambda c: c.id == config_id, self._configs)

    @singleresult
    def name(self, name):
        return filter(lambda c: c.name.lower() == name.lower(), self._configs)
