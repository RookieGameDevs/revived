"""Action module.

This module implements helper functions and classes that can be used to define
actions and action creators, in the same fashion of redux ones, but using
decorators instead of anonymous functions.
"""
from enum import Enum
from enum import unique
from functools import wraps
from typing import Any
from typing import Callable
from typing import Dict
from typing import Optional


@unique
class ActionType(str, Enum):
    """Action type base class.

    The idea behind this class is to use an unique enum to store action types
    for each module. Usually there would be no need for such a feature-less
    class, but it is pretty handy while using type hints.
    """
    pass


class Action(dict):
    """Structure that stores all the required data for an action.

    Redux actions are plain objects - ie: python dicts - but having a specific
    class here helps for type hinting. The rationale behind this is that we
    store the type as *metadata* instead of part of the action data itself.
    """

    def __init__(self, action_type: ActionType, data: Optional[Dict[str, Any]]=None) -> None:
        """Constructor.

        Builds an action using the specified action type and optional data.
        While action_type is going to be stored as *metadata*, the Action object
        itself is going to behave exactly as a dict, with all the action data
        inside.

        :param action_type: The type of the action.
        :param data: An optional dict containing data. No restriction on depth
            and members type, as long as the keys are strings.
        """
        super().__init__(**(data or {}))
        self.type = action_type


def action(action_type: ActionType) -> Callable[[Callable], Callable]:
    """Decorator function to use as an *action creator* factory.

    This helper function is used to create action creators. The idea behind this
    is that we just want to define the relevant data as a dict, instead of
    complex objects. This decorator will take care of simple-dict-returing
    functions preparing the proper Action object that is needed by the revived
    API.

    :param action_type: The type of the action.
    :returns: The action creator.
    """
    def wrap(f: Callable[..., Dict]) -> Callable[..., Action]:
        @wraps(f)
        def wrapped(*args, **kwargs) -> Action:
            return Action(action_type, f(*args, **kwargs))
        return wrapped
    return wrap
