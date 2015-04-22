# -*- coding: utf-8 -*-
import collections
from types import MethodType


class Utils(object):
    """A general utility class."""

    @classmethod
    def init_from_dict(cls, obj, dct):

        for key, val in dct.iteritems():
            if Utils.is_function(val):
                setattr(obj, key, MethodType(val, obj, obj.__class__))
            else:
                setattr(obj, key, val)

    @classmethod
    def pluck(cls, dct, prop, do_filter=False):
        """Gets a list of values for the given property.

        Assumes the dct has key-value pairs where values are also dcts. Gets
        a list of values for the given property by taking them off each such
        value dct.
        """

        lst = []

        try:
            lst = map(lambda key: dct[key][prop], dct)

            if do_filter:
                lst = filter(lambda value: value is not None, lst)

        except KeyError:
            lst = []

        return lst

    @classmethod
    def is_function(cls, func):
        return hasattr(func, '__call__')

    @classmethod
    def is_list(cls, lst):
        return hasattr(lst,"__iter__")

    @classmethod
    def noop(cls, *args, **kwargs):
        pass

    @classmethod
    def flatten(cls, lst):
        """Flattens a 2D list of lists."""

        return [nested_elem for elem in lst for nested_elem in elem]

    @classmethod
    def nested_dict(cls):
        """A nested default dictionary.

        Dictionaries in Python can become cumbersome if you constantly have to
        check if a key exists in a dictionary before proceeding. Using this as
        a dict definition allows the user to define arbitrarily nested values
        in the dictionary. Undefined nested values will return a defaultdict
        that, when cast to a boolean, will return False.

        Usage:
            my_dict = Utils.nested_dict()
            my_dict[k1][k2][k3] = value

        Taken from:
            http://stackoverflow.com/questions/16724788/how-can-i-get-python-to-automatically-create-missing-key-value-pairs-in-a-dictio
        """
        return collections.defaultdict(cls.nested_dict)

    @classmethod
    def convert_list_to_count_dict(cls, lst):

        dct = {}

        for val in lst:
            if val in dct:
                dct[val] += 1
            else:
                dct[val] = 1

        return dct

    @classmethod
    def convert_to_list(cls, e):
        """Convert to a list if not already a list."""
        return list(e) if not Utils.is_list(e) else e

