import re
import inspect
from datetime import timedelta
from functools import update_wrapper

from singledispatch import singledispatch


class TestRailError(Exception):
    pass


class TooManyRequestsError(TestRailError):
    pass


class ServiceUnavailableError(TestRailError):
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


def testrail_duration_to_timedelta(duration):
        span = lambda x: int(x.group(0)[:-1]) if x else 0
        timedelta_map = {
            'weeks': span(re.search('\d+w', duration)),
            'days': span(re.search('\d+d', duration)),
            'hours': span(re.search('\d+h', duration)),
            'minutes': span(re.search('\d+m', duration)),
            'seconds': span(re.search('\d+s', duration))
        }
        return timedelta(**timedelta_map)


def singleresult(func):
    def func_wrapper(*args, **kw):
        items = func(*args)
        if hasattr(items, '__iter__'):
            items = list(items)
        if len(items) > 1:
            raise TestRailError(
                'identifier "%s" returned multiple results' % args[1])
        elif len(items) == 0:
            return None
            #raise TestRailError('identifier "%s" returned no result' % args[1])
        return items[0]
    return func_wrapper


class ContainerIter(object):
    def __init__(self, objs):
        self._objs = list(objs)

    def __len__(self):
        return len(self._objs)

    def __getitem__(self, index):
        return self._objs[index]


custom_methods_re = re.compile(r'^custom_(\w+)')


def custom_methods(content):
    matches = [custom_methods_re.match(method) for method in content]
    return dict({match.group(1): match.group(0) for match in matches if match})

