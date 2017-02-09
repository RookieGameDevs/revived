"""TODO: add documentation.
"""

from functools import wraps


class Module:
    def __init__(self):
        self._reducers = []

    def __call__(self, prev, action):
        next = prev
        for r in self._reducers:
            next = r(next, action)
        return next

    def reducer(self, action_type):
        def wrap(f):
            @wraps(f)
            def wrapped(prev, action):
                next = prev
                if action.type == action_type:
                    next = f(prev, action)
                return next
            self._reducers.append(wrapped)
            return wrapped
        return wrap


def reducer(action_type):
    def wrap(f):
        @wraps(f)
        def wrapped(prev, action):
            next = prev
            if action.type == action_type:
                next = f(prev, action)
            return next
        return wrapped
    return wrap


def combine_reducers(*top_reducers, **reducers):
    def reduce(prev, action):
        next = prev
        for r in top_reducers:
            next = r(next, action)
        for key, r in reducers.items():
            next[key] = r(next.get(key), action)
        return next

    return reduce
