"""Store tests.
"""

from revived.store import DispatchInReducerError
from revived.store import Store
import pytest


@pytest.fixture
def dummy_reducer():
    return lambda state, action: action


def test_store__creation(dummy_reducer):
    store = Store(dummy_reducer)
    assert store.get_state() is None


def test_store__dispatch(dummy_reducer):
    store = Store(dummy_reducer)
    store.dispatch('test')
    assert store.get_state() ==  'test'


def tets_store__dispatch__dispatch_in_reducer(dummy_reducer):
    store = Store(dummy_reducer)

    def wrong_reducer(state, action):
        store.dispatch('should fail')

    store.replace_reducer(wrong_reducer)
    with pytest.raises(DispatchInReducerError):
        store.dispatch('test')


def test_store__dispatch__dispatch_in_subscriber(dummy_reducer):
    store = Store(dummy_reducer)

    def callback():
        if store.get_state() == 'test1':
            store.dispatch('test2')

    store.subscribe(callback)

    store.dispatch('test1')
    assert store.get_state() == 'test2'


def test_store__dispatch__subscriber(dummy_reducer):
    called = False

    def callback():
        nonlocal called
        called = True

    store = Store(dummy_reducer)
    store.subscribe(callback)
    store.dispatch('test')

    assert called


def test_store__unsubscribe(dummy_reducer):
    called = 0

    def callback():
        nonlocal called
        called += 1

    store = Store(dummy_reducer)
    unsubscribe = store.subscribe(callback)

    store.dispatch('test1')
    assert called == 1

    unsubscribe()
    store.dispatch('test2')
    assert called == 1
