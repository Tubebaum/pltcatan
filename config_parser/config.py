import ply.lex as lex
import ply.yacc as yacc
import sys
import os
sys.path.append('..')
from imperative_parser.parser import parse_function

tokens = (
    'COLON',
    'LCURLY',
    'RCURLY',
    'LBRACKET',
    'RBRACKET',
    'COMMA',
    'DOT',
    'WILD',
    'PLUS',
    'ID',
    'EXTENSION',
    'STR',
    'FUNC',
    'NUM'
)

reserved = {
    'uniform': 'UNIFORM',
    'none': 'NONE'
}

tokens += tuple(reserved.values())
t_COLON = r':'
t_LCURLY = r'\{'
t_RCURLY = r'\}'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_COMMA = r','
t_DOT = r'\.'
t_WILD = r'\*'
t_PLUS = r'\+'
t_STR = r'".*"'
t_ignore = ' \t'

def t_FUNC(t):
    r'func[^\{]*{'
    func = t.value
    bracks = 1
    pos = t.lexer.lexpos
    pos2 = t.lexpos
    lexdata = t.lexer.lexdata[t.lexer.lexpos:]
    for c in lexdata:
        t.lexer.lexpos += 1
        func += c
        if c == '{':
            bracks += 1
        elif c == '}':
            bracks -= 1
        elif c == '\n':
            t.lexer.lineno += 1
        if not bracks:
            break
    t.value = func
    return t

def t_ID(t):
    r'[A-Za-z][A-Za-z-]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_EXTENSION(t):
    r'@extend'
    return t

def t_NUM(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print "Illegal character '%s'" % t.value[0]

lexer = lex.lex()

def p_property_value(p):
    'property : ID COLON value'
    p[0] = {p[1]: p[3]}

def p_property_extension(p):
    'property : EXTENSION COLON value'
    p[0] = {p[1]: p[3]}

def p_value_structure(p):
    'value : structure'
    p[0] = p[1]

def p_value_list(p):
    'value : LBRACKET list RBRACKET'
    p[0] = p[2]

def p_value_dots(p):
    'value : dots'
    p[0] = p[1]

def p_value_num(p):
    'value : NUM'
    p[0] = p[1]

def p_value_str(p):
    'value : STR'
    p[0] = p[1].strip('\'"')

def p_value_uniform(p):
    'value : UNIFORM'
    p[0] = 'uniform'

def p_value_none(p):
    'value : NONE'
    p[0] = None

def p_value_func(p):
    'value : FUNC'
    #p[0] = parse_function(p[1])
    p[0] = p[1]

def p_structure_properties(p):
    'structure : LCURLY properties RCURLY'
    p[0] = p[2]

def p_list_comma(p):
    'list : value COMMA list'
    p[1] = [p[1]]
    p[1].extend(p[3])
    p[0] = p[1]

def p_list_value(p):
    'list : value'
    p[0] = [p[1]]

def p_dots_dot(p):
    'dots : ID DOT dots'
    p[0] = p[1] + '.' + p[3]

def p_dots_plus(p):
    'dots : ID PLUS NUM'
    p[0] = p[1] + ' + ' + str(p[3])

def p_dots_id(p):
    'dots : ID'
    p[0] = p[1]

def p_dots_wild(p):
    'dots : WILD'
    p[0] = '*'

def p_properties_comma(p):
    'properties : property COMMA properties'
    p[3].update(p[1])
    p[0] = p[3]

def p_properties_property(p):
    'properties : property'
    p[0] = p[1]

def p_error(p):
    print p
    print "Syntax error in input!"

parser = yacc.yacc()
