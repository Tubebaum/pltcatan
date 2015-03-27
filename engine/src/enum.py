class Enum(dict):
    """Enum class for Python 2.7.x (official one not released until 3.4.x).

    Inspired by:
    http://stackoverflow.com/questions/36932/how-can-i-represent-an-enum-in-python
    """

    def __getattr__(self, name):
        if name in self:
            return self[name]
        raise AttributeError