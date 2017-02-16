"""
This module implements helper functions and classes that can be used to define
``actions`` and ``action creators``, in the same fashion of redux ones, but
using decorators instead of anonymous functions.

Actions and action creators
===========================

Actions are payloads of information that send data from your application to your
``store``. They are the only source of information for the ``store``. You send
them to the store using :any:`revived.store.Store.dispatch`.

Actions are instances of :any:`revived.action.Action`. They have a type
property. Types should be defined in an enum inheriting
:any:`revived.action.ActionType`. Once your app is large enough, you may want to
move them into a separate module.

Action creators are exactly that: functions that create ``actions``. It's easy
to conflate the terms ``action`` and ``action creator``, so do your best to use
the *proper term*.

Define action types
===================

While you are free to define the action type enum as he prefers, it is
**strongly suggested** to write them down in this way:

.. code:: python

    from revived.actions import ActionType as BaseActionType

    # custom action types enum
    class ActionType(BaseActionType):
        AN_ACTION_TYPE = 'an_action_type'


Define action creators
======================

While it is possible to explicitly build :any:`revived.action.Action` instances
directly, it is **strongly suggested** to create ``actions`` using ``action
creators``.

Assuming you are in the same module of the ``action types`` defined previously,
you can define ``action creators`` in this way:

.. code:: python

    # define the action creator that takes two arguments and returns a
    # dictionary with those arguments in an arbitrary way.
    @action(ActionTypes.AN_ACTION_TYPE)
    def an_action_type_with_parameters(param1, param2):
        return {'1': param1, '2': param2}

    # create the action object
    action_obj = an_action_type_with_parameters(1, 2)
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
    # FIXME: this method is added to avoid sphinx_autodoc_typehints errors:
    # see https://github.com/agronholm/sphinx-autodoc-typehints/issues/12
    def __init__(*args, **kwargs):
        pass


class Action(dict):
    """Structure that stores all the required data for an action.

    Redux actions are plain objects - ie: python dicts - but having a specific
    class here helps for type hinting. The rationale behind this is that we
    store the type as ``metadata`` instead of part of the action data itself.

    While ``action_type`` is going to be stored as ``metadata``, the
    :any:`revived.action.Action` instance itself is going to behave exactly as a
    dict, with all the action data inside.

    :param action_type: The type of the action.
    :param data: An optional dict containing data. No restriction on depth
        and members type, as long as the keys are strings.
    """

    def __init__(self, action_type: ActionType, data: Optional[Dict[str, Any]]=None) -> None:
        super().__init__(**(data or {}))
        self.type = action_type


def action(action_type: ActionType) -> Callable[[Callable], Callable]:
    """Decorator function to use as an ``action creator`` factory.

    This helper function is used to create action creators. The idea behind this
    is that we just want to define the relevant data as a ``dict``, instead of
    complex objects. This decorator will take care of simple-dict-returning
    functions preparing the proper :any:`revived.action.Action` instance that
    is needed by the revived API.

    :param action_type: The type of the action.
    :returns: The ``action creator``.
    """
    def wrap(f: Callable[..., Dict]) -> Callable[..., Action]:
        @wraps(f)
        def wrapped(*args, **kwargs) -> Action:
            return Action(action_type, f(*args, **kwargs))
        return wrapped
    return wrap
