# -*- coding: utf-8 -*-
import random
from collections import Counter
from engine.src.lib.utils import Utils
from engine.src.exceptions import NotEnoughResourcesException
from engine.src.resource_type import ResourceType
from engine.src.trading.trade_offer import TradeOffer


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

    def _default_init_resources(self, count):
        """Initialize this entity to have count resources per resource type.

        Args:
            count (int): Number of each arable resource this entity will have.

        Returns:
            None. Modifies self.resources.
        """

        self.resources = {}
        for arable_type in ResourceType.get_arable_types():
            self.resources[arable_type] = count

    def count_resources(self):
        return sum(self.resources.values())

    def validate_resources(self, resources):
        """Check that this player has at least as many resources as given."""

        default_resources = TradeOffer._get_empty_resources()
        default_resources.update(resources)

        resources = default_resources

        # This entity does not have the given resources if the difference
        # between its count and the given resources dict count for any given
        # resource type is negative.
        resource_debt = {resource_type: count - resources[resource_type]
                         for resource_type, count in self.resources.items()
                         if count - resources[resource_type] < 0}

        valid = len(resource_debt.keys()) == 0

        if valid:
            return True
        else:
            raise NotEnoughResourcesException(self, resource_debt.keys())

    def get_resource_list(self):
        """Get a list of resource types, one for each "card" this player has."""

        return Utils.flatten(map(
            lambda resource_type:
                [resource_type] * self.resources[resource_type],
            self.resources
        ))

    def transfer_resources(self, to_entity, resource_type, resource_count):
        """Transfer specified resources from this entity to the given entity."""

        self.withdraw_resources(resource_type, resource_count)
        to_entity.deposit_resources(resource_type, resource_count)

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

        if resource_type == ResourceType.FALLOW:
            # TODO: raise exception.
            return

        if self.resources[resource_type] >= resource_count:
            self.resources[resource_type] -= resource_count
        else:
            raise NotEnoughResourcesException(self, resource_type)

    def withdraw_random_resource(self):
        """Remove a random resource from this trading entity.

        Note that this method only withdraws a single random resource.
        Callers of this method should check to make sure that this entity
        still has resources using self.count_resources().
        """

        resources = self.get_resource_list()

        resource_type = random.choice(resources)

        self.resources[resource_type] -= 1

        return resource_type

    def deposit_multiple_resources(self, resource_type_count_dict):

        for resource_type, count in resource_type_count_dict.iteritems():
            self.deposit_resources(resource_type, count)

    def deposit_resources(self, resource_type, resource_count):
        """Deposit the specified number of resources from the entity.

        Args:
            resource_type (ResourceType): Type of resource to deposit.

            resource_count (int): Number of resources of the given type to
              deposit.
        """

        if resource_type != ResourceType.FALLOW:
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
            raise NotEnoughResourcesException(obstructing_entity,
                                              obstructing_resource_type)

        else:
            trade_offer.execute(requesting_entity, self)
