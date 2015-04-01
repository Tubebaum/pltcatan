import lex

tokens = (
    'COLON',
    'LCURLY',
    'RCURLY',
    'LBRACKET',
    'RBRACKET',
    'COMMA',
    'DOT',
    'WILD',
    'ID',
    'STR',
    'FUNC',
    'NUM'
)
reserved = {
    'uniform': 'UNIFORM'
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
t_STR = r'".*"'
t_ignore = ' \t'

def t_FUNC(t):
    r'func[^\}]*}'
    return t

def t_ID(t):
    r'[A-Za-z][A-Za-z-]*'
    t.type = reserved.get(t.value, 'ID')
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

import yacc

def p_property_value(p):
    'property : ID COLON value'
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
    p[0] = p[1]

def p_value_uniform(p):
    'value : UNIFORM'
    p[0] = 'uniform'

def p_value_func(p):
    'value : FUNC'
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
    print "Syntax error in input!"

parser = yacc.yacc()
