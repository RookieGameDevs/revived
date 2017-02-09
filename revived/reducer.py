"""Reducer module.

This module implements helper functions and classes that can be used to define
reducers in the same fashion of redux ones, but using decorators instead of
anonymous functions.
"""
from .action import Action
from .action import ActionType
from functools import wraps
from typing import Any
from typing import Callable
from typing import List

Reducer = Callable[[Any, Action], Any]
ReducerList = List[Reducer]


class Module:
    """Helper class for module creations.

    This is just an helper class: you can obtain the same result using the
    reducer decorator and then combining all the defined reducers as top-level
    reducers. The module instance will work exactly as a reducer function, but
    will call all the registered reducers. The call order is not guaranteed.

    This snippet:

        module_reducer = Module()

        @mod.reduder(ActionType.DUMMY_ACTION_TYPE1)
        def dummy1(prev, action):
            next = prev
            # Do something
            return next

        @mod.reduder(ActionType.DUMMY_ACTION_TYPE2)
        def dummy2(prev, action):
            next = prev
            # Do something
            return next

    has exactly the same result of:

        @reducer(ActionType.DUMMY_ACTION_TYPE1)
        def dummy1(prev, action):
            next = prev
            # Do something
            return next

        @reducer(ActionType.DUMMY_ACTION_TYPE2)
        def dummy2(prev, action):
            next = prev
            # Do something
            return next

        module_reducer = combine_reducers(dummy1, dummy2)
    """

    def __init__(self) -> None:
        """Constructor.

        Creates a module - ie. an aggregate of reducers - that works like a
        single reducer on a specific state.
        """
        self._reducers = []  # type:
        ReducerList

    def __call__(self, prev: Any, action: Action):
        """Lets the module work like a reducer.

        :param pref: The previous state.
        :param action: The action performed.
        :returns: The next state.
        """
        next = prev
        for r in self._reducers:
            next = r(next, action)
        return next

    def reducer(self, action_type: ActionType) -> Callable[[Reducer], Reducer]:
        """Decorator function to create a reducer.

        Creates a reducer attached to the module. This reducer is handling the
        specified action type and it is going to be ignored in case the action
        is of a different type.

        :param action_type: The action type.
        :returns: The reducer function.
        """
        def wrap(f: Reducer) -> Reducer:
            @wraps(f)
            def wrapped(prev: Any, action: Action) -> Reducer:
                next = prev
                if action.type == action_type:
                    next = f(prev, action)
                return next
            self._reducers.append(wrapped)
            return wrapped
        return wrap


def reducer(action_type: ActionType) -> Callable[[Reducer], Reducer]:
    """Decorator function to create a reducer.

    Creates a reducer. This reducer is handling the specified action type and it
    is going to be ignored in case the action is of a different type.

    :param action_type: The action type. :returns: The reducer function.
    :returns: The reducer function.
    """
    def wrap(f: Reducer) -> Reducer:
        @wraps(f)
        def wrapped(prev: Any, action: Action) -> Reducer:
            next = prev
            if action.type == action_type:
                next = f(prev, action)
            return next
        return wrapped
    return wrap


def combine_reducers(*top_reducers: Reducer, **reducers: Reducer) -> Reducer:
    """Create a reducer combining the reducers passed as parameters.

    It is possible to use this function to combine top-level reducers or to
    assign to reducers a specific subpath of the state. The result is a reducer,
    so it is possible to combine the resulted function with other reducers
    creating at-will complex reducer trees.

    :param top_reducers: An optional list of top-level reducers.
    :param reducers: An optional list of reducers that will handle a subpath.
    :returns: The combined reducer function.
    """
    def reduce(prev: Any, action: Action) -> Any:
        next = prev
        for r in top_reducers:
            next = r(next, action)
        for key, r in reducers.items():
            next[key] = r(next.get(key), action)
        return next

    return reduce
