#!/usr/bin/env python
import sys
import config
import skit

passed_all = True

def dummy():
    return 0

recognized_types = [type(''), type(0), type(dict()), type(list()), type(None),\
        type(dummy)]
function_names = ['play-card', 'draw-card']
string_names = ['name', 'description', 'position-type']
int_names = ['points-to-win', 'player-count', 'radius', 'tile-count', 'count',\
        'point-value', 'base-yield']
structure_names = ['game', 'board', 'card', 'development', 'structure',\
        'player-built']

def type_per_name(skit, property, value):
    can_be_none = False
    global passed_all
    if property in function_names:
        if type(value) != type(dummy):
            print 'Error: property %s does not contain a function' % property
            print 'Actual type: %s', type(value)
            passed_all = False
    elif property in string_names:
        if type(value) != type(''):
            print 'Error: property %s does not contain a string' % property
            print 'Actual type: %s', type(value)
            passed_all = False
    elif property in int_names:
        if type(value) != type(0):
            print 'Error: property %s does not contain an integer' % property
            print 'Actual type: %s', type(value)
            passed_all = False
    elif property in structure_names:
        if type(value) != type(dict()):
            print 'Error: property %s does not contain a dict' % property
            print 'Actual type: %s', type(value)
            passed_all = False

def test_types(skit):
    if type(skit) not in recognized_types:
        print 'Error: %s has unrecognized type', (skit, type(skit))
    if isinstance(skit, dict):
        for property, value in skit.iteritems():
            if property == 'default' and not skit[property].get('game', None):
                continue
            else:
                type_per_name(skit, property, value)
            test_types(value)

if __name__ == '__main__':
    game = config.parser.parse(open('default.skit', 'r').read())
    default = skit.compile('default.skit')
    test_types(game)
    test_dict = {'test': {'game': {'points-to-win': 5 } } }
    test_skit = 'test: { game: { points-to-win: 5 } }'
    compiled_skit = config.parser.parse(test_skit)
    if test_dict != compiled_skit:
        print 'Error: Static test dict does not match compiled test.skit'
        print 'Static test dict: %s', test_dict
        print 'Compiled test.skit: %s', compiled_skit
        passed_all = False
    test_dict['test']['game']['points-to-win'] = 10
    if test_dict == compiled_skit:
        print 'Error: Static test dict matches compiled test.skit with lower \
points to win'
        print 'Static test dict: %s', test_dict
        print 'Compiled test.skit: %s', compiled_skit
        passed_all = False
    test_skit = 'test: { game: { points-to-win: default.game.points-to-win } }'
    compiled_skit = config.parser.parse(test_skit)
    skit.extend(compiled_skit)
    if test_dict != compiled_skit:
        print 'Error: Static test dict does not match compiled test.skit\'s \
points-to-win'
        print 'Static test dict: %s', test_dict
        print 'Compiled test.skit: %s', compiled_skit
        passed_all = False
    test_skit = 'test: { game: default.game }'
    first_compile = config.parser.parse(test_skit)
    second_compile = config.parser.parse(test_skit)
    if first_compile != second_compile:
        print 'Error: Equivalent skit structures do not match when compiled'
        print 'Static test dict: %s', test_dict
        print 'Compiled test.skit: %s', compiled_skit
        passed_all = False
    skit.extend(first_compile)
    skit.extend(second_compile)
    if first_compile != second_compile:
        print 'Error: Equivalent skit structures do not match when extended'
        print 'Static test dict: %s', test_dict
        print 'Compiled test.skit: %s', compiled_skit
        passed_all = False
    first_skit = 'skit: { one: { a: 5, b: 6, c: 4 }, two: { b: 6, a: 5, c: 4 } }'
    second_skit = 'skit: { two: { b: 6, a: 5, c: 4 }, one: { a: 5, b: 6, c: 4 } }'
    first_compile = config.parser.parse(first_skit)
    second_compile = config.parser.parse(second_skit)
    if first_compile != second_compile:
        print 'Error: Semantically skit structures do not match when extended'
        print 'Static test dict: %s', test_dict
        print 'Compiled test.skit: %s', compiled_skit
        passed_all = False
    if passed_all:
        print 'Passed every test!'
