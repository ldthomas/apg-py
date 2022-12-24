import unittest
import re
from apg_py.lib import identifiers as id
from apg_py.lib import utilities as utils
from apg_py.exp.exp import ApgExp


class TestExpExec(unittest.TestCase):
    """Testing matching (exec() function) of simple
    expressions with no rules."""

    def test_exp_flags_1(self):
        '''Test flags.'''
        pattern = 'start = "abc"\n'
        exp = ApgExp(pattern, 'yyggtc')
        self.assertTrue(exp.flags == 'cgt')
        exp = ApgExp(pattern, 'yyggtcy')
        self.assertTrue(exp.flags == 'cty')
        exp = ApgExp(pattern, 'y')
        self.assertTrue(exp.flags == 'y')
        exp = ApgExp(pattern, 'g')
        self.assertTrue(exp.flags == 'g')

    def test_exp_simple_1(self):
        '''Test default - no flags.'''
        pattern = 'start = "abc"\n'
        input = '---ABC==='
        exp = ApgExp(pattern)
        result = exp.exec(input)
        self.assertTrue(result is not None)
        self.assertTrue(result.match == 'ABC')
        self.assertTrue(result.index == 3)
        self.assertTrue(result.indices == [3, 6])
        self.assertTrue(result.left_context == '---')
        self.assertTrue(result.right_context == '===')

    def test_exp_character_codes_1(self):
        '''Test character codes.'''
        pattern = 'start = "abc"\n'
        input = utils.string_to_tuple('---ABC===')
        exp = ApgExp(pattern, 'c')
        result = exp.exec(input)
        self.assertTrue(result is not None)
        self.assertTrue(result.match[0] == 65)
        self.assertTrue(result.index == 3)
        self.assertTrue(result.indices == [3, 6])
        self.assertTrue(result.left_context[0] == 45)
        self.assertTrue(result.right_context[0] == 61)

    def test_exp_global_1(self):
        '''Test global flag.'''
        pattern = 'start = "abc"\n'
        input = '---ABC===abc~~~'
        exp = ApgExp(pattern, 'g')
        result = exp.exec(input)
        self.assertTrue(result is not None)
        self.assertTrue(result.match == 'ABC')
        self.assertTrue(result.index == 3)
        result = exp.exec(input)
        self.assertTrue(result.match == 'abc')
        self.assertTrue(result.index == 9)
        self.assertTrue(result.right_context == '~~~')
        result = exp.exec(input)
        self.assertTrue(result is None)
        self.assertTrue(exp.last_index == 0)

    def test_exp_sticky_1(self):
        '''Test sticky flag.'''
        pattern = 'start = "abc"\n'
        input = '---ABCabc~~~'
        exp = ApgExp(pattern, 'g')
        exp.last_index = 3
        result = exp.exec(input)
        self.assertTrue(result.match == 'ABC')
        self.assertTrue(result.index == 3)
        result = exp.exec(input)
        self.assertTrue(result.match == 'abc')
        self.assertTrue(result.index == 6)
        self.assertTrue(result.right_context == '~~~')
        result = exp.exec(input)
        self.assertTrue(result is None)
        self.assertTrue(exp.last_index == 0)


class TestExpTest(unittest.TestCase):
    """Testing (test() function) of simple expressions with no rules."""

    def test_test_simple_1(self):
        '''Test test() default - no flags.'''
        pattern = 'start = "abc"\n'
        input = '---ABC==='
        exp = ApgExp(pattern)
        result = exp.test(input)
        self.assertTrue(result)
        self.assertTrue(exp.last_index == 0)

    def test_test_character_codes_1(self):
        '''Test test() with character codes.'''
        pattern = 'start = "abc"\n'
        input = utils.string_to_tuple('---ABC===')
        exp = ApgExp(pattern, 'c')
        result = exp.test(input)
        self.assertTrue(result)
        self.assertTrue(exp.last_index == 0)

    def test_test_global_1(self):
        '''Test test() with global flag.'''
        pattern = 'start = "abc"\n'
        input = '---ABC===abc~~~'
        exp = ApgExp(pattern, 'g')
        result = exp.test(input)
        self.assertTrue(result)
        self.assertTrue(exp.last_index == 6)
        result = exp.test(input)
        self.assertTrue(result)
        self.assertTrue(exp.last_index == 12)
        result = exp.test(input)
        self.assertFalse(result)
        self.assertTrue(exp.last_index == 0)

    def test_test_sticky_1(self):
        '''Test test() with sticky flag.'''
        pattern = 'start = "abc"\n'
        input = '---ABCabc~~~'
        exp = ApgExp(pattern, 'g')
        exp.last_index = 3
        result = exp.test(input)
        self.assertTrue(result)
        self.assertTrue(exp.last_index == 6)
        result = exp.test(input)
        self.assertTrue(result)
        self.assertTrue(exp.last_index == 9)
        result = exp.test(input)
        self.assertFalse(result)
        self.assertTrue(exp.last_index == 0)


class TestExpExceptions(unittest.TestCase):
    """Testing errors raising exceptions."""

    def test_exception_1(self):
        '''Test bad flags.'''
        pattern = 'start = "abc"\n'
        input = '---ABC==='
        with self.assertRaises(Exception) as context:
            exp = ApgExp(pattern, 'x')
        # print()
        # print(context.exception)
        found = re.search('flag x not recognized', str(context.exception))
        self.assertTrue(found)

    def test_exception_2(self):
        '''Test bad pattern syntax.'''
        pattern = 'start = "abc\n'
        input = '---ABC==='
        with self.assertRaises(Exception) as context:
            exp = ApgExp(pattern)
        # print()
        # print(context.exception)
        found = re.search('Pattern syntax error:', str(context.exception))
        self.assertTrue(found)
        found = re.search(
            'expected literal string closure', str(
                context.exception))
        self.assertTrue(found)

    def test_exception_3(self):
        '''exec() bad string input.'''
        pattern = 'start = "abc"\n'
        input = '---ABC==='
        with self.assertRaises(Exception) as context:
            exp = ApgExp(pattern, 'c')
            result = exp.exec(input)
        found = re.search(
            'input must be a tuple', str(
                context.exception))
        self.assertTrue(found)

    def test_exception_4(self):
        '''exec() bad character codes input.'''
        pattern = 'start = "abc"\n'
        input = '---ABC==='
        with self.assertRaises(Exception) as context:
            exp = ApgExp(pattern)
            result = exp.exec(utils.string_to_tuple(input))
        found = re.search(
            'input must be a string', str(
                context.exception))
        self.assertTrue(found)

    def test_exception_5(self):
        '''test() bad character codes input.'''
        pattern = 'start = "abc"\n'
        input = '---ABC==='
        with self.assertRaises(Exception) as context:
            exp = ApgExp(pattern, 'c')
            result = exp.test(input)
        found = re.search(
            'input must be a tuple', str(
                context.exception))
        self.assertTrue(found)

    def test_exception_6(self):
        '''test() bad string input.'''
        pattern = 'start = "abc"\n'
        input = '---ABC==='
        with self.assertRaises(Exception) as context:
            exp = ApgExp(pattern)
            result = exp.test(utils.string_to_tuple(input))
        # print()
        # print(context.exception)
        found = re.search(
            'input must be a string', str(
                context.exception))
        self.assertTrue(found)


if __name__ == '__main__':
    unittest.main()
