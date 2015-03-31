import lex as lex
tokens = (
    'COLON',
    'LCURLY',
    'RCURLY',
    'LBRACKET',
    'RBRACKET',
    'COMMA',
    'ID',
    'STR',
    'FUNC',
    'NUM'
)

t_COLON = r':'
t_LCURLY = r'\{'
t_RCURLY = r'\}'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_COMMA = ','
t_ID = r'[A-Za-z][A-Za-z-]*'
t_STR = r'".*"'
t_ignore = ' \t'

def t_FUNC(t):
    r'func[^\}]*}'
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
