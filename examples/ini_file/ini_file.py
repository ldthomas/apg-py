''' @file examples/ini_file/ini_file.py
@brief The ini file class for parsing an ini file into section/key/values.
'''
import sys
import os
from pprint import pprint
# add the current working directory to the path
# DO NOT MOVE THE FOLLOWING STATEMENT
# if using autopep8 formatter, for example, set argument '--ignore=E402'
sys.path.append(os.getcwd())
from apg_py.lib import utilities as utils
from apg_py.lib.parser import Parser
# from apg_py.lib.trace import Trace
from apg_py.lib.ast import Ast
import examples.ini_file.grammar as grammar
import examples.ini_file.parser_callbacks as pcb
import examples.ini_file.ast_callbacks as acb

# Note: The ABNF syntax for the ini file parser is in grammar.abnf.
# The grammar object, grammar.py was generated with
# python3 apg.py -i examples/ini_file/grammar.abnf


class IniFile:

    def __init__(self):
        self.__have_file = False
        self.__no_file = 'Must first call IniFile.get_ini_file(file_name).'

    def help(self):
        display = '''IniFile is a class for parsing and retrieving named values from an ini formatted file.
This format is similar to, but has some variations from, the WikiPedia description at
https://en.wikipedia.org/wiki/INI_file.

- Named values may be in an unnamed "global" section and/or in named sections.
- Each section consists of lines of key/value pairs.
- Section names are case sensitive and are alphanumeric with underscores.
- Section names are enclosed in square brackets and must begin in the first column of a line.
- Spaces are allowed, e.g. [ Section1 ]
- Keys are case sensitive and are alphanumeric with underscores.
- Values are multi-valued lists.
- Multiple occurrances of a section name will merge the two sections.
- Multiple occurrances of a key name within a section will merge the lists of values.
- Blank lines are ignored.
- Comments begin with a semicolon, ";", and continue to the end of the line.
- Values may be boolean, integers or strings.
- True booleans may be true or yes, case insensitive.
- False booleans may be false or no, case insensitive.
- Null values may be null or void, case insensitive.
- The keywords true, false, yes, no, null, void are reserved
  and must be quoted if needed as strings.
- Strings with blanks characters must be single or double quoted.
- Escaped characters may be used within quoted or unquoted strings.

Escaped characters:
\\\\      single back slash, x5C
\\"      double quote, x22
\\#      hash or number sign, x23
\\'      single quote, x27
\\,      comma, x2C
\\:      colon, x3A
\\;      semicolon, x3B
\\=      equal sign, x3D
\\b      blank or space, x20
\\t      tab, x09
\\n      line feed, x0A
\\r      carriage return, x0D
\\xhh    hexadecimal character code, xhh, h = 0-9A-F
\\uhhhh  Unicode character code, xhhhh, h = 0-9A-F

Example:
; the global section
url         = 'https://en.wikipedia.org/wiki/INI_file'
IP          = '198.162.1.1'
other       = null
[section1]      ; start section A
numbers     = 1, 2,3,  4
use_them    = yes
[ SectionB  ]   ; start section B
hamburgers  = '$1.99', '$2.99', '$3.99'
[ section1 ]    ; continue with section A
numbers     = 5,6   ; add some more numbers to the list

'''
        return display

    def parse_ini_file(self, fname):
        fd = open(fname, 'r')
        input = fd.read()
        fd.close()
        parser = Parser(grammar)
        # Trace(parser, mode='dc')
        parser.add_callbacks({'line-end': pcb.line_end})
        parser.add_callbacks({'bad-section-line': pcb.bad_section_line})
        parser.add_callbacks({'bad-value-line': pcb.bad_value_line})
        parser.add_callbacks({'bad-blank-line': pcb.bad_blank_line})
        ast = Ast(parser)
        ast.add_callback('section-name', acb.section_name)
        ast.add_callback('key-name', acb.key_name)
        ast.add_callback('value', acb.value)
        ast.add_callback('d-quoted-value', acb.d_value)
        ast.add_callback('s-quoted-value', acb.s_value)
        ast.add_callback('string', acb.string_value)
        ast.add_callback('true', acb.true_value)
        ast.add_callback('false', acb.false_value)
        ast.add_callback('null', acb.null_value)
        ast.add_callback('number', acb.number_value)
        data = {}
        data['line_no'] = 0
        data['errors'] = []
        result = parser.parse(utils.string_to_tuple(input), user_data=data)
        if(not result.success):
            # ABNF syntax is designed so that this should never happen
            raise Exception('internal error - parser failed')
        if(len(data['errors'])):
            # display errors
            pprint(data['errors'])
            raise Exception('ini file syntax errors found')
        self.__data = {}
        self.__data['current_section'] = None
        self.__data['current_key'] = None
        self.__data['global'] = {}
        self.__data['sections'] = {}
        ast.translate(self.__data)
        self.__have_file = True
        # print()
        # print('IniFile constructor')
        # pprint(self.__data, sort_dicts=False)

    def get_keys(self):
        '''Get a list of the global key names.
        @returns Returns a list, possibly empty, of global key names.
        '''
        if(not self.__have_file):
            raise Exception(self.__no_file)
        keys = []
        for key, value in self.__data['global'].items():
            keys.append(key)
        return keys

    def get_values(self, key):
        '''Get the list of values for an global key name.
        @param key The name of the key to get values for.
        @returns Returns a list, possibly empty, of values.
        '''
        if(not self.__have_file):
            raise Exception(self.__no_file)
        values = []
        key_values = self.__data['global'].get(key)
        if(key_values):
            for value in key_values:
                values.append(value)
        return values

    def get_sections(self):
        '''Get a list of the section names.
        @returns Returns a list, possibly empty, of section names.
        '''
        if(not self.__have_file):
            raise Exception(self.__no_file)
        sections = []
        for key, value in self.__data['sections'].items():
            sections.append(key)
        return sections

    def get_section_keys(self, section):
        '''Get a list of key names in the named section.
        @param section The section name to find the key names in.
        @returns Returns a list, possibly empty, of key names.
        '''
        if(not self.__have_file):
            raise Exception(self.__no_file)
        keys = []
        if(self.__data['sections'].get(section)):
            for key, value in self.__data['sections'][section].items():
                keys.append(key)
        return keys

    def get_section_values(self, section, key):
        '''Get a list of values for the named key in the named section.
        @param section The section name to find the key in.
        @param key The key name to find the list of values for.
        @returns Returns a list, possibly empty, of values.
        '''
        if(not self.__have_file):
            raise Exception(self.__no_file)
        values = []
        if(self.__data['sections'].get(section)):
            key_values = self.__data['sections'][section].get(key)
            if(key_values):
                for value in key_values:
                    values.append(value)
        return values
