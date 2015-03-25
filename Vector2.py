class Vector2(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __key(self):
        return self.to_tuple()

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__key() == other.__key()
        else:
            return False

    def __hash__(self):
        return hash(self.__key())

    def __ne__(self, other):
        return not self.__eq__(other)

    def __mul__(self, scalar):
        return Vector2(scalar * self.x, scalar * self.y)

    def __rmul__(self, scalar):
        return self.__mul__(scalar)

    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    def to_tuple(self):
        return (self.x, self.y)

    def __str__(self):
        return str(self.to_tuple())
