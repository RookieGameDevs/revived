"""TODO: add documentation.
"""


def create_reducer(action_type, r):
    def red(prev, action):
        next = prev
        if action['type'] == action_type:
            next = r(prev, action)
        return next
    return red


def reducer(action_type):
    def wrapper(r):
        return create_reducer(action_type, r)
    return wrapper


def combine_reducers(**reducers):
    def exec(prev, action):
        next = {}
        for key, r in reducers.items():
            next[key] = r(prev.get(key), action)
        return next

    return exec
