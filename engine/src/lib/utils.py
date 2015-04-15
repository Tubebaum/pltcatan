# -*- coding: utf-8 -*-
import collections


class Utils(object):
    """A general utility class."""

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
