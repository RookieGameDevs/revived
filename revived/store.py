"""Store module.

This module implements the global state store, and the init action and
action_creator. This is the entry point of the revived module.
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
    """Action types for the store module.

    Basically the only type here is the **INIT** one. Reducers should wait for
    this action to create the initial state for the state subpath they are
    responsible of.
    """
    INIT = 'init'


@action(ActionType.INIT)
def init():
    """Action creator for the init aciton.
    """
    pass


class DispatchInReducerError(Exception):
    """Exception raised when a dispatch is called inside a reducer.
    """
    pass


class Store:
    """Container object of the global state.

    This object is responsible of the global state. Its main responsibilities
    are:
    * Keeping track of all the subscribers, and call them on state changes.
    * Keeping reference to the reducer to be used and call it to proprly handle
      state changes.
    """
    def __init__(self, reducer: Reducer) -> None:
        """Constructor.

        Creates the store, using the given function as reducer. At the beginning
        no callback is subscribed to store changes. It is possible to add
        subscribers later, while there is no way - at the moment - to replace
        the reducer.

        :param reducer: The root reducer.
        """
        self._reducer = reducer
        self._state = None  # type: Any

        self._subscribers = {}  # type: dict[uuid.UUID, Callable[[], None]]
        self._is_reducing = False

        self.dispatch(init())

    def subscribe(self, callback: Callable[[], None]) -> Callable[[], None]:
        """Subscribes a callback to state changes.

        Every time the state changes, the callback is called. No parameters are
        passed to the callback. It is responsibility of the store handler to
        actually connect the store with the caller. The returned function can be
        called without arguments to unsubscribe the callback.

        :param callback: The callback to be subscribed.
        :returns: The unsubscribe functions.
        """
        key = uuid.uuid1()
        self._subscribers[key] = callback

        def unsubscribe():
            self._subscribers.pop(key, None)

        return unsubscribe

    def subscriber(self, callback: Callable[[], None]) -> Callable[[], None]:
        """Decorator function to subscribe a function to store changes.

        The subscribed function will be called every time the internal state of
        the store changes.

        NOTE: The decorator function will return the function itself. To
        unsubscribe the callback the user should use the *unsubscribe* function
        attached into the callback.

        .. code:: python

            # create the store object
            store = Store(root_reducer)

            # define and subscribe the function
            @store.subscriber
            def a_subscriber():
                # do something!
                pass

            # unsubscribe the function
            a_subscriber.unsubscribe()

        :param callback: The callback to be subscribed. :returns: The callback
        itself.
        """
        unsubscribe = self.subscribe(callback)
        callback.unsubscribe = unsubscribe
        return callback

    def dispatch(self, action: Action) -> None:
        """Dispatches an action.

        This is the only piece of code responsible of dispatching actions. When
        an action is dispatched, the state is changed according to the defined
        root reducer and all the subscribers are called. *The calling order is
        not guaranteed.

        :param action: The action that should be dispatched.
        """
        if self._is_reducing:
            raise DispatchInReducerError
        self._is_reducing = True
        self._state = self._reducer(self.get_state(), action)
        self._is_reducing = False
        subscribers = copy.copy(self._subscribers)
        for cback in subscribers.values():
            cback()

    def get_state(self) -> Any:
        """Returns the global state contained into the store.
        """
        return self._state
