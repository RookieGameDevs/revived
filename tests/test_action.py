"""Action tests.
"""
from revived.action import action


def test_action__action_creator_without_arguments():
    @action('action1')
    def action1():
        return {'test': 'value'}

    a = action1()
    assert a.type == 'action1'
    assert dict(a) == {'test': 'value'}


def test_action__action_creator_with_arguments():
    @action('action2')
    def action2(value):
        return {'test': value}

    a = action2('first')
    assert a.type == 'action2'
    assert dict(a) == {'test': 'first'}

    a = action2('second')
    assert a.type == 'action2'
    assert dict(a) == {'test': 'second'}
