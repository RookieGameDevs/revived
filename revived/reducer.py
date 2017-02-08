"""TODO: add documentation.
"""

from functools import wraps


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


def combine_reducers(**reducers):
    def exec(prev, action):
        next = {}
        for key, r in reducers.items():
            next[key] = r(prev.get(key), action)
        return next

    return exec
