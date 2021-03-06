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
        extended = extended.get(extension.pop(), properties)
        if extended is properties:
            return extended
    if isinstance(extended, dict) or isinstance(extended, list):
        return extended.copy()
    else:
        return extended

def extend_verbose(skit, property, value, extension):
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

def extend_clean(skit, property, value, extension):
    '''
    Extend properties using the cleaner syntax where one mention of @extend and
    explicit-overwrite-only set to true cascades the extension gracefully
    '''
    explicit = extension['explicit-overwrite-only']
    extension = extension['value']
    extend_verbose(skit, property, value, extension)
    if explicit:
        for extended_property, extended_value in value.iteritems():
            if isinstance(extended_value, dict) and extended_property !=\
                    '@extend':
                if needs_extending(extended_value):
                    skit[property][extended_property]['@extend'] =\
                            make_extend(extension, extended_property, explicit)
    return extension

def needs_extending(skit):
    '''
    Checks to see if a structure needs to be extended
    '''
    children_structures = False
    if isinstance(skit, dict):
        return True
    for property, value in skit.iteritems():
        if isinstance(value, dict):
            children_structures = True
    return children_structures

def make_extend(extension, extended_property, explicit):
    '''
    Coerce the structure to look like a verbose extension
    '''
    return {'value': '%s.%s' % (extension, extended_property),
            'explicit-overwrite-only': explicit}

def replace(value):
    '''
    Replace an import alias with its actual value
    '''
    if '+' in value:
        terms = value.split('+')
        sum = 0
        for term in terms:
            term = term.strip()
            if term.isdigit():
                replacement = float(term)
            else:
                replacement = undot(term.strip())
                if replacement is properties:
                    sum = None
                    break
            sum += float(replacement)
        if sum is None:
            replacement = value
        else:
            replacement = sum
    else:
        replacement = undot(value.strip())
    if replacement is properties:
        return value
    else:
        return replacement

def extend(skit, parent=None):
    '''
    Replace all extended properties with the contents of the actual value
    denoted by the dot-notated property name and set any additional properties
    '''
    for property, value in skit.iteritems():
        if isinstance(value, str):
            replacement = replace(value)
            if isinstance(replacement, dict):
                replacement = replacement.get(property, replacement)
            skit[property] = replacement
        if isinstance(value, dict):
            extension = value.get('@extend')
            if extension:
                if isinstance(extension, str):
                    extend_verbose(skit, property, value, extension)
                    extension = None
                else:
                    extension = extend_clean(skit, property, value, extension)
            extend(skit[property])

def imports(full_file, file):
    '''
    Compiles every skit structure that is imported in addition to
    the top-level structure
    '''
    imports = file.split('\n')
    line_no = 0
    chars_read = 0
    for line in imports:
        line_length = len(line)
        if line:
            line = line.split()
            if line[0] == '@import':
                if len(line) < 4:
                    print 'Error: Invalid @import on line', line_no
                    return None
                if line[1][-1] == '/':
                    if line[1][0] == '.':
                        properties[line[3]], success = compile(full_file + line[1] +\
                                '__value__.skit', as_name=line[3])
                    elif line[1][0] == '/':
                        properties[line[3]], success = compile(line[1] +\
                                '__value__.skit', as_name=line[3])
                else:
                    if line[1][0] == '.':
                        properties[line[3]], success = compile(full_file + line[1] +\
                                '.skit')
                    elif line[1][0] == '/':
                        properties[line[3]], success = compile(line[1] + '.skit')

            else:
                break
        line_no += 1
        chars_read += line_length
    if chars_read > 0:
        chars_read += 1
    return file[chars_read:]

def compile(file, clean=False, as_name=None):
    '''
    Cleans tmp/ directory and reinitializes with compiled skit code
    '''
    full_file = os.path.dirname(file) + '/'
    base_file = os.path.basename(file)
    compile_file = 'tmp/' + base_file
    if clean:
        shutil.rmtree('tmp/', True)
        compile('default.skit')
    file = open(file, 'r').read()
    file = imports(full_file, file)
    skit, succeeded = config.parse(file)
    main_property = os.path.splitext(base_file)[0]
    extend(skit)
    if as_name:
        properties[as_name] = skit
        main_property = as_name
    else:
        properties[main_property] = skit.get(main_property)
    if not os.path.isdir('tmp/'):
        os.makedirs('tmp/')
    pickle.dump(skit, open(compile_file, 'wb'))
    return skit, succeeded

def run(file):
    '''
    Runs skit game
    Recompiles skit code only if code has been changed
    '''
    _, success = compile('default.skit')
    if success:
        base_file = os.path.basename(file)
        compile_file = 'tmp/' + base_file
        skit = None
        if not os.path.isfile(compile_file) or\
            os.path.getmtime(file) > os.path.getmtime(compile_file):
            skit = compile(file)[0]
        else:
            skit = pickle.load(open(compile_file, 'rb'))
        main_property = os.path.splitext(base_file)[0]
        properties[main_property] = skit.get(main_property)
        Config.config = properties[main_property]
        Config.init()
        game = Game()
        skit = skit.get(os.path.splitext(base_file)[0], None)
        # TODO: restore after engine syncs config dict format
        # if skit.get('game', None):
        game.start()
    else:
        print "Build failed, check the log for errors"
        sys.exit(1)

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
