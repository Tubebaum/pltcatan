#!/usr/bin/env python
import sys
import config

if __name__ == '__main__':
    game = config.parser.parse(open('default.skit', 'r').read())
    print game
