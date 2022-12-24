import unittest
import re
from apg_py.api.api import Api

valid_input = 'start = one two / three\r\n'
valid_input += 'one = "1"\n'
valid_input += 'two = "2"\r'
valid_input += 'three = "3"\n'

invalid_input = 'start = one \x03 two / three\r\n'
invalid_input += 'one = "1"\n'
invalid_input += 'two = "2"\r'
invalid_input += 'three = "3"'


class TestApiScanner(unittest.TestCase):
    """Test the scanner phase of the API generator."""

    def test_api_scanner_1(self):
        '''Test valid grammar, strict = False.'''
        api = Api()
        self.assertFalse(api.errors)

    def test_api_scanner_2(self):
        '''Test valid grammar, find_line() function.'''
        api = Api()
        grammar = api.generate(valid_input, phase='scanner')
        self.assertFalse(api.errors)
        line_no = api.find_line(0)
        self.assertTrue(line_no == 0)
        line_no = api.find_line(24)
        self.assertTrue(line_no == 0)
        line_no = api.find_line(25)
        self.assertTrue(line_no == 1)
        line_no = api.find_line(35)
        self.assertTrue(line_no == 2)
        line_no = api.find_line(45)
        self.assertTrue(line_no == 3)
        line_no = api.find_line(49)
        self.assertTrue(line_no == 3)

    def test_api_scanner_3(self):
        '''Test grammar not strict ABNF.'''
        api = Api()
        grammar = api.generate(valid_input, strict=True, phase='scanner')
        self.assertTrue(api.errors)
        display = api.display_errors()
        found = re.search('LF.*not allowed', display)
        self.assertTrue(found)
        found = re.search('CR.*not allowed', display)
        self.assertTrue(found)

    def test_api_scanner_4(self):
        '''Test invalid grammar.'''
        api = Api()
        grammar = api.generate(invalid_input, phase='scanner')
        self.assertTrue(api.errors)
        display = api.display_errors()
        found = re.search('invalid character found: \\\\x03', display)
        self.assertTrue(found)
        found = re.search(
            'last line must end with line end character',
            display)
        self.assertTrue(found)


if __name__ == '__main__':
    unittest.main()
