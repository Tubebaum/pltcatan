import ast

import ply.lex as lex
import ply.yacc as yacc

from utils import get_registry, trivial_from_registry, trivial

# Automatically build no-op nonterminals
register = get_registry()

def gen_function(name):
    return trivial_from_registry(name, register, suffix='_reg')

# Helper functions

def listify(p):
    p[0] = [p[1]]
    if len(p) > 2:
        p[0].extend(p[3])
    return p

# Token declarations

reserved = {
    'func': 'FUNC_DECL',
    'return': 'RETURN'
}
tokens = ['ID', 'NUM', 'NEWLINE'] + list(reserved.values())
literals = ['=', '+', '-', '*', '/', '(', ')', '{', '}', '[', ',', ']', '.', '"', '\'']

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID') # Check for reserved words
    return t

def t_NUM(t):
    r'\d+|\d+\.\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print "Integer value too large", t.value
        t.value = 0
    return t

t_ignore = " \t"

def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += t.value.count('\n')
    return t

def t_error(t):
    print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)

# Build the lexer
lex.lex()

# Parsing rules
precedence = (
    ('left','+','-'),
    ('left','*','/'),
    ('right','UMINUS'),
    )

# Simple expressions

@register('expr')
def p_id(p):
    """id : ID"""
    p[0] = ast.Name(p[1], ast.Load())

@register('expr')
def p_num(p):
    """num : NUM"""
    p[0] = ast.Num(p[1])

# Groupings

def p_expr_group(p):
    """expr : '(' expr ')'"""
    p[0] = p[2]

# Strings

@register('expr')
def p_list_braces(p):
    """list : '[' expr_list ']'"""
    p[0] = ast.List(p[2], ast.Load())

@register('expr')
def p_str(p):
    """str : '"' ID '"'
           | \"'\" ID \"'\""""
    p[0] = ast.Str(p[2])

# Statements

def p_stmt_expr(p):
    """stmt : expr"""
    p[0] = ast.Expr(p[1])

def p_stmt_assignment(p):
    """stmt : ID '=' expr"""
    p[0] = ast.Assign([ast.Name(p[1], ast.Store())], p[3])

def p_stmt_return(p):
    """stmt : RETURN expr
            | RETURN"""
    if len(p) > 2:
        p[0] = ast.Return(p[2])
    else:
        p[0] = ast.Return()

# Functions

@register('stmt')
def p_func(p):
    """func : FUNC_DECL ID '(' params ')' '{' body '}'"""
    args = ast.arguments(p[4], None, None, [])
    p[0] = ast.FunctionDef(p[2], args, p[7], [])

@register('expr')
def p_funccall(p):
    """funccall : ID '(' expr_list ')'"""
    p[0] = ast.Call(ast.Name(p[1], ast.Load()), p[3], [], None, None)

# Lists

def p_params(p):
    """params : param ',' params
              | param"""
    p = listify(p)

def p_param(p):
    """param : ID
             | empty"""
    p[0] = ast.Name(p[1], ast.Param())

def p_body_stmtlst(p):
    """body : NEWLINE stmtlst
            | stmtlst"""
    p[0] = p[2] if len(p) > 2 else p[1]

def p_stmtlst(p):
    """stmtlst : stmt NEWLINE stmtlst
               | stmt NEWLINE
               | stmt"""
    p = listify(p)

def p_in_params(p):
    """expr_list : opt_expr ',' expr_list
                 | opt_expr"""
    p = listify(p)

p_opt_expr = trivial('opt_expr', ['expr', 'empty'])

# Property access

@register('expr')
def p_expr_property(p):
   """property : expr '.' ID"""

   p[0] = ast.Attribute(p[1], p[3], ast.Load())

# Arithmetic

def p_expr_binop(p):
    """expr : expr '+' expr
            | expr '-' expr
            | expr '*' expr
            | expr '/' expr"""
    if   p[2] == '+': p[0] = ast.BinOp(p[1], ast.Add(), p[3]) #p[1] + p[3]
    elif p[2] == '-': p[0] = ast.BinOp(p[1], ast.Sub(), p[3]) #p[1] - p[3]
    elif p[2] == '*': p[0] = ast.BinOp(p[1], ast.Mult(), p[3]) #p[1] * p[3]
    elif p[2] == '/': p[0] = ast.BinOp(p[1], ast.Div(), p[3]) #p[1] / p[3]

def p_expr_uminus(p):
    """expr : '-' expr %prec UMINUS"""
    p[0] = ast.BinOp(p[2], ast.Mult(), ast.Num(-1))

# Terminal registration

p_expr_reg = gen_function('expr')
p_stmt_reg = gen_function('stmt')

def p_error(p):
    print "Syntax error at '%s'" % p.value

def p_empty(p):
    """empty :"""
    pass

yacc.yacc(start='stmt')

def parse_string(s):
    return yacc.parse(s)

if __name__ == '__main__':
    while 1:
        try:
            s = raw_input('>')
        except EOFError:
            break
        if not s: continue
        print ast.dump(yacc.parse(s))
