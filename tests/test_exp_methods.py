import unittest
import re
import sys
from pprint import pprint
from apg_py.lib import identifiers as id
from apg_py.lib import utilities as utils
from apg_py.exp.exp import ApgExp

delim_pattern = '''pattern = owsp ("," / ";") owsp\n
owsp = *%d32\n'''
empty_pattern = '''pattern = ""\n'''
mixed_pattern = '''pattern = ("y" / "")\n'''
entire_pattern = '''pattern = %s"The entire string."\n'''
fname = 'tests/temp.out'


class TestExpSplit(unittest.TestCase):
    """Test tracing with exec()."""

    def test_split_1(self):
        '''Empty input.'''
        apgexp = ApgExp(delim_pattern)
        result = apgexp.split('')
        self.assertTrue(len(result) == 1)
        self.assertTrue(result[0] == '')
        apgexp = ApgExp(delim_pattern, 'c')
        result = apgexp.split(())
        self.assertTrue(len(result) == 1)
        self.assertTrue(result[0] == ())

    def test_split_1_1(self):
        '''Matches entire string.'''
        apgexp = ApgExp(entire_pattern)
        result = apgexp.split('The entire string.')
        self.assertTrue(len(result) == 1)
        self.assertTrue(result[0] == '')
        apgexp = ApgExp(entire_pattern, 'c')
        result = apgexp.split(utils.string_to_tuple('The entire string.'))
        self.assertTrue(len(result) == 1)
        self.assertTrue(result[0] == ())

    def test_split_2(self):
        '''Empty pattern.'''
        apgexp = ApgExp(empty_pattern)
        result = apgexp.split('abc')
        self.assertTrue(len(result) == 3)
        self.assertTrue(result[0] == 'a')
        self.assertTrue(result[1] == 'b')
        self.assertTrue(result[2] == 'c')
        apgexp = ApgExp(empty_pattern, 'c')
        result = apgexp.split(utils.string_to_tuple('abc'))
        self.assertTrue(len(result) == 3)
        self.assertTrue(result[0][0] == 97)
        self.assertTrue(result[1][0] == 98)
        self.assertTrue(result[2][0] == 99)

    def test_split_3(self):
        '''No match.'''
        pattern = 'pattern = %d33\n'
        apgexp = ApgExp(pattern)
        result = apgexp.split('abc')
        self.assertTrue(len(result) == 1)
        self.assertTrue(result[0] == 'abc')
        apgexp = ApgExp(pattern, 'c')
        result = apgexp.split(utils.string_to_tuple('abc'))
        self.assertTrue(len(result) == 1)
        self.assertTrue(result[0][0] == 97)
        self.assertTrue(result[0][1] == 98)
        self.assertTrue(result[0][2] == 99)

    def test_split_4(self):
        '''Multiple matches.'''
        input = 'a,b  ,  c;  d'
        apgexp = ApgExp(delim_pattern)
        result = apgexp.split(input)
        self.assertTrue(len(result) == 4)
        self.assertTrue(result[0] == 'a')
        self.assertTrue(result[1] == 'b')
        self.assertTrue(result[2] == 'c')
        self.assertTrue(result[3] == 'd')
        apgexp = ApgExp(delim_pattern, 'c')
        result = apgexp.split(utils.string_to_tuple(input))
        self.assertTrue(len(result) == 4)
        self.assertTrue(result[0][0] == 97)
        self.assertTrue(result[1][0] == 98)
        self.assertTrue(result[2][0] == 99)
        self.assertTrue(result[3][0] == 100)

    def test_split_5(self):
        '''Multiple matches - leading delimiters.'''
        input = ',,a,b  ,  c;  d'
        apgexp = ApgExp(delim_pattern)
        result = apgexp.split(input)
        self.assertTrue(len(result) == 4)
        self.assertTrue(result[0] == 'a')
        self.assertTrue(result[1] == 'b')
        self.assertTrue(result[2] == 'c')
        self.assertTrue(result[3] == 'd')
        apgexp = ApgExp(delim_pattern, 'c')
        result = apgexp.split(utils.string_to_tuple(input))
        self.assertTrue(len(result) == 4)
        self.assertTrue(result[0][0] == 97)
        self.assertTrue(result[1][0] == 98)
        self.assertTrue(result[2][0] == 99)
        self.assertTrue(result[3][0] == 100)

    def test_split_6(self):
        '''Multiple matches - trailing delimiters.'''
        input = ',,a,b  ,  c;  d;; ;'
        apgexp = ApgExp(delim_pattern)
        result = apgexp.split(input)
        self.assertTrue(len(result) == 4)
        self.assertTrue(result[0] == 'a')
        self.assertTrue(result[1] == 'b')
        self.assertTrue(result[2] == 'c')
        self.assertTrue(result[3] == 'd')
        apgexp = ApgExp(delim_pattern, 'c')
        result = apgexp.split(utils.string_to_tuple(input))
        self.assertTrue(len(result) == 4)
        self.assertTrue(result[0][0] == 97)
        self.assertTrue(result[1][0] == 98)
        self.assertTrue(result[2][0] == 99)
        self.assertTrue(result[3][0] == 100)

    def test_split_7(self):
        '''Mixed empty string & delimiter.'''
        input = 'abycyyd'
        apgexp = ApgExp(mixed_pattern)
        result = apgexp.split(input)
        self.assertTrue(len(result) == 4)
        self.assertTrue(result[0] == 'a')
        self.assertTrue(result[1] == 'b')
        self.assertTrue(result[2] == 'c')
        self.assertTrue(result[3] == 'd')
        apgexp = ApgExp(mixed_pattern, 'c')
        result = apgexp.split(utils.string_to_tuple(input))
        self.assertTrue(len(result) == 4)
        self.assertTrue(result[0][0] == 97)
        self.assertTrue(result[1][0] == 98)
        self.assertTrue(result[2][0] == 99)
        self.assertTrue(result[3][0] == 100)

    def test_split_8(self):
        '''Limited matches.'''
        input = 'a,b,c,d'
        apgexp = ApgExp(delim_pattern)
        result = apgexp.split(input, limit=1)
        self.assertTrue(len(result) == 1)
        self.assertTrue(result[0] == 'a')
        result = apgexp.split(input, limit=2)
        self.assertTrue(len(result) == 2)
        self.assertTrue(result[1] == 'b')
        result = apgexp.split(input, limit=3)
        self.assertTrue(len(result) == 3)
        self.assertTrue(result[2] == 'c')
        result = apgexp.split(input, limit=4)
        self.assertTrue(len(result) == 4)
        self.assertTrue(result[3] == 'd')
        apgexp = ApgExp(delim_pattern, 'c')
        result = apgexp.split(utils.string_to_tuple(input), limit=1)
        self.assertTrue(len(result) == 1)
        self.assertTrue(result[0][0] == 97)
        result = apgexp.split(utils.string_to_tuple(input), limit=2)
        self.assertTrue(len(result) == 2)
        self.assertTrue(result[1][0] == 98)
        result = apgexp.split(utils.string_to_tuple(input), limit=3)
        self.assertTrue(len(result) == 3)
        self.assertTrue(result[2][0] == 99)
        result = apgexp.split(utils.string_to_tuple(input), limit=4)
        self.assertTrue(len(result) == 4)
        self.assertTrue(result[3][0] == 100)


pattern = '''start = A / B\n
A = 1*"a"\n
B = 1*"b"\n
'''


def start_cb(state, input, index, length, data):
    if(state == id.SEM_POST):
        data.append({'start': input[index:index + length]})


def a_cb(state, input, index, length, data):
    if(state == id.SEM_POST):
        data.append({'A': input[index:index + length]})


def b_cb(state, input, index, length, data):
    if(state == id.SEM_POST):
        data.append({'B': input[index:index + length]})


class TestExpAst(unittest.TestCase):
    """Test working with the AST."""

    def test_ast_1(self):
        '''Callbacks - string input.'''
        test_string = 'aaabbbcccAAACCC'
        apgexp = ApgExp(pattern, 'g')
        apgexp.include()
        result = apgexp.exec(test_string)
        self.assertTrue(result is not None)
        self.assertTrue(result.ast is not None)
        result.ast.add_callback('start', start_cb)
        result.ast.add_callback('A', a_cb)
        result.ast.add_callback('B', b_cb)
        data = []
        result.ast.translate(data)
        # print()
        # pprint(data)
        self.assertTrue('aaa' == utils.tuple_to_string(data[0]['A']))
        self.assertTrue('aaa' == utils.tuple_to_string(data[1]['start']))
        result = apgexp.exec(test_string)
        result.ast.add_callback('start', start_cb)
        result.ast.add_callback('A', a_cb)
        result.ast.add_callback('B', b_cb)
        data = []
        result.ast.translate(data)
        self.assertTrue('bbb' == utils.tuple_to_string(data[0]['B']))
        self.assertTrue('bbb' == utils.tuple_to_string(data[1]['start']))
        result = apgexp.exec(test_string)
        result.ast.add_callback('start', start_cb)
        result.ast.add_callback('A', a_cb)
        result.ast.add_callback('B', b_cb)
        data = []
        result.ast.translate(data)
        self.assertTrue('AAA' == utils.tuple_to_string(data[0]['A']))
        self.assertTrue('AAA' == utils.tuple_to_string(data[1]['start']))

    def test_ast_2(self):
        '''Callbacks - character code input.'''
        test_string = 'aaabbbcccAAACCC'
        test_tuple = utils.string_to_tuple(test_string)
        apgexp = ApgExp(pattern, 'gc')
        apgexp.include()
        result = apgexp.exec(test_tuple)
        self.assertTrue(result is not None)
        self.assertTrue(result.ast is not None)
        result.ast.add_callback('start', start_cb)
        result.ast.add_callback('A', a_cb)
        result.ast.add_callback('B', b_cb)
        data = []
        result.ast.translate(data)
        self.assertTrue('aaa' == utils.tuple_to_string(data[0]['A']))
        self.assertTrue('aaa' == utils.tuple_to_string(data[1]['start']))

    def test_ast_3(self):
        '''No AST.'''
        test_string = 'aaabbbcccAAACCC'
        test_tuple = utils.string_to_tuple(test_string)
        apgexp = ApgExp(pattern, 'gc')
        result = apgexp.exec(test_tuple)
        self.assertTrue(result is not None)
        self.assertTrue(result.ast is None)


def fn_string(input, result):
    if(len(result.rules['A'.lower()])):
        return 'xxx'
    return 'yyy'


def fn_bad_string(input, result):
    return (1, 1, 1)


def fn_bad_tuple(input, result):
    return 'xxx'


def fn_tuple(input, result):
    if(len(result.rules['A'.lower()])):
        return (120, 120, 120)
    return (121, 121, 121)


class TestExpReplace(unittest.TestCase):
    """Test the replacement function."""

    def test_replace_1(self):
        '''Simple replacement string - single match.'''
        test_string = 'aaabbbcccCCCBBBAAA'
        apgexp = ApgExp(pattern)
        string = apgexp.replace(test_string, '<->')
        self.assertTrue(string == '<->bbbcccCCCBBBAAA')

    def test_replace_2(self):
        '''Simple replacement string - all matches.'''
        test_string = 'aaabbbcccCCCBBBAAA'
        apgexp = ApgExp(pattern, 'g')
        string = apgexp.replace(test_string, '<->')
        self.assertTrue(string == '<-><->cccCCC<-><->')

    def test_replace_3(self):
        '''Special character replacement string - $$.'''
        test_string = 'aaabbbcccCCCBBBAAA'
        apgexp = ApgExp(pattern, 'g')
        string = apgexp.replace(test_string, '<$$>')
        self.assertTrue(string == '<$><$>cccCCC<$><$>')

    def test_replace_4(self):
        '''Special character replacement string - $`.'''
        test_string = 'aaabbbcccCCCBBBAAA'
        apgexp = ApgExp(pattern, 'g')
        string = apgexp.replace(test_string, '<$`>')
        self.assertTrue(
            string == '<><aaa>cccCCC<aaabbbcccCCC><aaabbbcccCCCBBB>')

    def test_replace_5(self):
        '''Special character replacement string - $&.'''
        test_string = 'aaabbbcccCCCBBBAAA'
        apgexp = ApgExp(pattern, 'g')
        string = apgexp.replace(test_string, '<$&>')
        self.assertTrue(
            string == '<aaa><bbb>cccCCC<BBB><AAA>')

    def test_replace_6(self):
        '''Special character replacement string - $'.'''
        test_string = 'aaabbbcccCCCBBBAAA'
        apgexp = ApgExp(pattern, 'g')
        string = apgexp.replace(test_string, '<$\'>')
        self.assertTrue(
            string == '<bbbcccCCCBBBAAA><cccCCCBBBAAA>cccCCC<AAA><>')

    def test_replace_7(self):
        '''Special character replacement string - ${A}.'''
        test_string = 'aaabbbcccCCCBBBAAA'
        apgexp = ApgExp(pattern, 'g')
        apgexp.include()
        string = apgexp.replace(test_string, '<${A}>')
        self.assertTrue(
            string == '<aaa><>cccCCC<><AAA>')
        string = apgexp.replace(test_string, '<${a}>')
        self.assertTrue(
            string == '<aaa><>cccCCC<><AAA>')

    def test_replace_8(self):
        '''Special character replacement string - ${B}.'''
        test_string = 'aaabbbcccCCCBBBAAA'
        apgexp = ApgExp(pattern, 'g')
        apgexp.include()
        string = apgexp.replace(test_string, '<${B}>')
        self.assertTrue(
            string == '<><bbb>cccCCC<BBB><>')
        string = apgexp.replace(test_string, '<${b}>')
        # print()
        # print(string)
        self.assertTrue(
            string == '<><bbb>cccCCC<BBB><>')

    def test_replace_9(self):
        '''Tuple replacement.'''
        test_string = 'aaabbbcccCCCBBBAAA'
        test_tuple = utils.string_to_tuple(test_string)
        apgexp = ApgExp(pattern, 'gc')
        apgexp.include()
        string = apgexp.replace(test_tuple, (0, 1, 0))
        self.assertTrue(
            string == (0, 1, 0, 0, 1, 0, 99, 99, 99,
                       67, 67, 67, 0, 1, 0, 0, 1, 0,))

    def test_replace_10(self):
        '''String function replacement.'''
        test_string = 'aaabbbcccCCCBBBAAA'
        apgexp = ApgExp(pattern, 'g')
        apgexp.include()
        string = apgexp.replace(test_string, fn_string)
        self.assertTrue(string == 'xxxyyycccCCCyyyxxx')
        with self.assertRaises(Exception) as context:
            string = apgexp.replace(test_string, fn_bad_string)
        self.assertTrue('must return a string' in str(context.exception))

    def test_replace_11(self):
        '''Tuple function replacement.'''
        test_string = 'aaabbbcccCCCBBBAAA'
        test_tuple = utils.string_to_tuple(test_string)
        apgexp = ApgExp(pattern, 'gc')
        apgexp.include()
        string = apgexp.replace(test_tuple, fn_tuple)
        self.assertTrue(
            string == (
                120,
                120,
                120,
                121,
                121,
                121,
                99,
                99,
                99,
                67,
                67,
                67,
                121,
                121,
                121,
                120,
                120,
                120))
        with self.assertRaises(Exception) as context:
            string = apgexp.replace(test_tuple, fn_bad_tuple)
        # print()
        # print(context.exception)
        self.assertTrue(
            'must return a tuple of integers' in str(
                context.exception))
