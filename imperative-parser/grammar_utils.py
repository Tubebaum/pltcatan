from collections import defaultdict

def get_registry():
    """Produces a registration decorator that allows methods to be gathered under tags
    """
    registry = defaultdict(list)
    def register(nonterminal):
        def registrar(func):
            registry[nonterminal] += [func]
            return func
        return registrar
    register.get = lambda x: registry[x]
    return register

def gen_grammar(name, nonterminals, indent=4):
    """Generates a grammar docstring for the provided name and nonterminals

    Arguments:
        name -- the nonterminal name
        nonterminals -- a list of the nonterminals it's associated with

    Return:
        A docstring representing the grammar of the nonterminal
    """
    try:
        docstring = "{} : {}".format(name, nonterminals[0])
    except:
        print name, nonterminals
    padding = ' ' * (len(name) + 1 + indent) + '| '

    if len(nonterminals) > 1:
        docstring += '\n' + padding + ('\n' + padding).join(nonterminals[1:])

    return docstring


def trivial(name, nonterminals, indent=4, suffix=''):
    """Generates a method for a trivial terminal, where p[0] = p[1]

    Arguments:
        name -- a string representing the nonterminal name
        nonterminals -- a list of strings representing the nonterminals it's linked to

    Named Arguments:
        indent (4) -- an int representing the amount of indentation in the file
        suffix ('') -- a string representing a suffix that should be added to the name of the function

    Return:
        A function with the provided name and a generated grammar docstring
    """
    def template(p):
        p[0] = p[1]

    template.__doc__ = gen_grammar(name, nonterminals, indent)

    template.__name__ = template.func_name = 'p_' + name + suffix

    return template


def trivial_from_registry(name, registry, indent=4, suffix=''):
    """Generates a method for a trivial terminal, where p[0] = p[1], sourcing nonterminals from a registry

    Arguments:
        name -- a string representing the nonterminal name
        registry -- a registry generated by the get_registry() function

    Named Arguments:
        indent (4) -- an int representing the amount of indentation in the file
        suffix ('') -- a string representing a suffix that should be added to the name of the function

    Return:
        A function with the provided name and a generated grammar docstring
    """
    return trivial(name, [func.__doc__.split(':')[0].strip() for func in registry.get(name)], indent=indent, suffix=suffix)