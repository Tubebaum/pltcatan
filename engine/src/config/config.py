from types import *
from engine.src.lib.utils import Utils
from engine.src.config.game_config import game_config
from engine.src.config.type_config import type_config
from engine.src.config.type_mapping import type_mapping
from engine.src.exceptions import *


class Config(object):

    @classmethod
    def init_from_config(cls, obj, config_path):
        property_dict = Config.get(config_path)
        Utils.init_from_dict(obj, property_dict)

    @classmethod
    def pluck(cls, config_path, prop):
        target_dict = Config.get(config_path)
        return Utils.pluck(target_dict, prop, True)

    @classmethod
    def get(cls, dot_notation_str, dct=None, coerce_type=True):
        """Get a value from the main config dict given a dot notation string.

        E.g. if caller wants config['game']['points_to_win'], they can pass in
        as their dot_notation_str 'game.points_to_win'.

        See coerce() for effect of coerce_type flag.
        """

        if dct is None:
            dct = Config.config

        keys = dot_notation_str.split('.')

        def get_recursive(dct, keys):
            key = keys.pop(0)
            val = None

            # Get the value of the key if it's in the dict.
            if key in dct:
                val = dct.get(key)
            else:
                raise NoConfigValueDefinedException(dot_notation_str)

            # If we still have keys left, the property we want is nested
            # somewhere inside the value we fetched.
            if keys:
                if val:
                    return get_recursive(val, keys)
                else:
                    raise NoConfigValueDefinedException(dot_notation_str)
            # If we have no keys left, we've found the target value.
            else:
                return val

        value = get_recursive(dct, keys)

        if coerce_type:
            # print 'Pre-coerce {}'.format(value)
            value = Config.coerce(value, dot_notation_str)
            # print 'Post-coerce {}'.format(value)

        # Remove default value from dictionary type return value.
        if type(value) is dict:
            value = {k: value[k] for k in value.keys() if k != 'default'}

        return value

    @classmethod
    def coerce(cls, value, dot_notation_str):
        """Coerce the value to the type specified in type_config by given path.

        Sometimes the value stored at the specified path is not the type we
        need it to be. In this case, we can specify coerce_type = True. This
        will lead this method to get() the value stored in the config dict, and
        check if its type matches the type located at the same path in the
        type_config dict. If the types don't match, it uses a coercion function
        stored at type_mapping[from_type][to_type].
        """

        # Closure for coercing type.
        def coerce_type(value, from_type, to_type):
            if from_type == to_type:
                return value

            coercion_func = type_mapping[from_type][to_type]
            return coercion_func(value)

        result = value

        try:
            target_type = Config.get(dot_notation_str, Config.type_config, False)
            curr_type = type(value)
        except NoConfigValueDefinedException:
            # If no target type exists, return uncoerced value.
            return value

        # If target type is a dict, coerce key and value types.
        if type(target_type) is dict:

            # Structs are dicts but all their keys are not types, so they
            # shouldn't actually be coerced; they're just part of a path to
            # specify actual conversions.
            is_struct = len(filter(
                lambda key: type(key) == StringType,
                target_type.keys()
            )) != 0

            if is_struct:
                return value

            result = {}

            target_k_type = target_type.keys()[0]
            target_v_type = target_type.values()[0]

            for k, v in value.iteritems():
                coerced_k_value = coerce_type(k, type(k), target_k_type)
                coerced_v_value = coerce_type(v, type(v), target_v_type)

                result[coerced_k_value] = coerced_v_value

        # If target type not a dict, coerce value to target type directly.
        elif target_type != curr_type:
            result = coerce_type(value, curr_type, target_type)

        return result

    # The dictionary accessed by Config.get()
    config = game_config

    # A dictionary telling us what object types we should expect
    # for values in config.
    type_config = type_config

    type_mapping = type_mapping
