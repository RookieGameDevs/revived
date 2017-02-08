"""Reducer tests.
"""

from revived.reducer import combine_reducers
from revived.reducer import create_reducer
from revived.reducer import reducer


def test_reducer__create():
    def red(prev, action):
        return not prev

    r = create_reducer('action1', red)

    result = r(False, {'type': 'action1'})
    assert result is True

    result = r(False, {'type': 'action2'})
    assert result is False


def test_reducer__create_decorator():
    @reducer('action1')
    def red(prev, action):
        return not prev

    result = red(False, {'type': 'action1'})
    assert result is True

    result = red(False, {'type': 'action2'})
    assert result is False


def test_reducer__combine():
    def red1(prev, action):
        next = prev
        if action == 'action1':
            next = not prev
        return next

    def red2(prev, action):
        next = prev
        if action == 'action2':
            next = False
        return next

    combined = combine_reducers(
        part1=red1,
        part2=red2)

    result = combined({'part1': False, 'part2': True}, 'action1')
    assert result == {'part1': True, 'part2': True}
    result = combined({'part1': False, 'part2': True}, 'action2')
    assert result == {'part1': False, 'part2': False}


def test_reducer__integration():
    @reducer('action1')
    def red1(prev, action):
        next = action['data']
        return next

    @reducer('action2')
    def red2(prev, action):
        next = action['data']
        return next

    combined = combine_reducers(
        part1=red1,
        part2=red2)

    result = combined({'part1': None, 'part2': None}, {'type': 'action1', 'data': True})
    assert result == {'part1': True, 'part2': None}
    result = combined({'part1': None, 'part2': None}, {'type': 'action2', 'data': True})
    assert result == {'part1': None, 'part2': True}
