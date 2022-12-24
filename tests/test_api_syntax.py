import unittest
import re
from apg_py.api.api import Api

valid_input = 'start = one two / three\r\n'
valid_input += 'one = "1"\n'
valid_input += 'two = "2"\r'
valid_input += 'three = \'3\'\n'

invalid_input = 'start = one \x03 two / three\r\n'
invalid_input += 'one = "1"\n'
invalid_input += 'two = "2"\r'
invalid_input += 'three = "3"\n'


class TestApiSyntax(unittest.TestCase):
    """Test the syntax phase of the API generator."""

    def test_api_syntax_1(self):
        '''Test valid grammar, strict = False.'''
        api = Api()
        grammar = api.generate(valid_input, phase='syntax')
        self.assertFalse(api.errors)

    def test_api_syntax_2(self):
        '''Test valid grammar, find_line() function.'''
        api = Api()
        grammar = api.generate(valid_input, phase='syntax')
        self.assertFalse(api.errors)
        line_no = api.find_line(0)
        self.assertTrue(line_no == 0)
        line_no = api.find_line(24)
        self.assertTrue(line_no == 0)
        line_no = api.find_line(25)
        self.assertTrue(line_no == 1)
        line_no = api.find_line(29)
        self.assertTrue(line_no == 1)
        line_no = api.find_line(35)
        self.assertTrue(line_no == 2)
        line_no = api.find_line(44)
        self.assertTrue(line_no == 2)
        line_no = api.find_line(45)
        self.assertTrue(line_no == 3)
        line_no = api.find_line(100)
        self.assertTrue(line_no == 3)

    def test_api_syntax_3(self):
        '''Test grammar not strict ABNF.'''
        api = Api()
        result = api.generate(valid_input, strict=True, phase='syntax')
        self.assertTrue(api.errors)
        # print()
        # print(api.display_errors())
        display = api.display_errors()
        found = re.search('LF.*not allowed', display)
        self.assertTrue(found)
        found = re.search('CR.*not allowed', display)
        self.assertTrue(found)

    def test_api_syntax_4(self):
        '''Test invalid grammar.'''
        api = Api()
        grammar = api.generate(invalid_input, phase='syntax')
        self.assertTrue(api.errors)
        display = api.display_errors()
        found = re.search('invalid character found: \\\\x03', display)
        self.assertTrue(found)

    def test_api_syntax_5(self):
        '''Test rule name error.'''
        api = Api()
        grammar = api.generate('$start = "a"\n', phase='syntax')
        self.assertTrue(api.errors)
        display = api.display_errors()
        found = re.search('malformed rule name', display)
        self.assertTrue(found)

    def test_api_syntax_6(self):
        '''Test defined as error.'''
        api = Api()
        grammar = api.generate('start $ "a"\n', phase='syntax')
        self.assertTrue(api.errors)
        display = api.display_errors()
        found = re.search('expected "defined as".*not found', display)
        self.assertTrue(found)

    def test_api_syntax_6_1(self):
        '''Test malformed rule.'''
        api = Api()
        grammar = api.generate('start =$ "a"\n', phase='syntax')
        self.assertTrue(api.errors)
        display = api.display_errors()
        # print()
        # print(display)
        found = re.search('malformed rule', display)
        self.assertTrue(found)

    def test_api_syntax_7(self):
        '''Test unclosed group.'''
        api = Api()
        grammar = api.generate('start = ("a" "b" / "c"\n', phase='syntax')
        self.assertTrue(api.errors)
        display = api.display_errors()
        found = re.search('expected group closure, "\\)", not found', display)
        self.assertTrue(found)

    def test_api_syntax_8(self):
        '''Test unclosed option.'''
        api = Api()
        grammar = api.generate('start = "a" ["b" / "c"\n', phase='syntax')
        self.assertTrue(api.errors)
        display = api.display_errors()
        found = re.search('expected option closure, "\\]", not found', display)
        self.assertTrue(found)

    def test_api_syntax_9(self):
        '''Test string not closed.'''
        api = Api()
        grammar = api.generate('start = "a" "b" / "c\n', phase='syntax')
        self.assertTrue(api.errors)
        display = api.display_errors()
        found = re.search(
            'expected literal string closure, ", not found',
            display)
        self.assertTrue(found)

    def test_api_syntax_9_1(self):
        '''Test prose value not closed.'''
        api = Api()
        grammar = api.generate(
            'start = "a" "b" / <prose value\n',
            phase='syntax')
        self.assertTrue(api.errors)
        display = api.display_errors()
        found = re.search(
            'expected prose value closure, >, not found',
            display)
        self.assertTrue(found)

    def test_api_syntax_10(self):
        '''Test case-sensitive literal string not closed.'''
        api = Api()
        grammar = api.generate('start = "a" ["b" / \'c"\n', phase='syntax')
        self.assertTrue(api.errors)
        display = api.display_errors()
        found = re.search(
            'expected case-sensitive literal string closure, \', not found',
            display)
        self.assertTrue(found)

    def test_api_syntax_11(self):
        '''Test tab not allowed in literal string.'''
        api = Api()
        grammar = api.generate('start = "a\tb"\n', phase='syntax')
        self.assertTrue(api.errors)
        display = api.display_errors()
        found = re.search(
            'tab characters not allowed in quoted strings or prose values',
            display)
        self.assertTrue(found)

    def test_api_syntax_12(self):
        '''Test tab not allowed in case-sensitive literal string.'''
        api = Api()
        grammar = api.generate('start = \'a\tb\'\n', phase='syntax')
        self.assertTrue(api.errors)
        display = api.display_errors()
        found = re.search(
            'tab characters not allowed in quoted strings or prose values',
            display)
        self.assertTrue(found)

    def test_api_syntax_13(self):
        '''Test tab not allowed in case-sensitive literal string.'''
        api = Api()
        grammar = api.generate('start = <prose\tvalue>\n', phase='syntax')
        self.assertTrue(api.errors)
        display = api.display_errors()
        found = re.search(
            'tab characters not allowed in quoted strings or prose values',
            display)
        self.assertTrue(found)
        found = re.search(
            'prose values.*no parser operator can be generated',
            display)
        self.assertTrue(found)

    def test_api_syntax_14(self):
        '''Test prose value not closed.'''
        api = Api()
        grammar = api.generate('start = <prose value\n', phase='syntax')
        self.assertTrue(api.errors)
        display = api.display_errors()
        found = re.search(
            'expected prose value closure, >, not found',
            display)
        self.assertTrue(found)

    def test_api_syntax_15(self):
        '''Test UDT not allowed with strict ABNF.'''
        api = Api()
        grammar = api.generate(
            'start = "a" u_name\r\n',
            strict=True,
            phase='syntax')
        self.assertTrue(api.errors)
        display = api.display_errors()
        found = re.search(
            'UDTs.*not allowed with strict ABNF',
            display)
        self.assertTrue(found)

    def test_api_syntax_16(self):
        '''Test AND (&) not allowed with strict ABNF.'''
        api = Api()
        grammar = api.generate(
            'start = &"a" "b"\r\n',
            strict=True,
            phase='syntax')
        self.assertTrue(api.errors)
        display = api.display_errors()
        found = re.search(
            '& operator.*not allowed with strict ABNF',
            display)
        self.assertTrue(found)

    def test_api_syntax_17(self):
        '''Test NOT (!) not allowed with strict ABNF.'''
        api = Api()
        grammar = api.generate(
            'start = !"a" "b"\r\n',
            strict=True,
            phase='syntax')
        self.assertTrue(api.errors)
        display = api.display_errors()
        found = re.search(
            '! operator.*not allowed with strict ABNF',
            display)
        self.assertTrue(found)

    def test_api_syntax_18(self):
        '''Test positive look behind (&&) not allowed with strict ABNF.'''
        api = Api()
        grammar = api.generate(
            'start = &&"a" "b"\r\n',
            strict=True,
            phase='syntax')
        self.assertTrue(api.errors)
        display = api.display_errors()
        found = re.search(
            '&& operator.*not allowed with strict ABNF',
            display)
        self.assertTrue(found)

    def test_api_syntax_19(self):
        '''Test negative look behind (!!) not allowed with strict ABNF.'''
        api = Api()
        grammar = api.generate(
            'start = !!"a" "b"\r\n',
            strict=True,
            phase='syntax')
        self.assertTrue(api.errors)
        display = api.display_errors()
        found = re.search(
            '!!.*not allowed with strict ABNF',
            display)
        self.assertTrue(found)

    def test_api_syntax_20(self):
        '''Test begin of string anchor (%^) not allowed with strict ABNF.'''
        api = Api()
        grammar = api.generate(
            'start = %^ "a" "b"\r\n',
            strict=True,
            phase='syntax')
        self.assertTrue(api.errors)
        display = api.display_errors()
        found = re.search(
            '%\\^ operator.*not allowed with strict ABNF',
            display)
        self.assertTrue(found)

    def test_api_syntax_21(self):
        '''Test end of string anchor not allowed with strict ABNF.'''
        api = Api()
        grammar = api.generate(
            'start = "a" "b" %$\r\n',
            strict=True,
            phase='syntax')
        self.assertTrue(api.errors)
        display = api.display_errors()
        found = re.search(
            '%\\$ operator.*not allowed with strict ABNF',
            display)
        self.assertTrue(found)

    def test_api_syntax_22(self):
        '''Test back referencing not allowed with strict ABNF.'''
        api = Api()
        grammar = api.generate(
            'start = A \\A\r\n',
            strict=True,
            phase='syntax')
        self.assertTrue(api.errors)
        display = api.display_errors()
        found = re.search(
            '\\(back referencing\\) not allowed with strict ABNF',
            display)
        self.assertTrue(found)

    def test_api_syntax_23(self):
        '''Test back referencing not allowed with strict ABNF.'''
        api = Api()
        grammar = api.generate(
            'start = A \\%s%rA\r\n',
            strict=True,
            phase='syntax')
        self.assertTrue(api.errors)
        display = api.display_errors()
        found = re.search(
            '\\(back referencing\\) not allowed with strict ABNF',
            display)
        self.assertTrue(found)


if __name__ == '__main__':
    unittest.main()
