from logging import exception
import unittest
import re
from apg_py.lib import identifiers as id
from apg_py.lib import utilities as utils
from apg_py.exp.exp import ApgExp

pattern = '''float    = sign decimal exponent
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

udt_pattern = '''float    = sign decimal exponent
sign     = e_sign ; ["+" / "-"]
decimal  = integer [dot fraction]
           / dot fraction
integer  = u_integer ; 1*%d48-57
dot      = "."
fraction = *%d48-57
exponent = ["e" esign exp]
esign    = ["+" / "-"]
exp      = 1*%d48-57
'''

full_float = '-1.23+E10'


def udt_sign(cbData):
    # matches '+', '-' or empty string
    cbData['phrase_length'] = 0
    cbData['state'] = id.EMPTY
    if(cbData['phrase_index'] < cbData['sub_end']):
        char = cbData['input'][cbData['phrase_index']]
        if(char == 43 or char == 45):
            cbData['phrase_length'] = 1
            cbData['state'] = id.MATCH


def udt_integer(cbData):
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


class TestExpInclude(unittest.TestCase):
    """Testing the ApgExp include functions
    with UDTs."""

    def test_include_1(self):
        '''Test add UDT with no-UDT pattern.'''
        exp = ApgExp(pattern)
        with self.assertRaises(Exception) as context:
            exp.define_udts({'sign': udt_sign})
        # print()
        # print(context.exception)
        self.assertTrue(str(context.exception) == 'pattern has no UDTs')

    def test_include_2(self):
        '''Test UDT callbacks not set.'''
        exp = ApgExp(udt_pattern)
        with self.assertRaises(Exception) as context:
            result = exp.exec(full_float)
        # print()
        # print(context.exception)
        self.assertTrue(
            'All UDTs require a callback function.' in str(
                context.exception))

    def test_include_3(self):
        '''Test UDT not found.'''
        exp = ApgExp(udt_pattern)
        with self.assertRaises(Exception) as context:
            exp.define_udts({'e_sign': udt_sign, 'u_int': udt_integer})
        # print()
        # print(context.exception)
        self.assertTrue(
            'UDT name u_int not found' == str(context.exception))

    def test_include_4(self):
        '''Include all rules and UDTs.'''
        exp = ApgExp(udt_pattern)
        exp.define_udts({'e_sign': udt_sign, 'u_integer': udt_integer})
        exp.include()
        result = exp.exec('###-1.23E10$$$')
        # print()
        # print(result)
        string = result.__str__()
        self.assertTrue(re.search('float', string))
        self.assertTrue(re.search('sign', string))
        self.assertTrue(re.search('decimal', string))
        self.assertTrue(re.search('\ninteger', string))
        self.assertTrue(re.search('dot', string))
        self.assertTrue(re.search('fraction', string))
        self.assertTrue(re.search('exponent', string))
        self.assertTrue(re.search('esign', string))
        self.assertTrue(re.search('exp', string))
        self.assertTrue(re.search('e_sign', string))
        self.assertTrue(re.search('u_integer', string))

    def test_include_5(self):
        '''Include some rules and UDTs.'''
        exp = ApgExp(udt_pattern)
        exp.define_udts({'e_sign': udt_sign, 'u_integer': udt_integer})
        exp.include(['sign', 'fraction', 'u_integer'])
        result = exp.exec('###-1.23E10$$$')
        # print()
        # print(result)
        string = result.__str__()
        self.assertFalse(re.search('float', string))
        self.assertTrue(re.search('sign', string))
        self.assertFalse(re.search('decimal', string))
        self.assertFalse(re.search('\ninteger', string))
        self.assertFalse(re.search('dot', string))
        self.assertTrue(re.search('fraction', string))
        self.assertFalse(re.search('exponent', string))
        self.assertFalse(re.search('esign', string))
        self.assertFalse(re.search('exp', string))
        self.assertFalse(re.search('e_sign', string))
        self.assertTrue(re.search('u_integer', string))


class TestExpExclude(unittest.TestCase):
    """Testing the ApgExp exclude functions
    with UDTs."""

    def test_exclude_1(self):
        '''Include all rules and UDTs using the exclude() option.'''
        exp = ApgExp(udt_pattern)
        exp.define_udts({'e_sign': udt_sign, 'u_integer': udt_integer})
        exp.exclude()
        result = exp.exec('###-1.23E10$$$')
        # print()
        # print(result)
        string = result.__str__()
        self.assertTrue(re.search('float', string))
        self.assertTrue(re.search('sign', string))
        self.assertTrue(re.search('decimal', string))
        self.assertTrue(re.search('\ninteger', string))
        self.assertTrue(re.search('dot', string))
        self.assertTrue(re.search('fraction', string))
        self.assertTrue(re.search('exponent', string))
        self.assertTrue(re.search('esign', string))
        self.assertTrue(re.search('exp', string))
        self.assertTrue(re.search('e_sign', string))
        self.assertTrue(re.search('u_integer', string))

    def test_exclude_1(self):
        '''Include a few rules and UDTs using the exclude() option.'''
        exp = ApgExp(udt_pattern)
        exp.define_udts({'e_sign': udt_sign, 'u_integer': udt_integer})
        exp.exclude(['float', 'dot', 'e_sign'])
        result = exp.exec('###-1.23E10$$$')
        # print()
        # print(result)
        string = result.__str__()
        self.assertFalse(re.search('float', string))
        self.assertTrue(re.search('sign', string))
        self.assertTrue(re.search('decimal', string))
        self.assertTrue(re.search('\ninteger', string))
        self.assertFalse(re.search('dot', string))
        self.assertTrue(re.search('fraction', string))
        self.assertTrue(re.search('exponent', string))
        self.assertTrue(re.search('esign', string))
        self.assertTrue(re.search('exp', string))
        self.assertFalse(re.search('e_sign', string))
        self.assertTrue(re.search('u_integer', string))
