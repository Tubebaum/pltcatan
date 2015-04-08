# -*- coding: utf-8 -*-
from engine.src.exceptions import NotEnoughResourcesException
from engine.src.resource_type import ResourceType


class TradingEntity(object):
    """Represents an entity capable of storing and trading resources.

    Attributes:
        resources (dict): Represents all resources currently owned by this
          entity. Keys are arable ResourceTypes and values are integers
          representing the amount of a particular resource type the entity has.

    TODO: This should be an abstract class.
    """

    def __init__(self):
        self.resources = {}
        # TODO: Freak error where Python isn't recognizing default arg.
        self._default_init_resources(0)

    def _default_init_resources(self, count=0):
        """Initialize this entity to have count resources per resource type.

        Args:
            count (int): Number of each arable resource this entity will have.

        Returns:
            None. Modifies self.resources.
        """

        self.resources = {}
        for arable_type in ResourceType.get_arable_types():
            self.resources[arable_type] = count

    def withdraw_resources(self, resource_type, resource_count):
        """Withdraw the specified number of resources from the entity.

        Args:
            resource_type (ResourceType): Type of resource to withdraw.

            resource_count (int): Number of resources of the given type to
              withdraw.

        Raises:
            NotEnoughResourcesException. When the withdrawal is for more
              resources than the entity currently has.
        """

        if self.resources[resource_type] >= resource_count:
            self.resources[resource_type] -= resource_count
        else:
            message = '{0} does not have enough {1} cards!'.format(
                self.__class__.__name__, resource_type)
            raise NotEnoughResourcesException(message)

    def deposit_resources(self, resource_type, resource_count):
        """Deposit the specified number of resources from the entity.

        Args:
            resource_type (ResourceType): Type of resource to deposit.

            resource_count (int): Number of resources of the given type to
              deposit.
        """

        self.resources[resource_type] += resource_count

    def trade(self, requesting_entity, trade_offer):
        """Trade one resource for another at a given ratio.

        Args:
            requesting_entity (TradingEntity): Entity who has proposed a trade
              wherein they offer the trade's offered_resources and request the
              trade's requested_resources from this entity.

            trade (Trade): Keeps track of how many of which resource are being
              offered and requested.

        Raises:
            NotEnoughResourcesException. When this or the other entity lacks
              the resources to complete the trade.
        """

        obstructing_entity, obstructing_resource_type = \
            trade_offer.validate(requesting_entity, self)

        if obstructing_entity is not None:

            message = '{0} does not have enough {1} cards!'.format(
                obstructing_entity.__class__.__name__,
                obstructing_resource_type)

            raise NotEnoughResourcesException(message)

        else:
            trade_offer.execute(requesting_entity, self)
