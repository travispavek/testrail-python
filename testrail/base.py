class TestRailBase(object):
    """ Base class for all TestRail objects with a TestRail ID
    """
    def __str__(self):
        class_name = self.__class__.__name__
        return "{0}-{1}".format(class_name, self.id)

    def __repr__(self):
        return str(self)
