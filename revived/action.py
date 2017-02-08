from enum import Enum
from enum import unique
from functools import wraps


@unique
class ActionType(str, Enum):
    pass


class Action(dict):
    def __init__(self, action_type, data=None):
        super().__init__(**(data or {}))
        self.type = action_type


def action(action_type):
    def wrap(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            return Action(action_type, f(*args, **kwargs))
        return wrapped
    return wrap
