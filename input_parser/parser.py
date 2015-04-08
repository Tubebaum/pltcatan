import ast

import ply.lex as lex
import ply.yacc as yacc

from symbol import symbol_table

# Token declarations

reserved = {
	'func': 'FUNC_DECL',
	'return': 'RETURN'
}
tokens = ['NAME', 'NUMBER', 'NEWLINE'] + list(reserved.values())
literals = ['=', '+', '-', '*', '/', '(', ')', '{', '}']

def t_NAME(t):
	r'[a-zA-Z_][a-zA-Z0-9_]*'
	t.type = reserved.get(t.value, 'NAME') # Check for reserved words
	return t

def t_NUMBER(t):
	r'\d+'
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

def p_stmt_assignment(p):
	"""stmt : NAME '=' expr"""
	p[0] = ast.Assign([ast.Name(p[1], ast.Store())], p[3])

def p_stmt_return(p):
	"""stmt : RETURN expr
		    | RETURN"""
	if len(p) > 2:
		p[0] = ast.Return(p[2])
	else:
		p[0] = ast.Return()

def p_stmt_expr(p):
	"""stmt : expr"""
	p[0] = ast.Expr(p[1])

def p_stmt_func(p):
	"""stmt : func"""
	p[0] = p[1]

def p_func(p):
	"""func : FUNC_DECL NAME '(' params ')' '{' body '}'"""
	args = ast.arguments(p[4], None, None, [])
	p[0] = ast.FunctionDef(p[2], args, p[7], [])

def p_params(p):
	"""params : param ',' params
			  | param"""
	p[0] = [p[1]]
	if len(p) > 2:
		p[0].extend(p[3])

def p_param(p):
	"""param : NAME
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
	p[0] = [p[1]]
	if len(p) > 2:
		p[0].extend(p[3])

def p_expr_funccall(p):
	"""expr : funccall"""
	p[0] = p[1]

def p_funccall(p):
	"""funccall : NAME '(' in_params ')'"""
	p[0] = ast.Call(ast.Name(p[1], ast.Load()), p[3], [], None, None)

def p_in_params(p):
	"""in_params : in_param ',' in_params
			     | in_param"""
	p[0] = [p[1]]
	if len(p) > 2:
		p[0].extend(p[3])

def p_in_param(p):
	"""in_param : expr
			    | empty"""
	p[0] = p[1]

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

def p_expr_group(p):
	"""expr : '(' expr ')'"""
	p[0] = p[2]

def p_expr_number(p):
	"""expr : NUMBER"""
	p[0] = ast.Num(p[1])

def p_expr_name(p):
	"""expr : NAME"""
	p[0] = ast.Name(p[1], ast.Load())

def p_error(p):
	print "Syntax error at '%s'" % p.value

def p_empty(p):
	"""empty :"""
	pass

yacc.yacc()

while 1:
	try:
		s = raw_input('>')
	except EOFError:
		break
	if not s: continue
	yacc.parse(s)
