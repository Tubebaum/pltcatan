# TODO: Cleanup. Separate module registration with game run logic?

# Add engine package to Python path.
import sys
import os

sys.path.insert(1, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Catch SIGINT for prettier force quit handling.
import signal

def signal_handler(signal, frame):
    print '\nYou force quit the game.'
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)


# Run main game loop.
from engine.src.game import Game

g = Game()
g.start()
