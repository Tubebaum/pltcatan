class ConfigObject(object):

    def __setattr__(self, key, value):
        self.__dict__[key] = value
