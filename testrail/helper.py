from singledispatch import singledispatch
from functools import update_wrapper
import inspect


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
        if len(items) > 1:
            raise TestRailError('identifier "%s" returned multiple results' % args[1])
        elif len(items) == 0:
            raise TestRailError('identifier "%s" returned no result' % args[1])
        return items[0]
    return func_wrapper


class ContainerIter(object):
    def __init__(self, objs):
        self._objs = objs
        self._index = 0

    def __iter__(self):
        return self

    def next(self):
        if self._index == len(self._objs):
            raise StopIteration
        else:
            self._index += 1
            return self._objs[self._index-1]
