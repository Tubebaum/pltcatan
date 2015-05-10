from itertools import imap, chain
from collections import Sequence

def listlike(obj):
    """Checks if the object is like a sequential container

    Args:
        obj (Object): The object to check

    Returns:
        Bool. True if the object is listlike, False if it's a string

    """
    return isinstance(obj, Sequence) and not isinstance(obj, basestring)


def one_or_many(value):
    """Ensures the value can be used like a list

    Args:
        value (Any): The value to check

    Returns:
        Any. The value if it's listlike, or the value wrapped in a tuple if it isn't

    """
    return value if listlike(value) else (value,)


def flatten(values):
    """Iterate over objects like a flat list

    Args:
        values (List): A list of objects to flatten

    Returns:
        List. A list containing the nested objects in values
    """
    return chain.from_iterable(imap(one_or_many, values))

def find_column(input, token=None, lexpos=None):
    """Finds the column of a token given the input it's in

    Args:
        input (String) - The input being parsed
        token (Token) - The token being located

    Returns:
        The column the token being located is in
    """
    lexpos = lexpos or token.lexpos
    last_cr = input.rfind('\n',0,lexpos)
    if last_cr < 0:
        last_cr = 0
    column = (lexpos - last_cr) + 1
    return column