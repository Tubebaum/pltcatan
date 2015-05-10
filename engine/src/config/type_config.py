from engine.src.resource_type import ResourceType
from engine.src.position_type import PositionType
from types import *

type_config = {
    'game': {
        'points_to_win': IntType,
        'player_count': IntType,

        'board' : {
            'tile_count': IntType,
            'radius': IntType,
        },
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
                    'draw_card': FunctionType,
                    'play_card': FunctionType
                }
            }
        }
    }
}
