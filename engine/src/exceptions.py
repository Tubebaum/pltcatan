class NotEnoughResourcesException(Exception):
    """Raise when a trader lacks enough resources cards for a transaction.

    E.g. when a player doesn't have enough resource cards to buy a structure,
    or when a bank runs out of resources.
    """
    pass