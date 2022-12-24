import unittest
from apg_py.lib import identifiers as id
from apg_py.lib import utilities as utils
from apg_py.lib.parser import Parser
from tests.grammars import recursive_html
from tests.grammars import recursive_html_cs
from tests.grammars import recursive_html_udt
from tests.grammars import recursive_mr
from tests.grammars import universal_html


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


fname = 'tests/temp.out'


class TestBkrr(unittest.TestCase):
    """Test recursive back referencing."""

    def test_bkrr_1(self):
        '''Test simple HTML.'''
        input = '<html></html>'
        parser = Parser(recursive_html)
        result = parser.parse(utils.string_to_tuple(input))
        self.assertTrue(result.success)

    def test_bkrr_2(self):
        '''Test single level nested HTML.'''
        input = '<html><div></div></html>'
        parser = Parser(recursive_html)
        result = parser.parse(utils.string_to_tuple(input))
        self.assertTrue(result.success)

    def test_bkrr_3(self):
        '''Test complex nested HTML.'''
        input = '<html><div></div><p><a></a></p></html>'
        parser = Parser(recursive_html)
        result = parser.parse(utils.string_to_tuple(input))
        self.assertTrue(result.success)

    def test_bkrr_4(self):
        '''Test even more complex nested HTML.'''
        input = '<html><div><h1><H2></h2></H1></DIV><p><a></a></p></html>'
        parser = Parser(recursive_html)
        result = parser.parse(utils.string_to_tuple(input))
        self.assertTrue(result.success)

    def test_bkrr_5(self):
        '''Test case-sensitive nested HTML.'''
        input = '<html><div><h1><h2></h2></h1></div><p><a></a></p></html>'
        parser = Parser(recursive_html_cs)
        result = parser.parse(utils.string_to_tuple(input))
        self.assertTrue(result.success)

    def test_bkrr_6(self):
        '''Test case-sensitive nested HTML - cases not matching.'''
        input = '<html><div><h1><H2></h2></H1></DIV><p><a></a></p></html>'
        parser = Parser(recursive_html_cs)
        result = parser.parse(utils.string_to_tuple(input))
        self.assertFalse(result.success)

    def test_bkrr_7(self):
        '''Test case-sensitive nested HTML - with udt.'''
        input = '<html123><div4><h1><h2></h2></h1></div4><p345>'
        input += '<a999></a999></p345></html123>'
        parser = Parser(recursive_html_udt)
        parser.add_callbacks({'u_digits': udtInteger})
        result = parser.parse(utils.string_to_tuple(input))
        self.assertTrue(result.success)

    def test_bkrr_8(self):
        '''Test round about nested HTML.'''
        input = '<html><div><h1><h2></h2></h1></div><p><a></a></p></html>'
        parser = Parser(recursive_mr)
        result = parser.parse(utils.string_to_tuple(input))
        self.assertTrue(result.success)


class TestBkru(unittest.TestCase):
    """Test universal back referencing."""

    def test_bkru_1(self):
        '''Test simple HTML.'''
        input = '<html></html>'
        parser = Parser(universal_html)
        result = parser.parse(utils.string_to_tuple(input))
        self.assertTrue(result.success)

    def test_bkru_2(self):
        '''Test nested only matches last opened tag HTML.'''
        input = '<html><div></div></div>'
        parser = Parser(universal_html)
        result = parser.parse(utils.string_to_tuple(input))
        self.assertTrue(result.success)

    def test_bkru_3(self):
        '''Test fails with correctly nested HTML.'''
        input = '<html><div></div></html>'
        parser = Parser(universal_html)
        result = parser.parse(utils.string_to_tuple(input))
        self.assertFalse(result.success)


if __name__ == '__main__':
    unittest.main()
