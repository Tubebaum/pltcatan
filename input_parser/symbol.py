class Symbol(object):
	def __init__(self, name="", tpe="", value=None):
		self.name = name
		self.tpe = tpe
		self.value = value

class SymbolTable(object):
	def __init__(self):
		self.table = {}

	def add_symbol(self, name, tpe, value):
		self.table[name] = Symbol(name, tpe, value)

	def get_symbol(self, name):
		return self.table[name]

symbol_table = SymbolTable()