import unittest
import ast

#TODO fix relative import
from ..parser import parse_string, parse_function
from ..oracle import ORACLE

class ParsingASTTests(unittest.TestCase):
    def assertSameParse(self, python, skit):
        self.assertEqual(
            ast.dump(ast.parse(python)),
            ast.dump(parse_string(skit, testing=True))
        )

    def test_id(self):
        self.assertSameParse("test", "test")

    def test_num(self):
        self.assertSameParse("1", "1")

    def test_group(self):
        self.assertSameParse("(1 + 2)", "(1 + 2)")

    def test_string_single_quotes(self):
        self.assertSameParse("'test'", "'test'")

    def test_string_double_quotes(self):
        self.assertSameParse('"test"', '"test"')

    def test_stmt_assignment(self):
        self.assertSameParse("test = 1", "test = 1")

    def test_multi_stmt_assignment(self):
        self.assertSameParse("a, b = tpl", "a, b = tpl")

    def test_stmt_aug_assign_add(self):
        self.assertSameParse("test += 1", "test += 1")

    def test_stmt_aug_assign_sub(self):
        self.assertSameParse("test -= 1", "test -= 1")

    def test_stmt_aug_assign_mult(self):
        self.assertSameParse("test *= 1", "test *= 1")

    def test_stmt_aug_assign_div(self):
        self.assertSameParse("test /= 1", "test /= 1")

    def test_stmt_return(self):
        self.assertSameParse("return", "return")

    def test_stmt_return_value(self):
        self.assertSameParse("return 1", "return 1")

    def test_stmt_print(self):
        self.assertSameParse("print 1", "print 1")

    def test_func(self):
        self.assertSameParse("def test(): pass",
                             "func test() { }")

    def test_func_param(self):
        self.assertSameParse("def test(one): pass",
                             "func test(one) { }")

    def test_func_default_param(self):
        self.assertSameParse("def test(one=1): pass",
                             "func test(one=1) { }")

    def test_func_body(self):
        self.assertSameParse("def test(): return",
                             "func test() { return }")

    def test_lambda(self):
        self.assertSameParse("lambda x: x",
                             "@(x) x")

    def test_funccall(self):
        self.assertSameParse("test()", "test()")

    def test_funccall_param(self):
        self.assertSameParse("test(1)", "test(1)")

    def test_funccall_params(self):
        self.assertSameParse("test(1,2)", "test(1,2)")

    def test_funccall_keyword_param(self):
        self.assertSameParse("test(one=1)", "test(one=1)")

    def test_funccall_keyword_params(self):
        self.assertSameParse("test(one=1,two=2)", "test(one=1,two=2)")

    def test_cond_eq(self):
        self.assertSameParse("1 == 1", "1 == 1")

    def test_cond_neq(self):
        self.assertSameParse("1 != 2", "1 != 2")

    def test_cond_lte(self):
        self.assertSameParse("1 <= 2", "1 <= 2")

    def test_cond_gte(self):
        self.assertSameParse("2 >= 1", "2 >= 1")

    def test_cond_lt(self):
        self.assertSameParse("1 < 2", "1 < 2")

    def test_cond_gt(self):
        self.assertSameParse("2 > 1", "2 > 1")

    def test_true(self):
        self.assertSameParse("True", "True")

    def test_false(self):
        self.assertSameParse("False", "False")

    def test_and(self):
        self.assertSameParse("True and False", "True and False")

    def test_and_chain(self):
        self.assertSameParse("True and False and True", "True and False and True")

    def test_or(self):
        self.assertSameParse("True or False", "True or False")

    def test_or_chain(self):
        self.assertSameParse("True or False or True", "True or False or True")

    def test_and_or(self):
        self.assertSameParse("True and False or True", "True and False or True")

    def test_or_and(self):
        self.assertSameParse("True or False and True", "True or False and True")

    def test_and_or_chain(self):
        self.assertSameParse("True and False or True or False", "True and False or True or False")

    def test_or_and_chain(self):
        self.assertSameParse("True or False and True and False", "True or False and True and False")

    def test_or_and_or_chain(self):
        self.assertSameParse("True or False and True or False", "True or False and True or False")

    def test_and_or_and_chain(self):
        self.assertSameParse("True and False or True and False", "True and False or True and False")

    def test_and_compop(self):
        self.assertSameParse("1 >= 2 and 3 <= 4", "1 >= 2 and 3 <= 4")

    def test_or_compop(self):
        self.assertSameParse("1 >= 2 or 3 <= 4", "1 >= 2 or 3 <= 4")

    def test_not(self):
        self.assertSameParse("not False", "not False")

    def test_if(self):
        self.assertSameParse("if 1: pass",
                             "if 1 { }")

    def test_if_cond(self):
        self.assertSameParse("if 1 == 1: pass",
                             "if 1 == 1 { }")

    def test_if_body(self):
        self.assertSameParse("if 1: print 1",
                             "if 1 { print 1 }")

    def test_if_else(self):
        self.assertSameParse("if 1:\n  pass\nelse:\n  pass",
                             "if 1 { } else { }")

    def test_if_else_body(self):
        self.assertSameParse("if 1:\n  print 1\nelse:\n  print False",
                             "if 1 { print 1 } else { print False }")

    def test_if_elseif(self):
        self.assertSameParse("if 1:\n  pass\nelif 2:\n  pass",
                             "if 1 { } else 2 { }")

    def test_if_elseif_chain(self):
        self.assertSameParse("if 1:\n  pass\nelif 2:\n  pass\nelif 3:\n  pass",
                             "if 1 { } else 2 { } else 3 { }")

    def test_if_elseif_else(self):
        self.assertSameParse("if 1:\n  pass\nelif 2:\n  pass\nelse:\n  pass",
                             "if 1 { } else 2 { } else { }")

    def test_if_elseif_chain_else(self):
        self.assertSameParse("if 1:\n  pass\nelif 2:\n  pass\nelif 3:\n  pass\nelse:\n  pass",
                             "if 1 { } else 2 { } else 3 { } else { }")

    #TODO Add ternary operator
    #def test_ternary(self):
    #    self.assertSameParse("1 if True else 2",
    #                         "True ? 1 : 2")

    def test_while(self):
        self.assertSameParse("while 1: pass",
                             "while 1 { }")

    def test_while_body(self):
        self.assertSameParse("while 1: print 1",
                             "while 1 { print 1 }")

    def test_for(self):
        self.assertSameParse("for i in range(1,2): pass",
                             "for i := range(1,2) {}")

    def test_for_body(self):
        self.assertSameParse("for i in range(1,2): print i",
                             "for i := range(1,2) { print i }")

    def test_list_decl(self):
        self.assertSameParse("[1,2,3]", "[1,2,3]")

    def test_property(self):
        self.assertSameParse("test.test", "test.test")

    def test_getitem(self):
        self.assertSameParse("test[test]", "test[test]")

    def test_binop_plus(self):
        self.assertSameParse("1 + 1", "1 + 1")

    def test_binop_minus(self):
        self.assertSameParse("1 - 1", "1 - 1")

    def test_binop_times(self):
        self.assertSameParse("1 * 1", "1 * 1")

    def test_binop_div(self):
        self.assertSameParse("1 / 1", "1 / 1")

    def test_uminus(self):
        self.assertSameParse("-1", "-1")

class ParsingBehaviorTests(unittest.TestCase):
    def assertSameParse(self, skit1, skit2):
        self.assertEqual(
            ast.dump(parse_string(skit1)),
            ast.dump(parse_string(skit2))
        )

    def compileFunc(self, func):
        return parse_function(func)

    def assertResult(self, func, result, eq=True):
        if eq:
            self.assertEqual(result, func({}))
        else:
            self.assertNotEqual(result, func({}))

    def test_group_same_as_regular(self):
        self.assertSameParse("1 + 2", "(1 + 2)")

    def test_single_double_qoutes(self):
        self.assertSameParse("'test'", '"test"')

    def test_range(self):
        self.assertSameParse("range(1,2)", "1 to 2")

    def test_top_func(self):
        test = []
        ORACLE.set('test', test)

        func = self.compileFunc("func(test) { return test }")
        test.append(1)

        self.assertResult(func, test)

        test.pop()
        self.assertResult(func, test)

        test = [1,2,3]
        self.assertResult(func, test, eq=False)

        ORACLE.set('test', test)
        self.assertResult(func, test)