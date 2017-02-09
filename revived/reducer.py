"""TODO: add documentation.
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
    def __init__(self) -> None:
        self._reducers = []  # type: ReducerList

    def __call__(self, prev: Any, action: Action):
        next = prev
        for r in self._reducers:
            next = r(next, action)
        return next

    def reducer(self, action_type: ActionType) -> Callable[[Reducer], Reducer]:
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
    def reduce(prev: Any, action: Action) -> Any:
        next = prev
        for r in top_reducers:
            next = r(next, action)
        for key, r in reducers.items():
            next[key] = r(next.get(key), action)
        return next

    return reduce
