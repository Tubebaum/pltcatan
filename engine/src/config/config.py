from types import *
from engine.src.lib.utils import Utils
from engine.src.config.game_config import game_config
from engine.src.config.type_config import type_config
from engine.src.config.type_mapping import type_mapping
from engine.src.exceptions import *
import pdb


class Config(object):

    is_coerced = False

    @classmethod
    def init_from_config(cls, obj, config_path):
        property_dict = Config.get(config_path)
        dct = { Utils.convert_format(k): v for (k, v) in property_dict.iteritems()}
        Utils.init_from_dict(obj, dct)

    @classmethod
    def pluck(cls, config_path, prop):
        target_dict = Config.get(config_path)
        return Utils.pluck(target_dict, prop, True)

    @classmethod
    def set(cls, value, dot_notation_str, dct=None):

        if dct is None:
            dct = Config.config

        keys = dot_notation_str.split('.')

        def set_recursive(dct, keys):
            if not keys:
                return dct

            key = keys.pop(0)
            val = None

            if key in dct:
                val = dct.get(key)
            else:
                raise NoConfigValueDefinedException(dot_notation_str)

            # If we still have keys left, the property we want to set is nested
            # somewhere inside the value we fetched.
            if keys:
                if val:
                    return set_recursive(val, keys)
                else:
                    raise NoConfigValueDefinedException(dot_notation_str)
            # If we have no keys left, we've found the target value.
            else:
                dct[key] = value

        set_recursive(dct, keys)


    @classmethod
    def get(cls, dot_notation_str, dct=None, remove_default=True):
        """Get a value from the main config dict given a dot notation string.

        E.g. if caller wants config['game']['points_to_win'], they can pass in
        as their dot_notation_str 'game.points_to_win'.

        See coerce() for effect of coerce_type flag.
        """

        if not Config.is_coerced:
            Config.coerce_all()

        if dct is None:
            dct = Config.config

        if not dot_notation_str:
            return dct

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

        if remove_default:
            # Remove default value from dictionary type return value.
            if type(value) is dict:
                value = {k: value[k] for k in value.keys() if k != 'default'}

        return value

    @classmethod
    def init(cls):
        Config.convert_keys()
        Config.coerce_all()

    @classmethod
    def convert_keys(cls):

        def convert(dct):
            for k, v in dct.iteritems():

                if type(k) is StringType:
                    dct.pop(k)
                    dct[Utils.convert_format(k)] = v

                if type(v) is dict:
                    convert(v)

        convert(Config.config)

    @classmethod
    def coerce_all(cls):
        Config.is_coerced = True
        Config.coerce_recursive('')

    @classmethod
    def coerce_recursive(cls, path_so_far):
        curr_value = Config.get(path_so_far, Config.config, False)

        try:
            target_type = Config.get(
                Config.get_default_path(path_so_far), Config.type_config, False)
        except NoConfigValueDefinedException:
            return

        is_struct = False

        if type(curr_value) is dict:
            is_struct = len(filter(
                lambda key: type(key) == StringType,
                target_type.keys()
            )) != 0

        if is_struct:
            for k, v in curr_value.iteritems():
                path = k if not path_so_far else '.'.join([path_so_far, k])
                Config.coerce_recursive(path)
        else:
            Config.set(
                Config.coerce(curr_value, type(curr_value), target_type),
                path_so_far
            )

    @classmethod
    def coerce(cls, value, from_type, to_type):

        if from_type == to_type:
            return value

        if from_type is dict:
            result = {}

            target_k_type = to_type.keys()[0]
            target_v_type = to_type.values()[0]

            for k, v in value.iteritems():
                coerced_k_value = Config.coerce(k, type(k), target_k_type)
                coerced_v_value = Config.coerce(v, type(v), target_v_type)

                result[coerced_k_value] = coerced_v_value

            return result
        else:
            coercion_func = type_mapping[from_type][to_type]
            return coercion_func(value)

    @classmethod
    def get_default_path(cls, dot_notation_str):
        # e.g. structure.player_built.road.cost =>
        #      structure.player_built.default.cost
        """
        If last prop is not a dict, replace second to last with default
        If last prop is a dict, e.g. structure.player_built.road
            if dict is a struct, replace last with default
            if dict isn't a struct, replace second to last with default
        """

        value = None
        path = None

        repl_index = -1

        while True:
            keys = dot_notation_str.split('.')

            try:
                keys[repl_index] = 'default'
                path = '.'.join(keys)
                value = Config.get(path, Config.type_config, False)
                break
            except NoConfigValueDefinedException:
                repl_index -= 1
            except IndexError:
                # No defaults; return as is.
                path = dot_notation_str
                break

        return path

    # The dictionary accessed by Config.get()
    config = game_config

    # A dictionary telling us what object types we should expect
    # for values in config.
    type_config = type_config

    type_mapping = type_mapping
