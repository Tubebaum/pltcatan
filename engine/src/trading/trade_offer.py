# -*- coding: utf-8 -*-
from enum import Enum
from engine.src.resource_type import ResourceType


class TradeOffer(object):
    # TODO: Convert resources to collections.Counter

    def __init__(self, offered_resources, requested_resources):

        self.requested_resources = TradeOffer._get_empty_resources()
        self.requested_resources.update(requested_resources)

        self.offered_resources = TradeOffer._get_empty_resources()
        self.offered_resources.update(offered_resources)

    @staticmethod
    def _get_empty_resources():

        resources = {}

        for arable_type in ResourceType.get_arable_types():
            resources[arable_type] = 0

        return resources

    def validate(self, proposing_entity, receiving_entity):
        """See if this trade can be carried out between the given entities.

        Args:
            proposing_entity (TradingEntity): The entity that proposed the
              trade, i.e. that wants to give the offered_resources and receive
              the requested_resources of this trade.

            receiving_entity (TradingEntity): The other entity to whom this
              trade was proposed and who will receive the offered_resources and
              give the requested_resources.

        Returns:
            TradingEntity, ResourceType. If the trade cannot be completed, this
              method returns the entity that is blocking it and the resource
              they lack. If the trade can be completed, it will return None.
        """

        # Check that the proposing_entity has all the resources listed in this
        # trade's offered_resources dict.
        for resource_type, count in self.offered_resources.iteritems():
            if proposing_entity.resources[resource_type] < count:
                return proposing_entity, resource_type

        # Check that the receiving entity has all the resources listed in this
        # trade's requested_resources dict.
        for resource_type, count in self.requested_resources.iteritems():
            if receiving_entity.resources[resource_type] < count:
                return receiving_entity, resource_type

        return None, None

    def execute(self, proposing_entity, receiving_entity):
        """Execute this trade based on the given trade entities.

        This call should always be preceded by a call to self.validate().

        Args:
            See self.validate()

        Returns:
            None.
        """

        # Take the offered resources from the entity that proposed the deal
        # and give them to the entity that accepted the deal.
        for resource_type, count in self.offered_resources.iteritems():
            proposing_entity.withdraw_resources(resource_type, count)
            receiving_entity.deposit_resources(resource_type, count)

        # Take the resources requested by the proposing entity from the
        # entity that accepted the deal and give them to the proposing entity.
        for resource_type, count in self.requested_resources.iteritems():
            proposing_entity.deposit_resources(resource_type, count)
            receiving_entity.withdraw_resources(resource_type, count)


class TradeMetaCriteria(Enum):
    ANY = 1
    SAME = 2


class TradeCriteria(TradeOffer):
    """Defines different trade criteria."""

    def __init__(self, offered_resources=None, requested_resources=None,
                 offered_meta=None, requested_meta=None):

        super(TradeCriteria, self).__init__(offered_resources,
                                            requested_resources)

        self.offered_meta = TradeCriteria._get_empty_meta()
        self.requested_meta = TradeCriteria._get_empty_meta()

        self.offered_meta.update(offered_meta)
        self.requested_meta.update(requested_meta)

    @staticmethod
    def _get_empty_meta():

        meta = {}

        for criteria in TradeMetaCriteria:
            meta[criteria] = 0

        return meta

    def permits(self, trade_offer):

        valid_offer = self.valid(self.offered_resources, self.offered_meta,
                                 trade_offer.offered_resource)

        valid_req = self.valid(self.requested_resources, self.requested_meta,
                               trade_offer.requested_resources)

        return valid_offer and valid_req

    @staticmethod
    def valid(crit_resources, crit_meta, offered_resources):

        offered_resources = offered_resources.copy()

        valid = True

        # First handle meta
        if valid and TradeMetaCriteria.SAME in crit_meta:

            valid = False

            req_same_resource_count = crit_meta[TradeMetaCriteria.SAME]

            for resource_type, count in offered_resources.iteritems():
                if count >= req_same_resource_count:
                    offered_resources[resource_type] -= req_same_resource_count
                    valid = True
                    break

        if valid and TradeMetaCriteria.ANY in crit_meta:

            req_any_resource_count = crit_meta[TradeMetaCriteria.ANY]

            for resource_type, count in offered_resources.iteritems():
                if count > 0:
                    deduct = min(count, req_any_resource_count)

                    req_any_resource_count -= deduct
                    offered_resources[resource_type] -= deduct

            if req_any_resource_count > 0:
                valid = False

        if valid:
            # Now handle normal resources
            for resource_type, count in crit_resources.iteritems():
                if count != offered_resources[resource_type]:
                    valid = False

        return valid
