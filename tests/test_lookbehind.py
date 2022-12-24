import unittest
import os
import sys
import re
from apg_py.lib import identifiers as id
from apg_py.lib import utilities as utils
from apg_py.lib.parser import Parser
from apg_py.lib.trace import Trace
from tests.grammars import float_bka_tls
from tests.grammars import float_bka_tls_empty
from tests.grammars import float_bka_tbs
from tests.grammars import float_bka_trg
from tests.grammars import float_bka_udt
from tests.grammars import float_bka_udt_empty
from tests.grammars import float_bka_alt
from tests.grammars import float_bka_cat
from tests.grammars import float_bka_rep
from tests.grammars import universal_bkr
from tests.grammars import float_bkn_tls


def udtEInteger(cbData):
    '''Match zero or more digits 0-9.'''
    index = cbData['phrase_index']
    length = 0
    while(index < cbData['subEnd']):
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
        cbData['state'] = id.EMPTY


def udtInteger(cbData):
    '''Match one or more digits 0-9.'''
    index = cbData['phrase_index']
    length = 0
    while(index < cbData['subEnd']):
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


fname = 'tests/temp.out'


class TestBKA(unittest.TestCase):
    """Test the positive look behind operator, &&."""

    def test_bka_tls_1(self):
        '''Test positive look behind for TLS.'''
        input = '---abc+12.34E+10'
        parser = Parser(float_bka_tls)
        fd = open(fname, 'w')
        saveout = sys.stdout
        sys.stdout = fd
        Trace(parser, mode='xc', line_max=8)
        result = parser.parse(
            utils.string_to_tuple(input),
            sub_begin=6,
            sub_length=0)
        sys.stdout = saveout
        fd.close()
        with open(fname, 'r') as fd:
            strTrace = fd.read()
            length = os.path.getsize(fname)
            # print()
            # print('file length ', length)
            # print(strTrace)
            found = re.search(r'\.\.\.\|M\|3\|TLS\(97,98,99\)<- abc', strTrace)
            self.assertTrue(found, 'trace of positive look behind incorrect')
            found = re.search(r'\.\.\|E\|0\|BKA', strTrace)
            self.assertTrue(found, 'trace of positive look behind incorrect')
        self.assertTrue(result.success, 'positive look behind failed')

    def test_bka_tls_11(self):
        '''Test positive look behind for failing TLS.'''
        input = '---zzz+12.34E+10'
        parser = Parser(float_bka_tls)
        fd = open(fname, 'w')
        saveout = sys.stdout
        sys.stdout = fd
        Trace(parser, mode='xc', line_max=8)
        result = parser.parse(
            utils.string_to_tuple(input),
            sub_begin=6,
            sub_length=0)
        sys.stdout = saveout
        fd.close()
        with open(fname, 'r') as fd:
            strTrace = fd.read()
            # length = os.path.getsize(fname)
            # print()
            # print('file length ', length)
            # print(strTrace)
            found = re.search(r'\.\.\.\|N\|0\|TLS\(97,98,99\)', strTrace)
            self.assertTrue(found, 'trace of positive look behind incorrect')
            found = re.search(r'\.\.\|N\|0\|BKA', strTrace)
            self.assertTrue(found, 'trace of positive look behind incorrect')
        self.assertFalse(result.success, 'positive look behind succeeded')

    def test_bka_tls_2(self):
        '''Test positive look behind for empty string TLS.'''
        input = '---abc+12.34E+10'
        parser = Parser(float_bka_tls_empty)
        fd = open(fname, 'w')
        saveout = sys.stdout
        sys.stdout = fd
        Trace(parser, mode='xc', line_max=8)
        result = parser.parse(
            utils.string_to_tuple(input),
            sub_begin=6,
            sub_length=0)
        sys.stdout = saveout
        fd.close()
        with open(fname, 'r') as fd:
            strTrace = fd.read()
            # length = os.path.getsize(fname)
            # print()
            # print('file length ', length)
            # print(strTrace)
            found = re.search(r'\.\.\.\|E\|0\|TLS\(\)<-', strTrace)
            self.assertTrue(found, 'trace of positive look behind incorrect')
            found = re.search(r'\.\.\|E\|0\|BKA', strTrace)
            self.assertTrue(found, 'trace of positive look behind incorrect')
        self.assertTrue(result.success, 'positive look behind failed')

    def test_bka_tbs_1(self):
        '''Test positive look behind for TBS.'''
        input = '---abc+12.34E+10'
        parser = Parser(float_bka_tbs)
        fd = open(fname, 'w')
        saveout = sys.stdout
        sys.stdout = fd
        Trace(parser, mode='xc', line_max=8)
        result = parser.parse(
            utils.string_to_tuple(input),
            sub_begin=6,
            sub_length=0)
        sys.stdout = saveout
        fd.close()
        with open(fname, 'r') as fd:
            strTrace = fd.read()
            # length = os.path.getsize(fname)
            # print()
            # print('file length ', length)
            # print(strTrace)
            found = re.search(r'\.\.\.\|M\|3\|TBS\(97,98,99\)<- abc', strTrace)
            self.assertTrue(found, 'trace of positive look behind incorrect')
            found = re.search(r'\.\.\|E\|0\|BKA', strTrace)
            self.assertTrue(found, 'trace of positive look behind incorrect')
        self.assertTrue(result.success, 'positive look behind failed')

    def test_bka_trg_1(self):
        '''Test positive look behind for TRG.'''
        input = '---abc+12.34E+10'
        parser = Parser(float_bka_trg)
        fd = open(fname, 'w')
        saveout = sys.stdout
        sys.stdout = fd
        Trace(parser, mode='xc', line_max=8)
        result = parser.parse(
            utils.string_to_tuple(input),
            sub_begin=6,
            sub_length=0)
        print(result)
        sys.stdout = saveout
        fd.close()
        with open(fname, 'r') as fd:
            strTrace = fd.read()
            # length = os.path.getsize(fname)
            # print()
            # print('file length ', length)
            # print(strTrace)
            found = re.search(r'\.\.\.\|M\|1\|TRG\(97,122\)<- c', strTrace)
            self.assertTrue(found, 'trace of positive look behind incorrect')
            found = re.search(r'\.\.\|E\|0\|BKA', strTrace)
            self.assertTrue(found, 'trace of positive look behind incorrect')
        self.assertTrue(result.success, 'positive look behind failed')

    def test_bka_cat_1(self):
        '''Test positive look behind for CAT.'''
        input = '---ABCabcx+12.34E+10'
        parser = Parser(float_bka_cat)
        fd = open(fname, 'w')
        saveout = sys.stdout
        sys.stdout = fd
        Trace(parser, mode='xc', line_max=8)
        result = parser.parse(
            utils.string_to_tuple(input),
            sub_begin=10,
            sub_length=0)
        print(result)
        sys.stdout = saveout
        fd.close()
        with open(fname, 'r') as fd:
            strTrace = fd.read()
            # length = os.path.getsize(fname)
            # print()
            # print('file length ', length)
            # print(strTrace)
            found = re.search(r'\|M\|1\|TRG\(97,122\)<- x', strTrace)
            self.assertTrue(found, 'trace of positive look behind incorrect')
            found = re.search(r'\|M\|3\|TBS\(97,98,99\)<- abc', strTrace)
            self.assertTrue(found, 'trace of positive look behind incorrect')
            found = re.search(r'\|M\|3\|TLS\(97,98,99\)<- ABC', strTrace)
            self.assertTrue(found, 'trace of positive look behind incorrect')
            found = re.search(r'\.\.\|E\|0\|BKA', strTrace)
            self.assertTrue(found, 'trace of positive look behind incorrect')
        self.assertTrue(result.success, 'positive look behind failed')

    def test_bka_alt_1(self):
        '''Test positive look behind for ALT - rightmost.'''
        input = '---ABCabcx+12.34E+10'
        parser = Parser(float_bka_alt)
        # Trace(parser, mode='xc', line_max=8)
        result = parser.parse(
            utils.string_to_tuple(input),
            sub_begin=10,
            sub_length=0)
        # print(result)
        self.assertTrue(result.success, 'positive look behind failed')

    def test_bka_alt_2(self):
        '''Test positive look behind for ALT - middle.'''
        input = '---ABCxabc+12.34E+10'
        parser = Parser(float_bka_alt)
        # Trace(parser, mode='xc', line_max=8)
        result = parser.parse(
            utils.string_to_tuple(input),
            sub_begin=10,
            sub_length=0)
        # print(result)
        self.assertTrue(result.success, 'positive look behind failed')

    def test_bka_alt_3(self):
        '''Test positive look behind for ALT - leftmost.'''
        input = '---abcxABC+12.34E+10'
        parser = Parser(float_bka_alt)
        result = parser.parse(
            utils.string_to_tuple(input),
            sub_begin=10,
            sub_length=0)
        self.assertTrue(result.success, 'positive look behind failed')

    def test_bka_rep_1(self):
        '''Test positive look behind for REP(1,3) - single match.'''
        input = '---ABC+12.34E+10'
        parser = Parser(float_bka_rep)
        result = parser.parse(
            utils.string_to_tuple(input),
            sub_begin=6,
            sub_length=0)
        self.assertTrue(result.success, 'positive look behind failed')

    def test_bka_rep_3(self):
        '''Test positive look behind for REP(1,3) - double match.'''
        input = '---abcABC+12.34E+10'
        parser = Parser(float_bka_rep)
        result = parser.parse(
            utils.string_to_tuple(input),
            sub_begin=9,
            sub_length=0)
        self.assertTrue(result.success, 'positive look behind failed')

    def test_bka_rep_3(self):
        '''Test positive look behind for REP(1,3) - triple match.'''
        input = '---ABCabcABC+12.34E+10'
        parser = Parser(float_bka_rep)
        result = parser.parse(
            utils.string_to_tuple(input),
            sub_begin=12,
            sub_length=0)
        self.assertTrue(result.success, 'positive look behind failed')

    def test_bka_udt_empty(self):
        '''Test positive look behind for empty UDT.'''
        input = '---12x+12.34E+10'
        parser = Parser(float_bka_udt_empty)
        parser.add_callbacks({'e_digits': udtEInteger})
        with self.assertRaises(Exception):
            parser.parse(
                utils.string_to_tuple(input),
                sub_begin=6,
                sub_length=0)

    def test_bka_udt(self):
        '''Test positive look behind for non-empty UDT.'''
        input = '---123+12.34E+10'
        parser = Parser(float_bka_udt)
        parser.add_callbacks({'U_digits': udtInteger})
        with self.assertRaises(Exception):
            parser.parse(
                utils.string_to_tuple(input),
                sub_begin=6,
                sub_length=0)

    def test_bka_bka(self):
        '''Back reference not allowed in look behind.'''
        input = '---xxabcabc---'
        parser = Parser(universal_bkr)
        with self.assertRaises(Exception):
            parser.parse(
                utils.string_to_tuple(input),
                sub_begin=5,
                sub_length=0)


class TestBKN(unittest.TestCase):
    """Test the negative look behind operator, !!."""

    def test_bkn_tls_1(self):
        '''Test negative look behind for TLS MATCH.'''
        input = '---abc+12.34E+10'
        parser = Parser(float_bkn_tls)
        fd = open(fname, 'w')
        saveout = sys.stdout
        sys.stdout = fd
        Trace(parser, mode='xc', line_max=8)
        result = parser.parse(
            utils.string_to_tuple(input),
            sub_begin=6,
            sub_length=0)
        sys.stdout = saveout
        fd.close()
        with open(fname, 'r') as fd:
            strTrace = fd.read()
            # length = os.path.getsize(fname)
            # print()
            # print('file length ', length)
            # print(strTrace)
            found = re.search(
                r'\.\.\.\|M\|3\|TLS\(97,98,99\)<- abc', strTrace)
            # print()
            # print('re.search')
            # print(found)
            self.assertTrue(found, 'trace of negative look behind incorrect')
            found = re.search(r'\.\.\|N\|0\|BKN', strTrace)
            # print()
            # print('re.search')
            # print(found)
            self.assertTrue(found, 'trace of negative look behind incorrect')
        self.assertFalse(result.success, 'negative look behind succeeded')

    def test_bkn_tls_2(self):
        '''Test negative look behind for TLS NOMATCH.'''
        input = '---zzz+12.34E+10'
        parser = Parser(float_bkn_tls)
        fd = open(fname, 'w')
        saveout = sys.stdout
        sys.stdout = fd
        Trace(parser, mode='xc', line_max=8)
        result = parser.parse(
            utils.string_to_tuple(input),
            sub_begin=6,
            sub_length=0)
        sys.stdout = saveout
        fd.close()
        with open(fname, 'r') as fd:
            strTrace = fd.read()
            # length = os.path.getsize(fname)
            # print()
            # print('file length ', length)
            # print(strTrace)
            found = re.search(
                r'\.\.\.\|N\|0\|TLS\(97,98,99\)', strTrace)
            self.assertTrue(found, 'trace of negative look behind incorrect')
            found = re.search(r'\.\.\|E\|0\|BKN', strTrace)
            self.assertTrue(found, 'trace of negative look behind incorrect')
        self.assertTrue(result.success, 'negative look behind succeeded')


if __name__ == '__main__':
    unittest.main()
