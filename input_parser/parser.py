import ply.lex as lex
import ply.yacc as yacc

from symbol import symbol_table

# Token declarations

tokens = ('NAME', 'NUMBER', 'VAR')
literals = ['=', '+', '-', '*', '/', '(', ')']

t_VAR = r'var'

t_NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'

def t_NUMBER(t):
	r'\d+'
	try:
		t.value = int(t.value)
	except ValueError:
		print "Integer value too large", t.value
		t.value = 0
	return t

t_ignore = " \t"

def t_newline(t):
	r'\n+'

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

#def p_funcdef(p):
#	"""funcdef : 'func' '(' parameters ')' ':' funcbody"""

#def p_body(p):
#	"""body : simple_stmt | NEWLINE INDENT stmtlst DEDENT"""

#def p_stmtlst(p):
#	"""stmtlst : stmtlst stmt NEWLINE
#			   | stmt NEWLINE"""

def p_stmt_assignment(p):
	"""stmt : NAME '=' expr"""
	symbol_table.add_symbol(p[1], "num", p[3])

def p_stmt_expr(p):
	"""stmt : expr"""
	print p[1]

def p_expr_binop(p):
	"""expr : expr '+' expr
			| expr '-' expr
			| expr '*' expr
			| expr '/' expr"""
	if   p[2] == '+': p[0] = p[1] + p[3]
	elif p[2] == '-': p[0] = p[1] - p[3]
	elif p[2] == '*': p[0] = p[1] * p[3]
	elif p[2] == '/': p[0] = p[1] / p[3]

def p_expr_uminus(p):
	"""expr : '-' expr %prec UMINUS"""
	p[0] = -p[2]

def p_expr_group(p):
	"""expr : '(' expr ')'"""
	p[0] = p[2]

def p_expr_number(p):
	"""expr : NUMBER"""
	p[0] = p[1]

def p_expr_name(p):
	"""expr : NAME"""
	try:
		p[0] = symbol_table.get_symbol(p[1]).value
	except LookupError:
		print "Undefined name '%s'" % p[1]
		p[0] = 0

def p_error(p):
	print "Syntax error at '%s'" % p.value

yacc.yacc()

while 1:
	try:
		s = raw_input('>')
	except EOFError:
		break
	if not s: continue
	yacc.parse(s)
