from functools import update_wrapper
import inspect

from singledispatch import singledispatch


class TestRailError(Exception):
    pass


def methdispatch(func):
    dispatcher = singledispatch(func)

    def wrapper(*args, **kw):
        try:
            return dispatcher.dispatch(args[1].__class__)(*args, **kw)
        except IndexError:
            return dispatcher.dispatch(args[0].__class__)(*args, **kw)
    wrapper.register = dispatcher.register
    update_wrapper(wrapper, func)
    return wrapper


def class_name(meth):
    for cls in inspect.getmro(meth.im_class):
        if meth.__name__ in cls.__dict__:
            return cls


def singleresult(func):
    def func_wrapper(*args, **kw):
        items = func(*args)
        if hasattr(items, '__iter__'):
            items = list(items)
        if len(items) > 1:
            raise TestRailError(
                'identifier "%s" returned multiple results' % args[1])
        elif len(items) == 0:
            raise TestRailError('identifier "%s" returned no result' % args[1])
        return items[0]
    return func_wrapper


class ContainerIter(object):
    def __init__(self, objs):
        self._objs = list(objs)
        self._index = 0

    def __iter__(self):
        return self

    def __len__(self):
        return len(self._objs)

    def __next__(self):
        return self.__next()

    def __next(self):
        if self._index == len(self._objs):
            raise StopIteration
        else:
            self._index += 1
            return self._objs[self._index-1]

    def next(self):
        return self.__next()


class UpdateCache(object):
    """ Decorator class for forcing cache to update by forcing the timestamp to
        be None
    """
    def __init__(self, cache):
        self.cache = cache

    def __call__(self, f):
        def wrapped_f(*args, **kwargs):
            resp = f(*args, **kwargs)
            if 'project_id' in resp:
                self.cache[resp['project_id']]['ts'] = None
            return resp
        return wrapped_f
