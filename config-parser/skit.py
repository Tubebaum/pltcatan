#!/usr/bin/env python
import config
import argparse
import dill as pickle
import os
import shutil
import sys
sys.path.append('..')
from engine.src.game import Game

properties = {}

def extend(skit):
    '''
    Replace all extended properties with the contents of the actual value
    denoted by the dot-notated property name and set any additional properties
    '''
    for property, value in skit.iteritems():
        if isinstance(value, dict):
            extension = value.get('@extend')
            if extension:
                extended = properties
                extension = extension.split('.')
                extension.reverse()
                while extension:
                    extended = extended[extension.pop()]
                skit[property] = extended.copy()
                for extended_property, extended_value in value.iteritems():
                    if extended_property != '@extend':
                        skit[property][extended_property] = extended_value
            extend(skit[property])

def compile(file, clean=False):
    '''
    Cleans tmp/ directory and reinitializes with compiled skit code
    '''
    base_file = os.path.basename(file)
    compile_file = 'tmp/' + base_file
    if clean:
        shutil.rmtree('tmp/', True)
        compile('default.skit')
    skit = config.parser.parse(open(file, 'r').read())
    main_property = os.path.splitext(base_file)[0]
    extend(skit)
    properties[main_property] = skit.get(main_property)
    if not os.path.isdir('tmp/'):
        os.makedirs('tmp/')
    pickle.dump(skit, open(compile_file, 'wb'))
    return skit

def run(file):
    '''
    Runs skit game
    Recompiles skit code only if code has been changed
    '''
    compile('default.skit')
    base_file = os.path.basename(file)
    compile_file = 'tmp/' + base_file
    skit = None
    if not os.path.isfile(compile_file) or\
        os.path.getmtime(file) > os.path.getmtime(compile_file):
        skit = compile(file)
    else:
        skit = pickle.load(open(compile_file, 'rb'))
    game = Game()
    skit = skit.get(os.path.splitext(base_file)[0], None)
    if skit.get('game', None):
        game.start()

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser(description='Skit compiler')
    arg_parser.add_argument('file', help='Skit file')
    arg_parser.add_argument('-c', '--compile', action='store_true',
        help='Only run compile steps')
    args = arg_parser.parse_args()
    if args.compile:
        compile(args.file, True)
    else:
        run(args.file)
