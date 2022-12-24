''' @file examples/basics/substrings.py
@brief Demonstrate parsing substrings.
Often, expecially as used by the pattern-matching engine
@ref exp.py, one needs to parse only a sub-string of
the entire input string.
Here this is explicitly demonstrated.
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

title = '''Demonstrate the parsing of substrings of the full input string.
'''
print()
print(title)

abnf_syntax = 'S = "a" S / "y"\n'
# abnf_syntax_strict = 'S = "a" S / "y"\r\n'
input_string = '***aaay***'
beg = 3
len = 4
print('The grammar:', end=' ')
print(abnf_syntax)
print('The full input string:', end=' ')
print(input_string)
print('The sub string:', end=' ')
print(input_string[beg:beg + len])

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
    result = parser.parse(
        utils.string_to_tuple(input_string),
        sub_begin=beg,
        sub_length=len)
    print('\n1) Parser Result')
    print(result)
