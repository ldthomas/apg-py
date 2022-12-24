import unittest
import re
# from pprint import pprint
from apg_py.lib import identifiers as id
from apg_py.lib.parser import Parser
from apg_py.lib import utilities as utils
from tests.grammars import abnf as abnf_grammar


def whatToDo(name, cbData):
    if(cbData['state'] == id.ACTIVE):
        cbData['user_data']['string'] += name + ': down\n'
    else:
        cbData['user_data']['string'] += name + ': up: state: '
        cbData['user_data']['string'] += id.dict.get(cbData['state'])
        cbData['user_data']['string'] += ': phrase_length: '
        cbData['user_data']['string'] += str(cbData['phrase_length'])
        cbData['user_data']['string'] += '\n'


def udata(name, cbData):
    if(name in cbData['user_data']):
        cbData['user_data'][name] = cbData['user_data'][name] + 1
    else:
        cbData['user_data'][name] = 1


def abnf(cbData):
    udata('abnf', cbData)
    whatToDo('abnf', cbData)


def rtrg(cbData):
    udata('rtrg', cbData)
    whatToDo('rtrg', cbData)


def rtbs(cbData):
    udata('rtbs', cbData)
    whatToDo('rtbs', cbData)


def rtls(cbData):
    udata('rtls', cbData)
    whatToDo('rtls', cbData)


class TestRnmCallbacks(unittest.TestCase):
    """Test parser with rule name callback functions."""

    def test_1(self):
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
        parser = Parser(abnf_grammar)
        parser.add_callbacks({'abnf': abnf})
        parser.add_callbacks({'rtbs': rtbs})
        parser.add_callbacks({'rtls': rtls})
        parser.add_callbacks({'rtrg': rtrg})
        data = {'string': ''}
        result = parser.parse(input, user_data=data)
        regex = 'abnf.*MATCH.*13'
        found = re.search(regex, data['string'])
        self.assertTrue(found, 'abnf should have phrase_length 13')
        regex = 'rtrg.*MATCH.*1'
        found = re.search(regex, data['string'])
        self.assertTrue(found, 'rtrg should have phrase_length 1')
        self.assertTrue(result.success)
        # print()
        # print('user data')
        # pprint(data)
        # print()
        # print(result)

    def test_2(self):
        input = (65, 66)
        parser = Parser(abnf_grammar)
        parser.add_callbacks({'abnf': abnf})
        parser.add_callbacks({'rtbs': rtbs})
        parser.add_callbacks({'rtls': rtls})
        parser.add_callbacks({'rtrg': rtrg})
        data = {'string': ''}
        result = parser.parse(input, user_data=data)
        regex = 'rtbs.*MATCH.*2'
        found = re.search(regex, data['string'])
        self.assertTrue(found, 'abnf should have phrase_length 13')
        self.assertTrue(result.success)

    def test_3(self):
        input = (67, 68)
        parser = Parser(abnf_grammar)
        parser.add_callbacks({'abnf': abnf})
        parser.add_callbacks({'rtbs': rtbs})
        parser.add_callbacks({'rtls': rtls})
        parser.add_callbacks({'rtrg': rtrg})
        data = {'string': ''}
        result = parser.parse(input, user_data=data)
        regex = 'rtls.*MATCH.*2'
        found = re.search(regex, data['string'])
        self.assertTrue(found, 'rtlf should have phrase_length 2')
        self.assertTrue(result.success)

    def test_4(self):
        '''Start rule not first rule.'''
        input = (67, 68)
        parser = Parser(abnf_grammar)
        result = parser.parse(input, start_rule='rtls')
        self.assertTrue(result.success)

    def test_5(self):
        '''Invalid start rule.'''
        input = (67, 68)
        parser = Parser(abnf_grammar)
        with self.assertRaises(Exception):
            parser.parse(input, start_rule='garbage')


if __name__ == '__main__':
    unittest.main()
