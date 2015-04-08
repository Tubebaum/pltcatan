from collections import defaultdict


def get_registry():
    registry = defaultdict(list)
    def register(nonterminal):
        def registrar(func):
            registry[nonterminal] += [func]
            return func
        return registrar
    register.get = lambda x: registry[x]
    return register


def trivial(name, nonterminals, indent=4, suffix='', docstring=None):
    def template(p):
        p[0] = p[1]

    if not docstring:
        docstring = "{} : {}".format(name, nonterminals[0])
        padding = ' ' * (len(name) + 1 + indent) + '| '

        if len(nonterminals) > 1:
            docstring += '\n' + padding + ('\n' + padding).join(nonterminals[1:])

    template.__doc__ = docstring
    
    template.__name__ = template.func_name = 'p_' + name + suffix

    return template


def trivial_from_registry(name, registry, indent=4, suffix=''):
    return trivial(name, [func.__doc__.split(':')[0].strip() for func in registry.get(name)], indent=indent, suffix=suffix)