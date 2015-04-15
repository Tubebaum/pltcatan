#!/usr/bin/env python
import config
import argparse
import dill as pickle
import os
import shutil
import sys
sys.path.append('..')
from engine.src.game import Game

def compile(file, clean=False):
    '''
    Cleans tmp/ directory and reinitializes with compiled skit code
    '''
    if clean:
        shutil.rmtree('tmp/', True)
    skit = config.parser.parse(open(args.file, 'r').read())
    base_file = os.path.basename(args.file)
    compile_file = 'tmp/' + base_file
    if not os.path.isdir('tmp/'):
        os.makedirs('tmp/')
    pickle.dump(skit, open(compile_file, 'wb'))
    return skit

def run(file):
    '''
    Runs skit game
    Recompiles skit code only if code has been changed
    '''
    base_file = os.path.basename(args.file)
    compile_file = 'tmp/' + base_file
    skit = None
    if not os.path.isfile(compile_file) or\
        os.path.getmtime(file) > os.path.getmtime(compile_file):
        skit = compile(file)
    else:
        skit = pickle.load(open(compile_file, 'rb'))


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
