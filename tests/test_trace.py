import unittest
import sys
import re
from apg_py.lib import identifiers as id
from apg_py.lib import utilities as utils
from apg_py.lib.parser import Parser
from apg_py.lib.trace import Trace
from tests.grammars import abnf
from tests.grammars import anbncn
from tests.grammars import float_anchors

fname = 'tests/temp.out'


class TestTrace(unittest.TestCase):
    """Test parser tracing."""
    input = (
        123,
        124,
        125,
        126,
        127,
        128,
        123,
        125,
        255,
        123,
        256,
        125,
        1024)

    def test_trace_1(self):
        '''Test rule name matches and no matches with truncated output.'''
        parser = Parser(abnf)
        fd = open(fname, 'w')
        saveout = sys.stdout
        sys.stdout = fd
        Trace(parser, mode='xc', line_max=8)
        result = parser.parse(self.input)
        sys.stdout = saveout
        fd.close()
        with open(fname, 'r') as fd:
            strTrace = fd.read()
            # length = os.path.getsize(fname)
            # print()
            # print('file length ', length)
            # print(strTrace)
            found = re.search('\\.\\.|N|0|RNM(rtls)', strTrace)
            self.assertTrue(found, 'trace of rtls incorrect')
            found = re.search('\\.\\.|N|0|RNM(rtbs)', strTrace)
            self.assertTrue(found, 'trace of rtbs incorrect')
            found = re.search('\\.\\.\\.|M|1|RNM(rtrg)', strTrace)
            self.assertTrue(found, 'trace of rtrg incorrect')
            found = re.search('{|}~ x7f x80 {}\\.\\.\\.', strTrace)
            self.assertTrue(found, 'truncated hex line incorrect')
        self.assertTrue(result.success)

    def test_trace_2(self):
        '''Test mixed hexadecimal+ASCII character output'''
        parser = Parser(abnf)
        fd = open(fname, 'w')
        saveout = sys.stdout
        sys.stdout = fd
        Trace(parser, mode='xc', line_max=32)
        result = parser.parse(self.input)
        sys.stdout = saveout
        fd.close()
        with open(fname, 'r') as fd:
            strTrace = fd.read()
            # length = os.path.getsize(fname)
            # print()
            # print('file length ', length)
            # print(strTrace)
            found = re.search('{|}~ x7f x80 {} xff { x100 } x400', strTrace)
            self.assertTrue(found, 'truncated hex line incorrect')
        self.assertTrue(result.success)

    def test_trace_3(self):
        '''Test mixed decimal+ASCII character output'''
        parser = Parser(abnf)
        fd = open(fname, 'w')
        saveout = sys.stdout
        sys.stdout = fd
        Trace(parser, mode='dc', line_max=32)
        result = parser.parse(self.input)
        sys.stdout = saveout
        fd.close()
        with open(fname, 'r') as fd:
            strTrace = fd.read()
            # length = os.path.getsize(fname)
            # print()
            # print('file length ', length)
            # print(strTrace)
            found = re.search('{|}~ 127 128 {} 255 { 256 } 1024', strTrace)
            self.assertTrue(found, 'truncated hex line incorrect')
        self.assertTrue(result.success)

    def test_trace_4(self):
        '''Test hexadecimal character code output'''
        parser = Parser(abnf)
        fd = open(fname, 'w')
        saveout = sys.stdout
        sys.stdout = fd
        Trace(parser, mode='x', line_max=32)
        result = parser.parse(self.input)
        sys.stdout = saveout
        fd.close()
        with open(fname, 'r') as fd:
            strTrace = fd.read()
            # length = os.path.getsize(fname)
            # print()
            # print('file length ', length)
            # print(strTrace)
            found = re.search(
                'x7b x7c x7d x7e x7f x80 x7b x7d xff x7b x100 x7d x400',
                strTrace)
            self.assertTrue(found, 'truncated hex line incorrect')
        self.assertTrue(result.success)

    def test_trace_4(self):
        '''Test decimal character code output'''
        parser = Parser(abnf)
        fd = open(fname, 'w')
        saveout = sys.stdout
        sys.stdout = fd
        Trace(parser, mode='d', line_max=32)
        result = parser.parse(self.input)
        sys.stdout = saveout
        fd.close()
        with open(fname, 'r') as fd:
            strTrace = fd.read()
            # length = os.path.getsize(fname)
            # print()
            # print('file length ', length)
            # print(strTrace)
            found = re.search(
                '123 124 125 126 127 128 123 125 255 123 256 125 1024',
                strTrace)
            self.assertTrue(found, 'truncated hex line incorrect')
        self.assertTrue(result.success)

    def test_trace_5(self):
        '''Test that trace raises and Exception
        if mode not 'x, 'd', 'xc' or 'dc'.'''
        parser = Parser(abnf)
        with self.assertRaises(Exception):
            Trace(parser, mode='h', line_max=32)

    def test_lookahead(self):
        '''Test AND and NOT operators.'''
        input = 'aaabbbccc'
        parser = Parser(anbncn)
        fd = open(fname, 'w')
        saveout = sys.stdout
        sys.stdout = fd
        Trace(parser, mode='xc')
        result = parser.parse(utils.string_to_tuple(input))
        sys.stdout = saveout
        fd.close()
        with open(fname, 'r') as fd:
            strTrace = fd.read()
            # length = os.path.getsize(fname)
            # print()
            # print('file length ', length)
            # print(strTrace)
            found = re.search('\\.\\.\\.\\.|E|0|NOT', strTrace)
            self.assertTrue(found, 'NOT operator incorrect')
            found = re.search('\\.\\.|E|0|AND', strTrace)
            self.assertTrue(found, 'AND operator incorrect')
        self.assertTrue(result.success)

    def test_substring(self):
        '''Test parsing a substring.'''
        input = '---aaabbbccc---'
        parser = Parser(anbncn)
        fd = open(fname, 'w')
        saveout = sys.stdout
        sys.stdout = fd
        Trace(parser, mode='xc')
        result = parser.parse(
            utils.string_to_tuple(input),
            sub_begin=3,
            sub_length=9)
        sys.stdout = saveout
        fd.close()
        with open(fname, 'r') as fd:
            strTrace = fd.read()
            # length = os.path.getsize(fname)
            # print()
            # print('file length ', length)
            # print(strTrace)
            found = re.search('\\.\\.\\.\\.|E|0|NOT', strTrace)
            self.assertTrue(found, 'NOT operator incorrect')
            found = re.search('\\.\\.|E|0|AND', strTrace)
            self.assertTrue(found, 'AND operator incorrect')
        self.assertTrue(result.success)

    def test_anchors_1(self):
        '''Test parsing with anchors - begin and end of string anchors ok.'''
        input = '+12.34E+10'
        parser = Parser(float_anchors)
        fd = open(fname, 'w')
        saveout = sys.stdout
        sys.stdout = fd
        Trace(parser, mode='xc')
        result = parser.parse(
            utils.string_to_tuple(input),
            sub_begin=0,
            sub_length=0)
        sys.stdout = saveout
        fd.close()
        with open(fname, 'r') as fd:
            strTrace = fd.read()
            # length = os.path.getsize(fname)
            # print()
            # print('file length ', length)
            # print(strTrace)
            found = re.search('\\.\\.|E|0|ABG', strTrace)
            self.assertTrue(found, 'ABG operator incorrect')
            found = re.search('\\.\\.|E|0|AEN', strTrace)
            self.assertTrue(found, 'AEN operator incorrect')
        self.assertTrue(result.success)

    def test_anchors_2(self):
        '''Test parsing with anchors - not begin of string.'''
        input = '===+12.34E+10'
        parser = Parser(float_anchors)
        fd = open(fname, 'w')
        saveout = sys.stdout
        sys.stdout = fd
        Trace(parser, mode='xc')
        result = parser.parse(
            utils.string_to_tuple(input),
            sub_begin=3,
            sub_length=0)
        sys.stdout = saveout
        fd.close()
        with open(fname, 'r') as fd:
            strTrace = fd.read()
            # length = os.path.getsize(fname)
            # print()
            # print('file length ', length)
            # print(strTrace)
            found = re.search('\\.\\.|N|0|ABG', strTrace)
            self.assertTrue(found, 'ABG operator incorrect')
        self.assertFalse(result.success)

    def test_anchors_3(self):
        '''Test parsing with anchors - not end of string.'''
        input = '+12.34E+10==='
        parser = Parser(float_anchors)
        fd = open(fname, 'w')
        saveout = sys.stdout
        sys.stdout = fd
        Trace(parser, mode='xc')
        result = parser.parse(
            utils.string_to_tuple(input),
            sub_begin=0,
            sub_length=10)
        sys.stdout = saveout
        fd.close()
        with open(fname, 'r') as fd:
            strTrace = fd.read()
            # length = os.path.getsize(fname)
            # print()
            # print('file length ', length)
            # print(strTrace)
            found = re.search('\\.\\.|N|0|AEN', strTrace)
            self.assertTrue(found, 'AEN operator incorrect')
        self.assertFalse(result.success)


if __name__ == '__main__':
    unittest.main()
