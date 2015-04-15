import ast
from collections import defaultdict

import ply.lex as lex
import ply.yacc as yacc

from grammar_utils import get_registry, trivial_from_registry, trivial, gen_grammar
from utils import flatten

# Allow dependency injection using the predefined GameOracle
from oracle import ORACLE

def gen_access_func(var_name):
    """Generates an AST to access the given variable using the GameOracle

    Arguments:
        name -- a string representing the variable name

    Return:
        An AST representing a call to the GameOracle for the given variable
    """
    return ast.Call(ast.Attribute(ast.Name('ORACLE', ast.Load()), 'get', ast.Load()), [ast.Str(var_name)], [], None, None)

# Automatically build no-op nonterminals
register = get_registry()

def gen_function(name):
    """Generates a function for the given trivial nonterminal based on the registry

    Arguments:
        name -- a string representing the nonterminal to generate the function for

    Return:
        A trivial function p[0] = p[1] for the nonterminal
    """
    return trivial_from_registry(name, register, suffix='_reg')

# Helper functions

def listify(p, item_pos=1, list_pos=3, size_check=2):
    """Creates a list of values from the given nonterminal parse p

    Arguments:
        p -- a list representing the parse

    Named Arguments:
        item_pos (1) -- an int representing the position of the item at the head of the list
        list_pos (3) -- an int representing the position of the rest of the list
        size_check (2) -- an int representing the length of the parse of a single item of the list

    Return:
        The parse p, with p[0] set to the list of items
    """
    p[0] = [p[item_pos]]
    if len(p) > size_check:
        p[0].extend(p[list_pos])
    return p

# Token declarations

reserved = {
    'func': 'FUNC_DECL',
    'return': 'RETURN',
    'print': 'PRINT'
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

def p_stmt_print(p):
    """stmt : PRINT expr"""
    p[0] = ast.Print(None, p[2] if isinstance(p[2], list) else [p[2]], True)

# Functions

@register('stmt')
def p_top_func(p):
    """topfunc : FUNC_DECL '(' params ')' '{' opt_newline stmtlst '}'"""
    args = ast.arguments(p[3], None, None, [gen_access_func(param.id) for param in p[3]])
    p[0] = ast.FunctionDef("top", args, p[7], [])

@register('stmt')
def p_func(p):
    """func : FUNC_DECL ID '(' params ')' '{' opt_newline stmtlst '}'"""
    args = ast.arguments(p[4], None, None, [])
    p[0] = ast.FunctionDef(p[2], args, p[8], [])

@register('expr')
def p_funccall(p):
    """funccall : expr '(' expr_list ')'"""
    p[0] = ast.Call(p[1], p[3], [], None, None)

p_opt_newline = trivial('opt_newline', ['NEWLINE', 'empty'])

# Lists

def p_params(p):
    """params : param ',' params
              | param"""
    p = listify(p)

def p_param(p):
    """param : ID
             | empty"""
    if p[1]:
        p[0] = ast.Name(p[1], ast.Param())

def p_stmtlst(p):
    """stmtlst : stmt NEWLINE stmtlst
               | stmt opt_newline"""
    p = listify(p, size_check=3)

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

def p_expr_getitem(p):
    """expr : ID '[' expr ']'"""
    p[0] = ast.Subscript(ast.Name(p[1], ast.Load()), ast.Index(p[3]), ast.Load())

# Arithmetic

def p_expr_binop(p):
    """expr : expr '+' expr
            | expr '-' expr
            | expr '*' expr
            | expr '/' expr"""
    if   p[2] == '+': p[0] = ast.BinOp(p[1], ast.Add(), p[3])  # p[1] + p[3]
    elif p[2] == '-': p[0] = ast.BinOp(p[1], ast.Sub(), p[3])  # p[1] - p[3]
    elif p[2] == '*': p[0] = ast.BinOp(p[1], ast.Mult(), p[3]) # p[1] * p[3]
    elif p[2] == '/': p[0] = ast.BinOp(p[1], ast.Div(), p[3])  # p[1] / p[3]

def p_expr_uminus(p):
    """expr : '-' expr %prec UMINUS"""
    p[0] = ast.BinOp(p[2], ast.Mult(), ast.Num(-1))

# Terminal registration

p_expr_reg = gen_function('expr')
p_stmt_reg = gen_function('stmt')

# Meta terminals

def p_error(p):
    print "Syntax error at '%s'" % p.value

def p_empty(p):
    """empty :"""
    pass

yacc.yacc(start='topfunc')

def parse_string(s):
    """Parses a given string into a Python AST

    Arguments:
        s -- the string to parse into an AST

    Return:
        The AST representation of the provided code string
    """
    return ast.Module([yacc.parse(s)])

def parse_function(s, name='top'):
    """Parses a string representing a Skit function into a first-class Python function

    Arguments:
        s -- the string representing a Skit function to parse into a Python function

    Named Arguments:
        name ('top') -- a string representing the name to give the function being parsed

    Return:
        A first-class Python function that performs the actions of the Skit function provided
    """
    exec(compile(ast.fix_missing_locations(parse_string(s)), filename='<ast>', mode='exec'))
    locals()[name].__name__ = locals()[name].func_name = name
    return locals()[name]

env = locals()

def print_grammar():
    """Prints the grammar formed by the functions in this file
    """
    p_funcs = [func for name, func in env.items() if
               name.startswith('p_') and
               hasattr(func, '__call__') and
               name != 'p_error']
    print p_funcs
    grammar = defaultdict(list)
    for name, nonterminals in [func.__doc__.split(':') for func in p_funcs]:
        grammar[name.strip()].append(nonterminals)
    grammar = {key: [item for item in flatten(
        [[docstr.strip() for docstr in item.split('|')] for item in value]
    )] for key, value in grammar.iteritems()}

    for name, nonterminals in grammar.iteritems():
        print gen_grammar(name, sorted(nonterminals), indent=0) + '\n'

if __name__ == '__main__':
    while 1:
        try:
            s = raw_input('>')
        except EOFError:
            break
        if not s: continue
        print ast.dump(parse_string(s))
