import ast
from collections import defaultdict

import ply.lex as lex
import ply.yacc as yacc

from grammar_utils import get_registry, trivial_from_registry, trivial, gen_grammar
from utils import flatten, find_column

# Allow dependency injection using the predefined GameOracle
from oracle import ORACLE

def gen_access_func(var_name):
    """Generates an AST to access the given variable using the GameOracle

    Args:
        name (String): A string representing the variable name

    Returns:
        ast.Call. An AST representing a call to the GameOracle for the given variable
    """
    return ast.Call(ast.Attribute(ast.Name('ORACLE', ast.Load()), 'get', ast.Load()), [ast.Str(var_name)], [], None, None)

class RewriteInjected(ast.NodeTransformer):
    def __init__(self, injected):
        """Creates a NodeTransformer object to replace calls to injected parameters with calls to a lookup table

        Args:
            injected (Iterable): An iterable representing the list of injected parameter names

        Returns:
            An instance of RewriteInjected whose visit method will rewrite the injected nodes
        """
        super(RewriteInjected, self).__init__()
        self.injected = set(injected)

    def visit_Name(self, node):
        if node.id in self.injected:
            return ast.copy_location(ast.Subscript(
                value=ast.Name(id=node.id, ctx=ast.Load()),
                slice=ast.Index(value=ast.Num(0)),
                ctx=node.ctx
            ), node)
        else:
            return self.generic_visit(node)

# Automatically build no-op nonterminals
register = get_registry()

def gen_function(name):
    """Generates a function for the given trivial nonterminal based on the registry

    Args:
        name (String): A string representing the nonterminal to generate the function for

    Returns:
        Func. A trivial function p[0] = p[1] for the nonterminal
    """
    return trivial_from_registry(name, register, suffix='_reg')

# Helper functions

def listify(p, item_pos=1, list_pos=3, size_check=2):
    """Creates a list of values from the given nonterminal parse p

    Args:
        p (List): A list representing the parse

    Named Args:
        item_pos (Int): 1 -- An int representing the position of the item at the head of the list
        list_pos (Int): 3 -- An int representing the position of the rest of the list
        size_check (Int): 2 -- An int representing the length of the parse of a single item of the list

    Returns:
        List. The parse p, with p[0] set to the list of items
    """
    p[0] = [p[item_pos]] if p[item_pos] else []
    if len(p) > size_check:
        p[0].extend(p[list_pos])
    return p

# Token declarations

# TODO allow reserved words in strings
reserved = {k: k.upper() for k in [
    'func',
    'return',
    'print',
    'if',
    'else',
    'or',
    'and',
    'not',
    'while',
    'for',
    'to'
]}
tokens = ['ID', 'NUM', 'COMPOP', 'AUGASSIGN', 'NEWLINE', 'IN', 'STRING'] + list(reserved.values())
literals = ['=', '+', '-', '*', '/', '(', ')', '{', '}', '[', ',', ']', '.', '@']

def t_STRING(t):
    r'\"(\\.|[^"])*\"|\'(\\.|[^"])*\''
    t.value = t.value.strip('"').strip("'")
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID') # Check for reserved words
    return t

def t_NUM(t):
    r'\d+|\d+\.\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print 'Integer value too large', t.value
        t.value = 0
    return t

t_COMPOP = r'==|<=|>=|<|>|!='
t_AUGASSIGN = r'\+=|-=|\*=|/='
t_IN = r':='

t_ignore = " \t"

def t_NEWLINE(t):
    r'\n\s+'
    t.lexer.lineno += t.value.count('\n')
    return t

def t_error(t):
    print 'Illegal character "%s"' % t.value[0]

# Build the lexer
lexer = lex.lex()

# Parsing rules
precedence = (
    ('left','+','-'),
    ('left','*','/'),
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'COMPOP'),
    ('left', 'TO'),
    ('right', 'NOT'),
    ('right','UMINUS'),
    ('right', '('),
    ('left', '['),
    ('left', '.')
)

# Simple expressions

@register('expr')
def p_id(p):
    """id : ID"""
    p[0] = ast.Name(p[1], ast.Load())

def p_store_id(p):
    """store_id : ID"""
    p[0] = ast.Name(p[1], ast.Store())

def p_assign_id(p):
    """assign_id : assign_lst"""
    p[0] = ast.Tuple(p[1], ast.Store()) if len(p[1]) > 1 else p[1][0]

def p_assign_lst(p):
    """assign_lst : store_id ',' assign_lst
                  | store_id"""
    p = listify(p)

p_store_other = trivial('store_id', ['property', 'getitem'])

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
def p_str(p):
    """str : STRING"""
    p[0] = ast.Str(p[1])

# Statements

def p_stmt_expr(p):
    """stmt : expr"""
    p[0] = ast.Expr(p[1])

def p_stmt_assignment(p):
    """stmt : assign_id '=' expr"""
    p[0] = ast.Assign([p[1]], p[3])

def p_stmt_aug_assignment(p):
    """stmt : store_id AUGASSIGN expr"""
    symbol_conversions = {
        '+=': ast.Add,
        '-=': ast.Sub,
        '*=': ast.Mult,
        '/=': ast.Div
    }
    p[0] = ast.AugAssign(p[1], symbol_conversions[p[2]](), p[3])

def p_stmt_return(p):
    """stmt : RETURN expr
            | RETURN"""
    if len(p) > 2:
        p[0] = ast.Return(p[2])
    else:
        p[0] = ast.Return(None)

def p_stmt_print(p):
    """stmt : PRINT expr"""
    p[0] = ast.Print(None, p[2] if isinstance(p[2], list) else [p[2]], True)

# Functions

@register('stmt')
def p_top_func(p):
    """topfunc : FUNC '(' params ')' '{' opt_newline body '}'"""
    if p[3]:
        args = ast.arguments([ast.Name('self', ast.Param())] + map(lambda x: x[0], p[3]), None, None, [gen_access_func(param[0].id) for param in p[3]])
    else:
        args = ast.arguments([], None, None, [])
    p[7] = [RewriteInjected([param[0].id for param in p[3]]).visit(node) for node in p[7]]
    p[0] = [ast.FunctionDef("top", args, p[7], [])]

@register('stmt')
def p_func(p):
    """func : FUNC ID '(' params ')' '{' opt_newline body '}'"""
    if p[4]:
        arg_names, defaults = tuple([filter(lambda x: x is not None, item) for item in zip(*p[4])])
        args = ast.arguments(list(arg_names), None, None, list(defaults))
    else:
        args = ast.arguments([], None, None, [])
    p[0] = ast.FunctionDef(p[2], args, p[8], [])

@register('expr')
def p_funccall(p):
    """funccall : expr '(' opt_newline expr_list ')'"""
    keywords = filter(lambda x: isinstance(x, ast.keyword), p[4])
    exprs = filter(lambda x: not isinstance(x, ast.keyword), p[4])
    p[0] = ast.Call(p[1], exprs, keywords, None, None)

@register('expr')
def p_lambda(p):
    """lambda : '@' '(' params ')' expr"""
    if p[3]:
        arg_names, defaults = tuple([filter(lambda x: x is not None, item) for item in zip(*p[3])])
        args = ast.arguments(list(arg_names), None, None, list(defaults))
    else:
        args = ast.arguments([], None, None, [])
    p[0] = ast.Lambda(args, p[5])

def p_body(p):
    """body : stmtlst
            | empty"""
    if p[1]:
        p[0] = p[1]
    else:
        p[0] = [ast.Pass()]

p_opt_newline = trivial('opt_newline', ['NEWLINE', 'empty'])

# Boolean logic

@register('expr')
def p_compare(p):
    """compare : expr COMPOP expr"""
    symbol_conversions = {
        '==': ast.Eq,
        '!=': ast.NotEq,
        '<=': ast.LtE,
        '>=': ast.GtE,
        '<': ast.Lt,
        '>': ast.Gt
    }

    p[0] = ast.Compare(p[1], [symbol_conversions[p[2]]()], [p[3]])

def p_bool_expr(p):
    """expr : expr AND expr
            | expr OR expr"""
    symbol_conversion = {
        'and': ast.And,
        'or': ast.Or
    }
    if isinstance(p[1], ast.BoolOp) and isinstance(p[1].op, symbol_conversion[p[2]]):
        p[1].values.append(p[3])
        p[0] = p[1]
    else:
        p[0] = ast.BoolOp(symbol_conversion[p[2]](), [p[1], p[3]])

def p_expr_not(p):
    """expr : NOT expr %prec NOT"""
    p[0] = ast.UnaryOp(ast.Not(), p[2])

# Conditionals

@register('stmt')
def p_if(p):
    """if : IF expr '{' opt_newline body '}' opt_else"""
    p[0] = ast.If(p[2], p[5], p[7])

def p_opt_else(p):
    """opt_else : ELSE '{' opt_newline body '}'
                | empty"""
    if len(p) > 2:
        p[0] = p[4]
    else:
        p[0] = []

def p_opt_elseif(p):
    """opt_else : ELSE expr '{' opt_newline body '}' opt_else"""
    p[0] = [ast.If(p[2], p[5], p[7])]

# Loops
@register('stmt')
def p_while(p):
    """while : WHILE expr '{' opt_newline body '}'"""
    p[0] = ast.While(p[2], p[5], [])

@register('stmt')
def p_for(p):
    """for : FOR ID IN expr '{' opt_newline body '}'"""
    p[0] = ast.For(ast.Name(p[2], ast.Store()), p[4], p[7], [])

@register('expr')
def p_range(p):
    """to : expr TO expr"""
    p[0] = ast.Call(ast.Name('range', ast.Load()), [p[1], p[3]], [], None, None)

# Lists

def p_params(p):
    """params : param ',' opt_newline params
              | param"""
    p = listify(p, list_pos=4)

def p_param(p):
    """param : ID
             | ID '=' expr
             | empty"""
    if p[1]:
        p[0] = (ast.Name(p[1], ast.Param()), None if len(p) < 3 else p[3])

def p_stmtlst(p):
    """stmtlst : stmt NEWLINE stmtlst
               | stmt opt_newline"""
    p = listify(p, size_check=3)

def p_in_params(p):
    """expr_list : opt_expr ',' opt_newline expr_list
                 | opt_expr"""
    p = listify(p, list_pos=4)

p_opt_expr = trivial('opt_expr', ['expr', 'empty'])

def p_opt_expr_default(p):
    """opt_expr : ID '=' expr"""
    p[0] = ast.keyword(p[1], p[3])

@register('expr')
def p_list_braces(p):
    """list : '[' expr_list ']'"""
    p[0] = ast.List(p[2], ast.Load())

# Property access

@register('expr')
def p_expr_property(p):
   """property : expr '.' ID"""

   p[0] = ast.Attribute(p[1], p[3], ast.Load())

@register('expr')
def p_expr_getitem(p):
    """getitem : expr '[' expr ']'"""
    p[0] = ast.Subscript(p[1], ast.Index(p[3]), ast.Load())

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
    if isinstance(p[2], ast.Num):
        p[2].n *= -1
        p[0] = p[2]
    else:
        p[0] = ast.UnaryOp(ast.USub(), p[2])

# Terminal registration

p_expr_reg = gen_function('expr')
p_stmt_reg = gen_function('stmt')

# Meta terminals

# Globals for communicating with p_error
# This is a code smell, but I don't think there's any easy way of
# communicating this otherwise
LINE_OFFSET = 1
COL_OFFSET = 1
FUNC_STR = ''

def p_error(p):
    print '[%d:%d] Syntax error at "%s"' % (p.lineno + LINE_OFFSET - 1, find_column(FUNC_STR, p) + COL_OFFSET - 2, p.value)

def p_empty(p):
    """empty :"""
    pass

test_parser = yacc.yacc(start='stmtlst')
parser = yacc.yacc(start='topfunc')

class BadParseException(Exception):
    def __init__(self, *args, **kwargs):
        super(self, BadParseException).__init__(*args, **kwargs)

def parse_string(s, debug=False, testing=False):
    """Parses a given string into a Python AST

    Args:
        s (String): The string to parse into an AST

    Named Args:
        debug (Bool): False -- A boolean representing whether to print debug info
        testing (Bool): False -- A boolean representing whether to use 'stmtlst' or 'topfunc' as the starting symbol

    Returns:
        ast.Module. The AST representation of the provided code string
    """
    if testing:
        body = test_parser.parse(s.strip(), debug=debug, lexer=lexer)
    else:
        body = parser.parse(s.strip(), debug=debug, lexer=lexer)
    return ast.Module(body)

def parse_function(func_str, name='top', debug=False, line_offset=1, col_offset=1):
    """Parses a string representing a Skit function into a first-class Python function

    Args:
        func_str (String): The string representing a Skit function to parse into a Python function

    Named Args:
        name (String): 'top' -- A string representing the name to give the function being parsed
        debug (Bool): False -- A boolean representing whether to print debug info
        line_offset (Int): 0 -- An int representing the line offset at which the function was found
        col_offset (Int): 0 -- An int representing the column offset at which the function was found

    Returns:
        Func. A first-class Python function that performs the actions of the Skit function provided
    """
    global LINE_OFFSET
    global COL_OFFSET
    global FUNC_STR
    LINE_OFFSET = line_offset
    COL_OFFSET = col_offset
    FUNC_STR = func_str

    func_ast = ast.fix_missing_locations(parse_string(func_str, debug=debug))

    exec(compile(func_ast, filename='<ast>', mode='exec'))
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
