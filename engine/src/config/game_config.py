from engine.src.resource_type import ResourceType
from engine.src.lib.utils import Utils

def get_import_value(dot_notation_str, var_name, prefix='engine.src.config.'):
    mod = __import__(prefix + dot_notation_str, globals(), locals(), [var_name], -1)
    value = getattr(mod, var_name)
    return value

game_config = {
    # Game
    'game' : {
        'points_to_win': 10,
        'player_count': 3
    },
    'board' : {
        'tile_count': 19,
        'radius': 3,
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
                'cost': {
                    'wool': 1,
                    'grain': 1,
                    'ore': 1
                },
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
    },
    # Structures
    'structure': {
        'player_built': {
            'default': {
                'name': None,
                'cost': {
                    'lumber': 0,
                    'brick': 0,
                    'wool': 0,
                    'grain': 0,
                    'ore': 0
                },
                'count': 0,
                'point_value': 0,
                'base_yield': 1,
                # TODO: Rename vars to reflect that they should be structure names?
                'extends': None,
                'upgrades': None,
                'position_type': 'vertex'
            },
            # Edge Structures
            'road': {
                'name': 'Road',
                'cost': {
                    'lumber': 1,
                    'brick': 1,
                },
                'count': 15,
                'point_value': 0,
                'base_yield': 0,
                'extends': None,
                'upgrades': None,
                'position_type': 'edge'
            },
            # Vertex Structures
            'settlement': {
                'name': 'Settlement',
                'cost': {
                    'lumber': 1,
                    'brick': 1,
                    'wool': 1,
                    'grain': 1
                },
                'count': 5,
                'point_value': 1,
                'base_yield': 1,
                'extends': None,
                'upgrades': None,
                'position_type': 'vertex'
            },
            'city': {
                'name': 'City',
                'cost': {
                    'grain': 2,
                    'ore': 3,
                },
                'count': 5,
                'point_value': 2,
                'base_yield': 2,
                'extends': None,
                'upgrades': 'Settlement',
                'position_type': 'vertex'
            },
            # For Demo
            'castle': {
                'name': 'Castle',
                'cost': {
                    'ore': 5
                },
                'count': 2,
                'point_value': 3,
                'base_yield': 3,
                'extends': None,
                'upgrades': 'City',
                'position_type': 'vertex'
            }
        }
    }
}
