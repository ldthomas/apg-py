import unittest
import re
from apg_py.lib import identifiers as id
from apg_py.lib import utilities as utils
from apg_py.lib.parser import Parser
from apg_py.lib.ast import Ast
from tests.grammars import ast_branch_fail
from tests.grammars import float_udt
from tests.grammars import float_bka_rnm
from tests.grammars import anbncn

# path = os.getcwd()
# print('\ntest_ast: cwd')
# print(path)
# print('\ntest_ast: sys.path')
# print(sys.path)
# print()


def udtSign(cbData):
    # matches '+', '-' or empty string
    cbData['phrase_length'] = 0
    cbData['state'] = id.EMPTY
    if(cbData['phrase_index'] < cbData['sub_end']):
        char = cbData['input'][cbData['phrase_index']]
        if(char == 43 or char == 45):
            cbData['phrase_length'] = 1
            cbData['state'] = id.MATCH


def udtInteger(cbData):
    # matches any string of digits 0-9
    index = cbData['phrase_index']
    length = 0
    while(index < cbData['sub_end']):
        char = cbData['input'][index]
        if(char >= 48 and char <= 57):
            length += 1
            index += 1
        else:
            break
    if(length > 0):
        cbData['state'] = id.MATCH
        cbData['phrase_length'] = length
    else:
        cbData['phrase_length'] = 0
        cbData['state'] = id.NOMATCH


def all(state, index, length, data):
    s = '    state: ' + id.dict.get(state) + '\n' \
        + '    phrase_index: ' + str(index) + '\n' \
        + '    phrase_length: ' + str(length) + '\n'
    data['string'] = data['string'] + s


def xCallback(state, input, index, length, data):
    data['string'] = data['string'] + 'X\n'
    all(state, index, length, data)
    return id.SEM_OK


def leftCallback(state, input, index, length, data):
    data['string'] = data['string'] + 'Left\n'
    all(state, index, length, data)
    return id.SEM_OK


def leftSkipCallback(state, input, index, length, data):
    data['string'] = data['string'] + 'Left(skip)\n'
    all(state, index, length, data)
    return id.SEM_SKIP


def rightCallback(state, input, index, length, data):
    data['string'] = data['string'] + 'Right\n'
    all(state, index, length, data)
    return id.SEM_OK


def startCallback(state, input, index, length, data):
    data['string'] = data['string'] + 'start\n'
    all(state, index, length, data)
    return id.SEM_OK


def alt1Callback(state, input, index, length, data):
    data['string'] = data['string'] + 'Alt1\n'
    all(state, index, length, data)


def alt2Callback(state, input, index, length, data):
    data['string'] = data['string'] + 'Alt2\n'
    all(state, index, length, data)


def esignCallback(state, input, index, length, data):
    data['string'] = data['string'] + 'e_sign\n'
    all(state, index, length, data)


def uintegerCallback(state, input, index, length, data):
    data['string'] = data['string'] + 'u_integer\n'
    all(state, index, length, data)


def digitsCallback(state, input, index, length, data):
    data['string'] = data['string'] + 'digits\n'
    all(state, index, length, data)


def aCallback(state, input, index, length, data):
    data['string'] = data['string'] + 'A\n'
    all(state, index, length, data)


def bCallback(state, input, index, length, data):
    data['string'] = data['string'] + 'B\n'
    all(state, index, length, data)


class TestAST(unittest.TestCase):
    """Test construction and translation of the AST."""

    def test_ast_1(self):
        '''Test the AST.'''
        input = 'xyzabcxyz'
        parser = Parser(ast_branch_fail)
        ast = Ast(parser)
        ast.add_callback('start', startCallback)
        ast.add_callback('x', xCallback)
        ast.add_callback('Alt1', alt1Callback)
        ast.add_callback('Alt2', alt2Callback)
        ast.add_callback('left', leftCallback)
        ast.add_callback('right', rightCallback)
        result = parser.parse(utils.string_to_tuple(input))
        self.assertTrue(result.success)
        data = {'string': ''}
        ast.translate(data)
        # print('\nAST translation')
        # print(data['string'])
        found = re.search('Left\n', data['string'])
        self.assertTrue(found, 'expected to find "Left"')
        found = re.search('Alt1\n', data['string'])
        self.assertTrue(found, 'expected to find "Alt1"')
        found = re.search('X\n', data['string'])
        self.assertTrue(found, 'expected to find "X"')

    def test_ast_2(self):
        '''Test skipping branches below the Left rule AST.'''
        input = 'xyzabcxyz'
        parser = Parser(ast_branch_fail)
        ast = Ast(parser)
        ast.add_callback('start', startCallback)
        ast.add_callback('x', xCallback)
        ast.add_callback('Alt1', alt1Callback)
        ast.add_callback('Alt2', alt2Callback)
        ast.add_callback('left', leftSkipCallback)
        ast.add_callback('right', rightCallback)
        result = parser.parse(utils.string_to_tuple(input))
        self.assertTrue(result.success)
        data = {'string': ''}
        ast.translate(data)
        # print('\nAST translation')
        # print(data['string'])
        found = re.search('Left\\(skip\\)\n', data['string'])
        self.assertTrue(found, 'expected to find "Left(skip)"')
        found = re.search('Alt1\n', data['string'])
        self.assertFalse(found, 'expected to find "Alt1"')
        found = re.search('X\n', data['string'])
        self.assertFalse(found, 'expected to find "X"')

    def test_ast_3(self):
        '''Test that failed parse tree branches are not on the AST.'''
        input = 'xyzxyz'
        parser = Parser(ast_branch_fail)
        ast = Ast(parser)
        ast.add_callback('start', startCallback)
        ast.add_callback('x', xCallback)
        ast.add_callback('Alt1', alt1Callback)
        ast.add_callback('Alt2', alt2Callback)
        ast.add_callback('left', leftCallback)
        ast.add_callback('right', rightCallback)
        result = parser.parse(utils.string_to_tuple(input))
        self.assertTrue(result.success)
        data = {'string': ''}
        ast.translate(data)
        # print('\nAST translation')
        # print(data['string'])
        found = re.search('Left\n', data['string'])
        self.assertTrue(found, 'expected to find "Left"')
        found = re.search('Alt2\n', data['string'])
        self.assertTrue(found, 'expected to find "Alt2"')
        found = re.search('X\n', data['string'])
        self.assertFalse(found, 'expected not to find "X"')

    def test_ast_4(self):
        '''Test UDTs on the AST.'''
        input = '+123.456E-10'
        parser = Parser(float_udt)
        parser.add_callbacks({'e_sign': udtSign})
        parser.add_callbacks({'u_integer': udtInteger})
        ast = Ast(parser)
        ast.add_callback('float', startCallback)
        ast.add_callback('e_sign', esignCallback)
        ast.add_callback('u_integer', uintegerCallback)
        result = parser.parse(utils.string_to_tuple(input))
        self.assertTrue(result.success)
        data = {'string': ''}
        ast.translate(data)
        # print('\nAST translation')
        # print(data['string'])
        found = re.search('e_sign\n', data['string'])
        self.assertTrue(found, 'expected to find "e_sign"')
        found = re.search('u_integer\n', data['string'])
        self.assertTrue(found, 'expected to find "u_integer"')

    def test_ast_5(self):
        '''Test rules in look ahead not on the AST.'''
        input = '123+123.456E-10'
        parser = Parser(float_bka_rnm)
        ast = Ast(parser)
        ast.add_callback('float', startCallback)
        ast.add_callback('digits', uintegerCallback)
        result = parser.parse(utils.string_to_tuple(input), sub_begin=3)
        self.assertTrue(result.success)
        data = {'string': ''}
        ast.translate(data)
        # print('\nAST translation')
        # print(data['string'])
        found = re.search('digits\n', data['string'])
        self.assertFalse(found, 'expected not to find "digits"')
        found = re.search('start\n', data['string'])
        self.assertTrue(found, 'expected to find "start"')

    def test_ast_5(self):
        '''Test rules in look behind not on the AST.'''
        input = '123+123.456E-10'
        parser = Parser(float_bka_rnm)
        ast = Ast(parser)
        ast.add_callback('float', startCallback)
        ast.add_callback('digits', uintegerCallback)
        result = parser.parse(utils.string_to_tuple(input), sub_begin=3)
        self.assertTrue(result.success)
        data = {'string': ''}
        ast.translate(data)
        # print('\nAST translation')
        # print(data['string'])
        found = re.search('digits\n', data['string'])
        self.assertFalse(found, 'expected not to find "digits"')
        found = re.search('start\n', data['string'])
        self.assertTrue(found, 'expected to find "start"')

    def test_ast_6(self):
        '''Test rules in look ahead not on the AST.'''
        input = 'aaabbbccc'
        parser = Parser(anbncn)
        ast = Ast(parser)
        ast.add_callback('S', startCallback)
        ast.add_callback('A', aCallback)
        ast.add_callback('B', bCallback)
        result = parser.parse(utils.string_to_tuple(input))
        self.assertTrue(result.success)
        data = {'string': ''}
        ast.translate(data)
        # print('\nAST translation')
        # print(data['string'])
        found = re.search('A\n', data['string'])
        self.assertFalse(found, 'expected not to find "A"')
        found = re.search('B\n', data['string'])
        self.assertTrue(found, 'expected to find "B"')


if __name__ == '__main__':
    unittest.main()
