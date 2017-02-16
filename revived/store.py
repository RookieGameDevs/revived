"""
This module implements the **global state store**, and the ``INIT`` action and
action_creator. This is the entry point of the revived module.

Rationale behind the ``Store``
==============================

:any:`revived.store.Store` is the object that brings ``actions`` and
``reducers``. The store has the following responsibilities:

* Holds application state;
* Allows access to state via :any:`revived.store.Store.get_state`;
* Allows state to be updated via :any:`revived.store.Store.dispatch`;
* Registers listeners via :any:`revived.store.Store.subscribe` or
  :any:`revived.store.Store.subscriber` decorator;
* Handles unregistering of listeners via the function returned by
  :any:`revived.store.Store.subscribe` or via the property
  :any:`revived.store.Subscriber.unsubscribe` of the
  :any:`revived.store.Subscriber` instance.

It's important to note that you'll only have a single store in your application.
When you want to split your data handling logic, you'll use ``reducer``
composition instead of many stores.

Dispatch actions
================

To dispatch actions the :any:`revived.store.Store.dispatch` method should be
used, passing as parameter the result of an action_creator. See more in
:any:`revived.action.action` and :any:`revived.action.Action`.

.. code:: python

    # create the store object
    store = Store(root_reducer)

    # register subscribers
    # ...

    # dispatch an action using the action_creator <an_action_creator>
    store.dispatch(an_action_creator(a_parameter, another_parameter))

Subscribe and unsubscribe to state changes
==========================================

There are two ways to **subscribe** and **usubscribe** to store changes: using
the :any:`revived.store.Store.subscribe` method or the
:any:`revived.store.Store.subscriber` decorator. Both approaches are equivalent
and the choice should be just made based on your taste.

Subscribe using :any:`revived.store.Store.subscribe`
----------------------------------------------------

.. code:: python

    # create the store object
    store = Store(root_reducer)

    # define the function
    def a_subscriber():
        # do something!
        pass

    # subscribe the function
    unsubscribe = store.subscribe(a_subscriber)

    # unsubscribe the function
    unsubscribe()

Subscribe using :any:`revived.store.Store.subscriber`
-----------------------------------------------------

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
"""
from .action import action
from .action import Action
from .action import ActionType as BaseActionType
from .reducer import Module
from .reducer import Reducer
from typing import Any
from typing import Callable
from typing import Union
import copy
import uuid


class ActionType(BaseActionType):
    """Action types for the store module.

    Basically the only type here is the ``INIT`` one. Reducers should wait for
    this action to create the initial state for the state subpath they are
    responsible of.
    """
    INIT = 'init'


@action(ActionType.INIT)
def init():
    """Action creator for the init action.
    """
    pass


class DispatchInReducerError(Exception):
    """Raised when :any:`revived.store.Store.dispatch` is called in a reducer.
    """
    # FIXME: this method is added to avoid sphinx_autodoc_typehints errors:
    # see https://github.com/agronholm/sphinx-autodoc-typehints/issues/12
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Subscriber:
    """Wrapper around a subscriber function with the ``unsubscribe`` property.

    While creating a subscriber using the decorator it is not possible to return
    the ``unsubscribe`` function. So a :any:`revived.store.Subscriber` is
    created wrapping the callback, that contains the
    :any:`revived.store.Subscriber.unsubscribe` function to be used to properly
    unregister the subscriber.

    :param callback: The callback to be wrapped into the subscriber.
    :param unsubscribe: The unsubscribe function for the subscriber.
    """

    def __init__(self, callback: Callable[[], None], unsubscribe: Callable[[], None]) -> None:
        self.callback = callback
        self._unsubscribe = unsubscribe

    def __call__(self) -> None:
        """Calls the wrapped subscriber.
        """
        self.callback()

    @property
    def unsubscribe(self) -> Callable[[], None]:
        """Property containing the ``unsubscribe`` function.

        :returns: The ``unsubscribe`` function for the subscriber.
        """
        return self._unsubscribe


class Store:
    """Container object for the global state.

    This object is responsible of the global state. Its main responsibilities
    are:

    * Keeping track of all the *subscribers*, and call them on **state
      changes**.
    * Keeping reference to the *reducer* to be used and call it to properly
      handle **state changes**.

    Creates the store, using the given function as ``reducer``. At the
    beginning no callback is subscribed to *store changes*. It is possible
    to add subscribers later, while there is no way - *at the moment* - to
    replace the reducer.

    :param reducer: The root reducer.
    """

    def __init__(self, reducer: Union[Reducer, Module]) -> None:
        self._reducer = reducer
        self._state = None  # type: Any

        self._subscribers = {}  # type: dict[uuid.UUID, Callable[[], None]]
        self._is_reducing = False

        self.dispatch(init())

    def subscribe(self, callback: Callable[[], None]) -> Callable[[], None]:
        """Subscribes a callback to *state changes*.

        Every time the state changes, the callback is called. No parameters are
        passed to the callback. It is responsibility of the callback to actually
        connect the store with the caller. The returned function can be called
        without arguments to unsubscribe the callback.

        :param callback: The callback to be subscribed.
        :returns: The unsubscribe function.
        """
        key = uuid.uuid1()
        self._subscribers[key] = callback

        def unsubscribe() -> None:
            self._subscribers.pop(key, None)

        return unsubscribe

    def subscriber(self, callback: Callable[[], None]) -> Subscriber:
        """Decorator function to subscribe a function to *store changes*.

        The subscribed function will be called every time the internal state of
        the store changes.

        **NOTE: The decorator function will return the function itself**. To
        unsubscribe the callback the user should use the
        :any:`revived.store.Subscriber.unsubscribe` function attached into the
        callback.

        :param callback: The callback to be subscribed. :returns: The callback
            itself.
        :returns: The wrapping subscriber.
        """
        unsubscribe = self.subscribe(callback)
        s = Subscriber(callback, unsubscribe)
        return s

    def dispatch(self, action: Action) -> None:
        """Dispatches an ``action``.

        This is the only piece of code responsible of *dispatching actions*.
        When an ``action`` is dispatched, the state is changed according to the
        defined root reducer and all the subscribers are called.

        **The calling order is not guaranteed**.

        :param action: The ``action`` that should be dispatched.
        :raises: :class:`revived.store.DispatchInReducerError`
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
        """Getter for the global state.

        :returns: The global state contained into the store.
        """
        return self._state
