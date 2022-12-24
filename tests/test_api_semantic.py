import unittest
import re
from apg_py.lib import utilities as utils
from apg_py.api.api import Api
from apg_py.lib.parser import Parser

fname = 'tests/temp.out'
api = Api()

start = 'start = one two / three four five\r\n'
line1 = 'one = "1"\n'
line2 = 'two = u_udt\r'
line3 = 'three = \\one \\%ru_udt\n'
line4 = 'four = %^ &one !two %$\n'
line5 = 'five = &&%d32 !!%d9 "abc"\n'
line6 = 'five = %d32 \\six\n'
line7 = 'five = %d32 \\u_notdefined\n'
line8 = 'five = %d32\nfour = %d32\n'
line9 = 'five = 2*1%d32\n'
line10 = 'five = 0%d32\n'
line11 = 'five = %d127-32\n'
line12 = 'five =/ %d32-127\nfive = %d32-127\n'


class TestApiSemantic(unittest.TestCase):
    """Test the semantic phase of the API generator."""

    def test_api_semantic_1(self):
        '''Test valid grammar, all operators.'''
        input = start + line1 + line2 + line3 + line4 + line5
        grammar = api.generate(input)
        self.assertFalse(api.errors)
        resultr = utils.pprint_to_string(grammar.rules, fname)
        self.assertTrue(resultr['error'] is None)
        resultu = utils.pprint_to_string(api.grammar.udts, fname)
        self.assertTrue(resultu['error'] is None)
        string = resultr['string'] + resultu['string']
        # print()
        # print(string)
        pattern = "'name': 'one'[\\s\\S]*'is_bkru': True[\\s\\S]*'type': 7,"
        pattern += " 'string': \\(49"
        found = re.search(pattern, string)
        self.assertTrue(found)
        found = re.search(
            "'name': 'two'[\\s\\S]*'type': 11, 'empty': False", string)
        self.assertTrue(found)
        found = re.search(
            "'name': 'u_udt'[\\s\\S]*'is_bkrr': True[\\s\\S]*'empty': False",
            string)
        self.assertTrue(found)
        pattern = "'name': 'four'[\\s\\S]*'type': 17[\\s\\S]*'type': "
        pattern += "12[\\s\\S]*'type': 13[\\s\\S]*'type': 18"
        found = re.search(pattern, string)
        self.assertTrue(found)
        found = re.search(
            "'name': 'five'[\\s\\S]*'type': 15[\\s\\S]*'type': 16",
            string)
        self.assertTrue(found)

    def test_api_semantic_2(self):
        '''Test invalid grammar- rnm-op refers to undefined rule.'''
        input = start + line1 + line2 + line3 + line4
        api.generate(input, phase='semantic')
        self.assertTrue(api.errors)
        string = api.display_errors()
        # print()
        # print(string)
        pattern = "rule name 'five' used but not defined"
        found = re.search(pattern, string)
        self.assertTrue(found)

    def test_api_semantic_3(self):
        '''Test invalid grammar- bkr-op refers to undefined rule.'''
        input = start + line1 + line2 + line3 + line4 + line6
        api.generate(input, phase='semantic')
        self.assertTrue(api.errors)
        string = api.display_errors()
        # print()
        # print(string)
        pattern = "back referenced name 'six' not a rule or UDT name"
        found = re.search(pattern, string)
        self.assertTrue(found)

    def test_api_semantic_4(self):
        '''Test invalid grammar- bkr-op refers to undefined UDT.'''
        input = start + line1 + line2 + line3 + line4 + line7
        api.generate(input, phase='semantic')
        self.assertTrue(api.errors)
        string = api.display_errors()
        # print()
        # print(string)
        pattern = "back referenced name 'u_notdefined' not a rule or UDT name"
        found = re.search(pattern, string)
        self.assertTrue(found)

    def test_api_semantic_5(self):
        '''Test invalid grammar- rule name previously defined.'''
        input = start + line1 + line2 + line3 + line4 + line8
        api.generate(input, phase='semantic')
        self.assertTrue(api.errors)
        string = api.display_errors()
        # print()
        # print(string)
        pattern = "Rule name 'four' previously defined\\."
        found = re.search(pattern, string)
        self.assertTrue(found)

    def test_api_semantic_7(self):
        '''Test invalid grammar- repetition min > max.'''
        input = start + line1 + line2 + line3 + line4 + line9
        api.generate(input, phase='semantic')
        self.assertTrue(api.errors)
        string = api.display_errors()
        # print()
        # print(string)
        pattern = "repetition min\\(2\\) > max\\(1\\)"
        found = re.search(pattern, string)
        self.assertTrue(found)

    def test_api_semantic_8(self):
        '''Test invalid grammar- repetition min, max = 0, 0 not allowed.'''
        input = start + line1 + line2 + line3 + line4 + line10
        api.generate(input, phase='semantic')
        self.assertTrue(api.errors)
        string = api.display_errors()
        # print()
        # print(string)
        pattern = 'repetition 0\\*0 not allowed - '
        pattern += 'for explicit empty string use ""'
        found = re.search(pattern, string)
        self.assertTrue(found)

    def test_api_semantic_9(self):
        '''Test invalid grammar- TRG min > max.'''
        input = start + line1 + line2 + line3 + line4 + line11
        api.generate(input, phase='semantic')
        self.assertTrue(api.errors)
        string = api.display_errors()
        # print()
        # print(string)
        pattern = 'TRG, terminal range, min\\(127\\) > max\\(32\\)'
        found = re.search(pattern, string)
        self.assertTrue(found)

    def test_api_semantic_10(self):
        '''Test invalid grammar- inc-alt rule not defined.'''
        input = start + line1 + line2 + line3 + line4 + line12
        api.generate(input, phase='semantic')
        self.assertTrue(api.errors)
        string = api.display_errors()
        # print()
        # print(string)
        pattern = 'Rule name \'five\' for incremental alternative '
        pattern += 'not previously defined\\.'
        found = re.search(pattern, string)
        self.assertTrue(found)

    def test_api_semantic_11(self):
        '''Test valid grammar- test inc-alt.'''
        line1 = 'start = A / %d66 /B\n'
        line2 = 'A = %d65\n'
        line3 = 'B = %d67\n'
        line5 = 'start = A\n'
        line6 = 'start =/ %d66\n'
        line7 = 'start =/ B\n'
        input = line1 + line2 + line3
        grammar = api.generate(input)
        self.assertFalse(api.errors)
        result = utils.pprint_to_string(grammar.rules, fname)
        self.assertTrue(result['error'] is None)
        string = result['string']
        # print()
        # print(string)
        # create same grammar using inc-alt
        input = line5 + line2 + line3 + line6 + line7
        grammar = api.generate(input)
        self.assertFalse(api.errors)
        result = utils.pprint_to_string(grammar.rules, fname)
        self.assertTrue(result['error'] is None)
        string_inc_alt = result['string']
        # print()
        # print(string_inc_alt)
        self.assertTrue(string == string_inc_alt)

    def test_api_semantic_12(self):
        '''Test valid grammar- parse the generated grammar object.'''
        input = '''float    = sign decimal exponent
sign     = ["+" / "-"]
decimal  = integer [dot fraction]
           / dot fraction
integer  = 1*%d48-57
dot      = "."
fraction = *%d48-57
exponent = ["e" esign exp]
esign    = ["+" / "-"]
exp      = 1*%d48-57
'''
        grammar = api.generate(input)
        self.assertFalse(api.errors)
        parser = Parser(grammar)
        string = '+123.456E-10'
        result = parser.parse(utils.string_to_tuple(string))
        self.assertTrue(result.success)
