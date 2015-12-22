import collections
nested_dict = lambda: collections.defaultdict(nested_dict)


def reset_shared_state(cls):
    for key in cls._shared_state.keys():
        if key == '_timeout':
            cls._shared_state[key] = 30
        elif key == '_project_id':
            cls._shared_state[key] = None
        else:
            cls._shared_state[key] = nested_dict()
