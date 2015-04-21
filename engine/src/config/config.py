from types import MethodType
import engine.src.config as config
from engine.src.exceptions import *

from engine.src.lib.utils import Utils
from engine.src.trading.trade_offer import *
from engine.src.resource_type import ResourceType


def get_import_value(dot_notation_str, var_name, prefix='engine.src.config.'):
    mod = __import__(prefix + dot_notation_str, globals(), locals(), [var_name], -1)
    value = getattr(mod, var_name)
    return value

config = {
    # Game
    'game' : {
        'points_to_win': 10,
        'default_player_count': 3
    },
    'board' : {
        'default_tile_count': 19,
        'default_radius': 3,
    },
    # Cards
    'card' : {
        # Development Cards
        'development': {
            'default': {
                'count': 0,
                'name': 'Development Card',
                'description': 'Development card default description.',
                'draw_card': Utils.noop,
                'play_card': Utils.noop,
                'cost': {ResourceType.GRAIN: 1, ResourceType.ORE: 1,
                         ResourceType.WOOL: 1},
            },
            # Non-Progress Cards
            'knight': {
                'count': 14,
                'name': 'Knight Card',
                'description': ('Move the robber to a new tile. Steal 1 '
                                'resource from the owner of a structure '
                                'adjacent to the new tile.'),
                'draw_card': get_import_value('card.development.knight', 'draw_card'),
                'play_card': get_import_value('card.development.knight', 'play_card'),
            },
            'victory_point': {
                'count': 5,
                'name': 'Victory Point Card',
                'description': ('Gives you one victory point. Must remain '
                                'hidden until used to win the game.'),
                'draw_card':
                    get_import_value('card.development.victory_point', 'draw_card'),
                'play_card':
                    get_import_value('card.development.victory_point', 'play_card'),
            },
            # Progress Cards
            'monopoly': {
                'count': 2,
                'name': 'Monopoly Card',
                'description': ('If you play this card, you must name 1 type '
                                'of resource. All the other players must give '
                                'you all of the Resource Cards of this type '
                                'that they have in their hands. If an opponent '
                                'does not have a Resource Card of the '
                                'specified type, he does not have to give you '
                                'anything.'),
                'draw_card': get_import_value('card.development.monopoly', 'draw_card'),
                'play_card': get_import_value('card.development.monopoly', 'play_card'),
            },
            'road_building': {
                'count': 2,
                'name': 'Road Building Card',
                'description': ('If you play this card, you may immediately '
                                'place 2 free roads on the board (according to '
                                'normal building rules)'),
                'draw_card':
                    get_import_value('card.development.road_building', 'draw_card'),
                'play_card':
                    get_import_value('card.development.road_building', 'play_card'),
            },
            'year_of_plenty': {
                'count': 2,
                'name': 'Year of Plenty Card',
                'description': ('If you play this card you may immediately '
                                'take any 2 Resource Cards from the supply '
                                'stacks. You may use these cards to build in '
                                'the same turn.'),
                'draw_card':
                    get_import_value('card.development.year_of_plenty', 'draw_card'),
                'play_card':
                    get_import_value('card.development.year_of_plenty', 'play_card'),
            }
        }
    }
}


class Config(object):

    @classmethod
    def init_from_config(cls, obj, config_path):
        property_dict = Config.get(config_path)

        for key, val in property_dict.iteritems():

            if Utils.is_function(val):
                setattr(obj, key, MethodType(val, obj, obj.__class__))
            else:
                setattr(obj, key, val)

    @classmethod
    def get(cls, dot_notation_str):

        keys = dot_notation_str.split('.')

        def get_recursive(dct, keys):
            key = keys.pop(0)
            val = None

            if key in dct:
                val = dct.get(key)
            else:
                raise NoConfigValueDefinedException(dot_notation_str)

            if keys:
                if val:
                    return get_recursive(val, keys)
                else:
                    raise NoConfigValueDefinedException(dot_notation_str)
            else:
                return val

        value = get_recursive(Config.config, keys)

        # Remove default value from dictionary type return value.
        # if isinstance(value, dict):
        #     value.pop('default')

        return value

    #### New config format
    config = config

    #### Old config format for compatibility

    # TradeCriteria
    TWO_FOR_ONE = TradeCriteria({}, {}, {TradeMetaCriteria.SAME: 2},
                                  {TradeMetaCriteria.ANY: 1})

    THREE_FOR_ONE = TradeCriteria({}, {}, {TradeMetaCriteria.SAME: 3},
                                    {TradeMetaCriteria.ANY: 1})


