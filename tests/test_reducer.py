"""Reducer tests.
"""
from revived.action import Action
from revived.reducer import combine_reducers
from revived.reducer import Module
from revived.reducer import reducer


def test_reducer__create():
    @reducer('action1')
    def red(prev, action):
        return not prev

    result = red(False, Action('action1'))
    assert result is True

    result = red(False, Action('action2'))
    assert result is False


def test_reducer__combine():
    @reducer('action1')
    def red1(prev, action):
        return not prev

    @reducer('action2')
    def red2(prev, action):
        return False

    combined = combine_reducers(
        part1=red1,
        part2=red2)

    result = combined({'part1': False, 'part2': True}, Action('action1'))
    assert result == {'part1': True, 'part2': True}
    result = combined({'part1': False, 'part2': True}, Action('action2'))
    assert result == {'part1': False, 'part2': False}


def test_reducer__module_reducer():
    module = Module()

    @module.reducer('action1')
    def red1(prev, action):
        return False

    @module.reducer('action2')
    def red2(prev, action):
        return True

    result = module(None, Action('action1'))
    assert result is False
    result = module(None, Action('action2'))
    assert result is True
