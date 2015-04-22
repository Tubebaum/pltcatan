#!/usr/bin/env python
import config
import argparse
import dill as pickle
import os
import shutil
import sys
sys.path.append('..')
from engine.src.game import Game
from engine.src.config.config import Config

properties = {}

def undot(property):
    '''
    Get the value of a dot.notated.property from the properties dict
    '''
    extended = properties
    extension = property.split('.')
    extension.reverse()
    while extension:
        extended = extended[extension.pop()]
    if isinstance(extended, dict) or isinstance(extended, list):
        return extended.copy()
    else:
        return extended

def extendVerbose(skit, property, value, extension):
    '''
    Extend properties using the verbose syntax where every extension must use an
    @extend explicitly
    '''
    skit[property] = undot(extension)
    for extended_property, extended_value in value.iteritems():
        if extended_property != '@extend':
            if isinstance(extended_value, str) and '+' in extended_value:
                extension, addition = extended_value.split('+')
                extended = undot(extension.strip())
                extended_value = extended + int(addition)
            skit[property][extended_property] = extended_value

def extendClean(skit, property, value, extension):
    explicit = extension['explicit-overwrite-only']
    extension = extension['value']
    extendVerbose(skit, property, value, extension)
    if explicit:
        for extended_property, extended_value in value.iteritems():
            if isinstance(extended_value, dict) and extended_property != '@extend':
                if needs_extending(extended_value):
                    skit[property][extended_property]['@extend'] = make_extend(extension, extended_property, explicit)
    return extension

def needs_extending(skit):
    children_structures = False
    for property, value in skit.iteritems():
        if isinstance(value, dict):
            children_structures = True
    return children_structures

def make_extend(extension, extended_property, explicit):
    return {'value': '%s.%s' % (extension, extended_property),
            'explicit-overwrite-only': explicit}

def extend(skit, parent=None):
    '''
    Replace all extended properties with the contents of the actual value
    denoted by the dot-notated property name and set any additional properties
    '''
    for property, value in skit.iteritems():
        if isinstance(value, dict):
            extension = value.get('@extend')
            if extension:
                if isinstance(extension, str):
                    extendVerbose(skit, property, value, extension)
                    extension = None
                else:
                    extension = extendClean(skit, property, value, extension)
            extend(skit[property], extension)

def replaceEngine(engine, skit):
    if isinstance(engine, dict):
        for property, value in engine.iteritems():
            if property == 'game':
                engine[property]['points_to_win'] = skit['game']['points-to-win']
            elif property == 'board':
                engine[property]['default_radius'] = skit['game']['board']['radius']
            elif property == 'development':
                for card, props in value.iteritems():
                    dev_card = skit['game']['cards']['development'].get(card.replace('_', '-'))
                    if dev_card:
                        engine[property][card]['count'] = dev_card['max-count']
                        engine[property][card]['description'] = dev_card['description']
            replaceEngine(engine[property], skit)

def compile(file, clean=False):
    '''
    Cleans tmp/ directory and reinitializes with compiled skit code
    '''
    base_file = os.path.basename(file)
    compile_file = 'tmp/' + base_file
    if clean:
        shutil.rmtree('tmp/', True)
        compile('default.skit')
    skit = config.parser.parse(open(file, 'r').read(), lexer=config.lexer)
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
    main_property = os.path.splitext(base_file)[0]
    properties[main_property] = skit.get(main_property)
    replaceEngine(Config.config, properties[main_property])
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
