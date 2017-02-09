"""Integration tests module.
"""
from revived.action import action
from revived.action import ActionType
from revived.reducer import combine_reducers
from revived.reducer import Module
# from revived.reducer import reducer
from revived.store import ActionType as StoreAT
from revived.store import Store

#
# Building revived module
#
# The building revival module will look like:
#
# {
#     'building': '<building_name>',
#     'target': '<target>',
#     'is_building': True,  # or False
# }
#


class BuildingAT(ActionType):
    BUILDING_CHANGE = 'building_change'
    BUILDING_TARGET_CHANGE = 'building_target_change'
    BUILDING_STARTED = 'building_started'
    BUILDING_FINISHED = 'building_finished'


@action(BuildingAT.BUILDING_CHANGE)
def building_change(building):
    return {'building': building}


@action(BuildingAT.BUILDING_TARGET_CHANGE)
def building_target_change(target):
    return {'target': target}


@action(BuildingAT.BUILDING_STARTED)
def building_started():
    pass


@action(BuildingAT.BUILDING_FINISHED)
def building_finished():
    pass


building_module = Module()


@building_module.reducer(BuildingAT.BUILDING_CHANGE)
def building_change_reducer(prev, action):
    building = action['building']
    return dict(prev, building=building)


@building_module.reducer(BuildingAT.BUILDING_TARGET_CHANGE)
def building_target_change_reducer(prev, action):
    target = action['target']
    return dict(prev, target=target)


@building_module.reducer(BuildingAT.BUILDING_STARTED)
def building_started_reducer(prev, action):
    return dict(prev, is_building=True)


@building_module.reducer(BuildingAT.BUILDING_FINISHED)
def building_finished_reducer(prev, action):
    return dict(prev, is_building=False)


#
# Attack revived module
#
# The attack revived module will look like:
#
# {
#     'target': '<target>',
#     'is_attacking': True,  # or False
# }
#


class AttackAT(ActionType):
    ATTACK_TARGET_CHANGE = 'attack_target_change'
    ATTACK_STARTED = 'attack_started'
    ATTACK_FINISHED = 'attack_finished'


@action(AttackAT.ATTACK_TARGET_CHANGE)
def attack_target_change(target):
    return {'target': target}


@action(AttackAT.ATTACK_STARTED)
def attack_started():
    pass


@action(AttackAT.ATTACK_FINISHED)
def attack_finished():
    pass


attack_module = Module()


@attack_module.reducer(AttackAT.ATTACK_TARGET_CHANGE)
def attack_target_change_reducer(prev, action):
    target = action['target']
    return dict(prev, target=target)


@attack_module.reducer(AttackAT.ATTACK_STARTED)
def attack_started_reducer(prev, action):
    return dict(prev, is_attacking=True)


@attack_module.reducer(AttackAT.ATTACK_FINISHED)
def attack_finished_reducer(prev, action):
    return dict(prev, is_attacking=False)


#
# Game revived module
#
# The game revived module will contain both the building and the attack one and
# will look like:
#
# {
#     'building_mode': {
#         'building': '<building_name>',
#         'target': '<target>',
#         'is_building': True,  # or False
#     },
#     'attack_mode': {
#         'target': '<target>',
#         'is_attacking': True,  # or False
#     },
#     'current_mode': 'building'
# }
#


class GameAT(ActionType):
    GAME_MODE_CHANGE = 'mode_change'


@action(GameAT.GAME_MODE_CHANGE)
def game_mode_change(mode):
    return {'mode': mode}


game_module = Module()


@game_module.reducer(GameAT.GAME_MODE_CHANGE)
def game_mode_change_reducer(prev, action):
    return {
        'current_mode': action['mode'],
        'building_mode': {},
        'attack_mode': {},
    }


@game_module.reducer(StoreAT.INIT)
def game_init(prev, action):
    return {
        'current_mode': 'attack',
        'building_mode': {},
        'attack_mode': {},
    }


store = Store(combine_reducers(game_module, building_mode=building_module, attack_mode=attack_module))


def test_revived__integration():
    assert store.get_state() == {
        'current_mode': 'attack',
        'building_mode': {},
        'attack_mode': {},
    }

    store.dispatch(game_mode_change('building'))
    assert store.get_state() == {
        'current_mode': 'building',
        'building_mode': {},
        'attack_mode': {},
    }

    store.dispatch(building_change('turret'))
    assert store.get_state() == {
        'current_mode': 'building',
        'building_mode': {
            'building': 'turret',
        },
        'attack_mode': {},
    }

    store.dispatch(building_target_change('turret1'))
    assert store.get_state() == {
        'current_mode': 'building',
        'building_mode': {
            'building': 'turret',
            'target': 'turret1',
        },
        'attack_mode': {},
    }

    store.dispatch(building_started())
    assert store.get_state() == {
        'current_mode': 'building',
        'building_mode': {
            'building': 'turret',
            'target': 'turret1',
            'is_building': True,
        },
        'attack_mode': {},
    }

    store.dispatch(building_finished())
    assert store.get_state() == {
        'current_mode': 'building',
        'building_mode': {
            'building': 'turret',
            'target': 'turret1',
            'is_building': False,
        },
        'attack_mode': {},
    }

    store.dispatch(game_mode_change('attack'))
    assert store.get_state() == {
        'current_mode': 'attack',
        'building_mode': {},
        'attack_mode': {},
    }

    store.dispatch(attack_target_change('zombie1'))
    assert store.get_state() == {
        'current_mode': 'attack',
        'building_mode': {},
        'attack_mode': {
            'target': 'zombie1'
        },
    }

    store.dispatch(attack_started())
    assert store.get_state() == {
        'current_mode': 'attack',
        'building_mode': {},
        'attack_mode': {
            'target': 'zombie1',
            'is_attacking': True
        },
    }

    store.dispatch(attack_finished())
    assert store.get_state() == {
        'current_mode': 'attack',
        'building_mode': {},
        'attack_mode': {
            'target': 'zombie1',
            'is_attacking': False
        },
    }
