''' @file examples/basics/parsing_basics.py
@brief Simple construction of a grammar object and parser.

A simple demonstration of the basics.
Generate a grammar object from an ABNF grammar syntax,
then use that object to parse an input string that matches the grammar.
'''
import sys
import os
# add the current working directory to the path
# DO NOT MOVE THE FOLLOWING STATEMENT
# if using autopep8 formatter, for example, set argument '--ignore=E402'
sys.path.append(os.getcwd())
from apg_py.lib import utilities as utils
from apg_py.lib.parser import Parser
from apg_py.api.api import Api

title = '''A simple demonstration of parsing basics.
Generate a grammar object from an ABNF grammar syntax.
Use the grammar object to parse an input string that matches the grammar.
'''
print()
print(title)

abnf_syntax = 'S = "a" S / "y"\n'
abnf_syntax_strict = 'S = "a" S / "y"\r\n'
input_string = 'aaay'

# construct the grammar object
api = Api()
grammar = api.generate(abnf_syntax)
if(api.errors):
    # report any errors
    print('\n1) Grammar Errors')
    print(api.display_errors())
else:
    # use the grammar object to parse an input string
    # input string must be a tuple of positive integers
    parser = Parser(grammar)
    result = parser.parse(utils.string_to_tuple(input_string))
    print('\n1) Parser Result - correct grammar')
    print(result)

# fails because of incorrect line end with strict ABNF
grammar = api.generate(abnf_syntax, strict=True)
if(api.errors):
    print('\n2) Grammar Errors - strict specified but line ends not CRLF')
    print(api.display_errors())
else:
    parser = Parser(grammar)
    result = parser.parse(utils.string_to_tuple(input_string))
    print('\n2) Parser Result')
    print(result)

# strict ABNF succeeds because grammar syntax is strictly ABNF
grammar = api.generate(abnf_syntax_strict, strict=True)
if(api.errors):
    print('\n3) Grammar Errors')
    print(api.display_errors())
else:
    parser = Parser(grammar)
    result = parser.parse(utils.string_to_tuple(input_string))
    print('\n3) Parser Result - strict specification succeeds')
    print(result)
