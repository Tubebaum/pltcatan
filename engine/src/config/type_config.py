from engine.src.resource_type import ResourceType
from engine.src.position_type import PositionType
from types import *

type_config = {
    'structure': {
        'player_built': {
            'default': {
                'cost': {ResourceType: IntType},
                'position_type': PositionType
            }
        }
    },
    'card': {
        'development': {
            'default': {
                'cost': {ResourceType: IntType},
                'draw_card': MethodType,
                'play_card': MethodType
            }
        }
    }
}
