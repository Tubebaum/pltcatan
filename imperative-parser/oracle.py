from collections import defaultdict

class StateNotFound(Exception):
    """Thrown when a dependency injection tries to inject a variable that isn't part of the declared game state
    """
    pass


class GameOracle(object):
    """A wrapper object for the game state, providing a simple interface to isolate development of the imperative
    parser from the game engine
    """

    def __init__(self, state={}):
        """Creates an instance of a GameOracle

        Named Arguments:
            state ({}) -- a dictionary containing references from variable name strings to game state objects

        Return:
            A GameOracle which can access the provided state dictionary
        """
        self.game_state = state

    def get(self, var):
        """Get a variable from the GameOracle's state

        Arguments:
            var -- a string representing the name of the variable to retrieve

        Return:
            The value of the variable being retrieved

        Throws:
            StateNotFound -- when a state being accessed isn't present in the state dict
        """
        try:
            return self.game_state[var]
        except KeyError:
            raise StateNotFound("Variable \"%s\" not present in game state" % var)

    def set(self, name, var):
        """Set a particular variable in the state dict to a particular value

        Arguments:
            name -- a string representing the name to store the variable under
            var -- the value to store for the variable
        """
        self.game_state[name] = var

# Access game state through the game oracle
ORACLE = GameOracle({
    'game': defaultdict(list)
})