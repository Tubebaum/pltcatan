from engine.src.lib.utils import Utils


class UserMessageException(Exception):
    """
    A custom exception class that prints self.msg when cast to a string.
    """
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class NotEnoughResourcesException(UserMessageException):
    """Raise when a trader lacks enough resources cards for a transaction.

    E.g. when a player doesn't have enough resource cards to buy a structure,
    or when a bank runs out of resources.

    Attributes:
        See Exception.

    Args:
        trading_entity (TradingEntity): The entity that lacked resources.

        resource_type (ResourceType or list of ResourceType): The type(s) of
          resource(s) the entity lacked.
    """

    def __init__(self, trading_entity, resource_types):

        resource_type_strs = map(
            lambda resource_type: str(resource_type),
            Utils.convert_to_list(resource_types)
        )

        resource_type_str = ''

        if len(resource_type_strs) == 1:
            resource_type_str = resource_type_strs[0]
        else:
            resource_type_str = ', '.join(resource_type_strs[:-1]) +\
                ', or ' + resource_type_strs[-1]

        self.msg = '{0} does not have enough {1} cards!'.format(
            trading_entity.__class__.__name__, resource_type_str)


class NotEnoughStructuresException(UserMessageException):
    """Raise when a player tries to build a structure despite having none left.

    Args:
        player (Player): The player that tried to build a structure.

        structure_name (str): The string name of structure the player attempted
          to build despite having run out.
    """

    def __init__(self, player, structure_name):
        self.msg = '{0} does not have a {1} in stock.'.format(
            player.name, structure_name)


class NotEnoughDevelopmentCardsException(UserMessageException):
    """Raise when a player tries to buy a development card when none left."""

    def __init__(self):
        self.msg = 'No development cards remaining.'


class InvalidBaseStructureException(UserMessageException):
    """Raise when one tries to build an invalid upgrade or extension structure.

    Upgrade and extension structures need to be built off an appropriate base
    structure of a predetermined class. If the wrong class base structure is
    attempted, we should raise this error.
    """

    def __init__(self, base_structure, augmenting_structure):
        augments = augmenting_structure.augments()

        if augments is None:
            augments = 'an empty position'

        self.msg = '{} must replace {}, but tried to replace a {}!'.format(
            augmenting_structure.name, augments, base_structure.name)


class BoardPositionOccupiedException(UserMessageException):
    """Raise when a player tries to build on a taken board position.

    Players can not place structures on positions taken by other players.
    Players can not replace existing structures with non-augmenting structures.
    """

    def __init__(self, position, structure, owning_player):

        self.msg = 'Position {} already has a {} belonging to {}.'.format(
            position, structure.name, owning_player.name)


class NoConfigValueDefinedException(UserMessageException):

    def __init__(self, dot_notation_str):

        self.msg = 'No config value defined for {}.'.format(dot_notation_str)


class NoSuchVertexException(UserMessageException):

    def __init__(self, tile, vertex_dir):

        self.msg = 'Tile has no vertex: {}'.format(vertex_dir)

class NoSuchEdgeException(UserMessageException):

    def __init__(self, tile, edge_dir):

        self.msg = 'Tile has no edge: {}'.format(edge_dir)


class InvalidStructurePlacementException(UserMessageException):
    """Raise when a player tries to place a structure somewhere they shouldn't.

    E.g. no neighboring claimed roads, too close to another structure, etc.
    """

    def __init__(self):
        self.msg = 'Not a valid position to place the structure.'
