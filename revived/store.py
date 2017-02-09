"""TODO: add documentation
"""
from .action import action
from .action import Action
from .action import ActionType as BaseActionType
from .reducer import Reducer
from typing import Any
from typing import Callable
import copy
import uuid


class ActionType(BaseActionType):
    INIT = 'init'


@action(ActionType.INIT)
def init():
    pass


class DispatchInReducerError(Exception):
    pass


class Store:
    def __init__(self, reducer: Reducer) -> None:
        self._reducer = reducer
        self._state = None  # type: Any

        self._subscribers = {}  # type: dict[uuid.UUID, Callable[[], None]]
        self._is_reducing = False

        self.dispatch(init())

    def subscribe(self, callback: Callable[[], None]) -> Callable[[], None]:
        key = uuid.uuid1()
        self._subscribers[key] = callback

        def unsubscribe():
            self._subscribers.pop(key, None)

        return unsubscribe

    def dispatch(self, action: Action) -> None:
        if self._is_reducing:
            raise DispatchInReducerError
        self._is_reducing = True
        self._state = self._reducer(self.get_state(), action)
        self._is_reducing = False
        subscribers = copy.copy(self._subscribers)
        for cback in subscribers.values():
            cback()

    def get_state(self) -> Any:
        return self._state
