"""TODO: add documentation
"""

import copy
import uuid


class DispatchInReducerError(Exception):
    pass


class Store:
    def __init__(self, reducer):
        self._reducer = reducer
        self._state = None

        self._subscribers = {}
        self._is_reducing = False

    def subscribe(self, callback):
        key = uuid.uuid1()
        self._subscribers[key] = callback

        def unsubscribe():
            self._subscribers.pop(key, None)

        return unsubscribe

    def dispatch(self, action):
        if self._is_reducing:
            raise DispatchInReducerError
        self._is_reducing = True
        self._state = self._reducer(self.get_state(), action)
        self._is_reducing = False
        subscribers = copy.copy(self._subscribers)
        for cback in subscribers.values():
            cback()

    def get_state(self):
        return self._state
