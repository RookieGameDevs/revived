"""TODO: add documentation.
"""
from enum import Enum
from enum import unique
from functools import wraps
from typing import Any
from typing import Callable
from typing import Optional


@unique
class ActionType(str, Enum):
    pass


class Action(dict):
    def __init__(self, action_type: ActionType, data: Optional[dict[str, Any]]=None) -> None:
        super().__init__(**(data or {}))
        self.type = action_type


def action(action_type: ActionType) -> Callable[[Callable], Callable]:
    def wrap(f: Callable[..., dict]) -> Callable[..., Action]:
        @wraps(f)
        def wrapped(*args, **kwargs) -> Action:
            return Action(action_type, f(*args, **kwargs))
        return wrapped
    return wrap
