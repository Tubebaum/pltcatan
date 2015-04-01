# -*- coding: utf-8 -*-


class Utils(object):
    """A general utility class."""

    @classmethod
    def flatten(cls, lst):
        """Flattens a 2D list of lists."""

        return [nested_elem for elem in lst for nested_elem in elem]