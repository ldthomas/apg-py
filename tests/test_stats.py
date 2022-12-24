import unittest
import sys
from apg_py.lib import identifiers as id
from apg_py.lib import utilities as utils
from apg_py.lib.parser import Parser
from apg_py.lib.stats import Stats
from tests.grammars import float_udt
from tests.grammars import anbncn


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


class TestStats(unittest.TestCase):
    """Test statistics collection."""

    def test_stats_1(self):
        '''Test full float with UDT callbacks.'''
        input = '+12.34E-10'
        parser = Parser(float_udt)
        parser.add_callbacks({'e_sign': udtSign})
        parser.add_callbacks({'u_integer': udtInteger})
        stats = Stats(parser)
        result = parser.parse(utils.string_to_tuple(input))
        self.assertTrue(result.success)
        # stats.display()
        total = stats.total(stats.stats[id.UDT])
        self.assertTrue(total == 2)
        self.assertTrue(stats.stats[id.UDT][id.MATCH] == 2)
        total = stats.total(stats.rule_stats['e_sign'])
        self.assertTrue(total == 1)
        self.assertTrue(stats.rule_stats['u_integer'][id.MATCH] == 1)

    def test_stats_2(self):
        '''Test partial float with UDT callbacks.'''
        input = '1234'
        parser = Parser(float_udt)
        parser.add_callbacks({'e_sign': udtSign})
        parser.add_callbacks({'u_integer': udtInteger})
        stats = Stats(parser)
        result = parser.parse(utils.string_to_tuple(input))
        self.assertTrue(result.success)
        # stats.display()
        total = stats.total(stats.stats[id.UDT])
        self.assertTrue(total == 2)
        self.assertTrue(stats.stats[id.UDT][id.MATCH] == 1)
        self.assertTrue(stats.stats[id.UDT][id.EMPTY] == 1)
        total = stats.total(stats.rule_stats['e_sign'])
        self.assertTrue(total == 1)
        self.assertTrue(stats.rule_stats['e_sign'][id.EMPTY] == 1)
        self.assertTrue(stats.rule_stats['exponent'][id.EMPTY] == 1)

    def test_stats_3(self):
        '''Test anbnc recursive with look ahead.'''
        input = 'aaabbbccc'
        parser = Parser(anbncn)
        stats = Stats(parser)
        result = parser.parse(utils.string_to_tuple(input))
        self.assertTrue(result.success)
        # stats.display()
        total = stats.total(stats.stats[id.AND])
        self.assertTrue(total == 1)
        total = stats.total(stats.stats[id.NOT])
        self.assertTrue(total == 2)
        self.assertTrue(stats.stats[id.AND][id.EMPTY] == 1)
        self.assertTrue(stats.stats[id.NOT][id.EMPTY] == 2)
        total = stats.total(stats.rule_stats['a'])
        self.assertTrue(total == 4)
        self.assertTrue(stats.rule_stats['a'][id.NOMATCH] == 1)
        self.assertTrue(stats.rule_stats['a'][id.MATCH] == 3)


if __name__ == '__main__':
    unittest.main()
