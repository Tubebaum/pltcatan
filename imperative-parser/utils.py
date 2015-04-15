from itertools import imap, chain
from collections import Sequence

def listlike(obj):
    """Checks if the object is like a sequential container

    Arguments:
        obj -- the object to check

    Return:
        True if the object is listlike, False if it's a string

    """
    return isinstance(obj, Sequence) and not isinstance(obj, basestring)


def one_or_many(value):
    """Ensures the value can be used like a list

    Arguments:
        value -- the value to check

    Return:
        The value if it's listlike, or the value wrapped in a tuple if it isn't

    """
    return value if listlike(value) else (value,)


def flatten(values):
    """Iterate over objects like a flat list

    Arguments:
        values -- a list of objects to flatten

    Return:
        A list containing the nested objects in values
    """
    return chain.from_iterable(imap(one_or_many, values))