"""
This module implements helper functions and classes that can be used to define
reducers in the same fashion of redux ones, but using decorators instead of
anonymous functions.

Things you **should never do** inside a reducer:

* Mutate its arguments;
* Perform side effects like API calls and routing transitions;
* Call **non-pure** functions.

**Given the same arguments, it should calculate the next state and return it. No
surprises. No side effects. No API calls. No mutations. Just a calculation.**

Create a reducer
================

A reducer is a function that looks like this:

.. code:: python

    def dummy(prev, action):
        next = prev
        if action.type == ActionType.DUMMY_ACTION_TYPE:
            # Do something
            return next

In order to decrease the amount of required boilerplate ``revived`` makes use of
a lot of python goodies, especially **decorators**.

While every function can be used as ``reducer`` (as long as it takes the proper
parameters), the easiest way to create a ``reducer`` that handles a specific
type of ``actions`` is to use the :any:`revived.reducer.reducer` decorator.

.. code:: python

    @reducer(ActionType.DUMMY_ACTION_TYPE)
    def dummy(prev, action):
        next = prev
        # Do something
        return next


Combine reducers
================

You can naively combine several ``reducers`` in this way:

.. code:: python

    def dummy(prev, action):
        next = prev
        if action.type == ActionType.DUMMY_ACTION_TYPE1:
            # Do something
            return next
        elif action.type == ActionType.DUMMY_ACTION_TYPE2:
            # Do something different
            return next
        else:
            return next

but this is going to make your ``reducer`` function huge and barely readable.
:any:`revived.reducer` contains utility functions that allows you to create much
more readable ``reducers``.

Reducers can (*and should*) be combined. You can easily do this combination
using :any:`revived.reducer.combine_reducers`.

The following example will produce a ``combined reducer`` where both the
``reducers`` will handle the whole subtree passed to it: exactly the same result of
the previous snippet of code!

.. code:: python

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

    combined_reducer = combine_reducers(dummy1, dummy2)

**Note**: a ``combined reducer`` is a ``reducer`` and can be combined again with
other reducers allowing you to creare every structure you will ever need in your
app.

Pass a subtree of the state
---------------------------

If you want it is possible to pass to a reducer only a subtree of the state
passed to the ``combined reducer``. To do this you should use keyword arguments
in this way:

.. code:: python

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

    combined_reducer = combine_reducers(dummy1, dummy_subtree=dummy2)

In this example ``dummy1`` will receive the whole subtree passed to the
``combined_reducer`` while ``dummy2`` will only receive the ``dummy_subtree``
subtree.

Create a reducer module
=======================

A ``reducer module`` is an utility object that behave exactly like a single
``reducer``, but permits to register more ``reducers`` into it. You will use it
to define a bunch of ``reducers`` that are all handling the same subtree of the
``state``.

Note that this is *only a helper construct*, because the following snippet of
code:

.. code:: python

    mod = Module()

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

.. code:: python

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

And of course **you can combine** a ``reducer module`` with other ``reducers``
and ``reducer modules``.
"""
from .action import Action
from .action import ActionType
from functools import wraps
from typing import Any
from typing import Callable
from typing import List
from typing import Union

Reducer = Callable[[Any, Action], Any]
ReducerList = List[Reducer]


class Module:
    """Helper class for module creations.

    This is just an helper class: you can obtain the same result using the
    reducer decorator and then combining all the defined reducers as top-level
    reducers. The module instance will work exactly as a reducer function, but
    will call all the registered reducers. The call order is not guaranteed.
    """

    def __init__(self) -> None:
        self._reducers = []  # type: ReducerList

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


def combine_reducers(*top_reducers: Union[Reducer, Module], **reducers: Union[Reducer, Module]) -> Reducer:
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
