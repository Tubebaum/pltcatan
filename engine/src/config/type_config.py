from engine.src.resource_type import ResourceType
from types import *

type_config = {
    'structure': {
        'player_built': {
            'default': {
                'cost': {ResourceType: IntType}
            }
        }
    },
    'card': {
        'development': {
            'default': {
                'cost': {ResourceType: IntType}
            }
        }
    }
}
