# TODO: Cleanup. Separate module registration with game run logic?

import sys
import os

# Add engine package to Python path.
sys.path.insert(1, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from engine.src.game import Game

g = Game()

