import unittest
import sys
import re
from apg_py.lib import identifiers as id
from apg_py.lib import utilities as utils
from apg_py.lib.parser import Parser
from apg_py.lib.trace import Trace
from tests.grammars import float_udt


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


def badInteger1(cbData):
    # u_integer cannot return EMPTY
    cbData['state'] = id.EMPTY
    cbData['phrase_length'] = 0


def badInteger2(cbData):
    # u_integer cannot return MATCH with 0 phrase length
    cbData['state'] = id.MATCH
    cbData['phrase_length'] = 0


def badInteger3(cbData):
    # u_integer returns phrase length too long
    cbData['state'] = id.MATCH
    cbData['phrase_length'] = 100


fname = 'tests/temp.out'


class TestTrace(unittest.TestCase):
    """Test UDT operator and callbacks."""

    def test_udt_1(self):
        '''Test proper UDT callbacks.'''
        input = '+12.34E-10'
        parser = Parser(float_udt)
        parser.add_callbacks({'e_sign': udtSign})
        parser.add_callbacks({'u_integer': udtInteger})
        fd = open(fname, 'w')
        saveout = sys.stdout
        sys.stdout = fd
        Trace(parser, mode='xc', line_max=8)
        result = parser.parse(utils.string_to_tuple(input))
        sys.stdout = saveout
        fd.close()
        with open(fname, 'r') as fd:
            strTrace = fd.read()
            # length = os.path.getsize(fname)
            # print()
            # print('file length ', length)
            # print(strTrace)
            found = re.search('|M|1|UDT(e_sign)', strTrace)
            self.assertTrue(found, 'trace of UDT(e_sign) incorrect')
            found = re.search('|M|2|UDT(u_integer)', strTrace)
            self.assertTrue(found, 'trace of UDT(u_integer) incorrect')
        self.assertTrue(result.success)

    def test_udt_2(self):
        '''Test with missing UDT callbacks.'''
        input = '+12.34E-10'
        parser = Parser(float_udt)
        with self.assertRaises(Exception):
            parser.parse(utils.string_to_tuple(input))
        parser = Parser(float_udt)
        parser.add_callbacks({'e_sign': udtSign})
        with self.assertRaises(Exception):
            parser.parse(utils.string_to_tuple(input))
        parser = Parser(float_udt)
        parser.add_callbacks({'u_integer': udtInteger})
        with self.assertRaises(Exception):
            parser.parse(utils.string_to_tuple(input))

    def test_udt_3(self):
        '''Test with bad UDT callback returns.'''
        input = '+12.34E-10'
        parser = Parser(float_udt)
        parser.add_callbacks({'e_sign': udtSign})
        parser.add_callbacks({'u_integer': badInteger1})
        with self.assertRaises(Exception):
            parser.parse(utils.string_to_tuple(input))
        parser = Parser(float_udt)
        parser.add_callbacks({'e_sign': badInteger2})
        parser.add_callbacks({'u_integer': udtInteger})
        with self.assertRaises(Exception):
            parser.parse(utils.string_to_tuple(input))
        parser = Parser(float_udt)
        parser.add_callbacks({'e_sign': udtSign})
        parser.add_callbacks({'u_integer': badInteger2})
        with self.assertRaises(Exception):
            parser.parse(utils.string_to_tuple(input))
        parser = Parser(float_udt)
        parser.add_callbacks({'e_sign': udtSign})
        parser.add_callbacks({'u_integer': badInteger3})
        with self.assertRaises(Exception):
            parser.parse(utils.string_to_tuple(input))


if __name__ == '__main__':
    unittest.main()
