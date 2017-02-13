"""Store tests.
"""
from revived.action import Action
from revived.store import ActionType as AT
from revived.store import DispatchInReducerError
from revived.store import Store
import pytest


@pytest.fixture
def dummy_reducer():
    return lambda state, action: action.type if action.type != AT.INIT else None


def test_store__creation(dummy_reducer):
    store = Store(dummy_reducer)
    assert store.get_state() is None


def test_store__dispatch(dummy_reducer):
    store = Store(dummy_reducer)
    store.dispatch(Action('test'))
    assert store.get_state() == 'test'


def tets_store__dispatch__dispatch_in_reducer(dummy_reducer):
    store = Store(dummy_reducer)

    def wrong_reducer(state, action):
        store.dispatch(Action('should fail'))

    store.replace_reducer(wrong_reducer)
    with pytest.raises(DispatchInReducerError):
        store.dispatch(Action('test'))


def test_store__dispatch__dispatch_in_subscriber(dummy_reducer):
    store = Store(dummy_reducer)

    def callback():
        if store.get_state() == 'test1':
            store.dispatch(Action('test2'))

    store.subscribe(callback)

    store.dispatch(Action('test1'))
    assert store.get_state() == 'test2'


def test_store__dispatch__subscriber(dummy_reducer):
    called = False

    def callback():
        nonlocal called
        called = True

    store = Store(dummy_reducer)
    store.subscribe(callback)
    store.dispatch(Action('test'))

    assert called


def test_store__dispatch__subscriber_decorator(dummy_reducer):
    store = Store(dummy_reducer)

    called = False

    @store.subscriber
    def callback():
        nonlocal called
        called = True

    store.dispatch(Action('test'))

    assert called


def test_store__unsubscribe(dummy_reducer):
    called = 0

    def callback():
        nonlocal called
        called += 1

    store = Store(dummy_reducer)
    unsubscribe = store.subscribe(callback)

    store.dispatch(Action('test'))
    assert called == 1

    unsubscribe()
    store.dispatch(Action('test'))
    assert called == 1


def test_store__unsubscribe_decorator(dummy_reducer):
    store = Store(dummy_reducer)

    called = 0

    @store.subscriber
    def callback():
        nonlocal called
        called += 1

    store.dispatch(Action('test'))
    assert called == 1

    callback.unsubscribe()
    store.dispatch(Action('test'))
    assert called == 1
