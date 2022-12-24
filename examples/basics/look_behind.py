''' @file examples/basics/look_behind.py
@brief Demonstration of using the look behind operators.

A demonstration of the positive (&&) and negative(!!)
look behind operators.
<br>*Note that UDT and back referencing operators are not allowed in
look behind mode.*
<br>Included is a demonstration of using anchors,
operators that match only the beginning and ending positions
of the input string.
'''
import sys
import os
# add the current working directory to the path
# DO NOT MOVE THE FOLLOWING STATEMENT
# if using autopep8 formatter, for example, set argument '--ignore=E402'
sys.path.append(os.getcwd())
from apg_py.lib import utilities as utils
from apg_py.lib.parser import Parser
from apg_py.lib.trace import Trace
from apg_py.api.api import Api

title = '''A demonstration of the positive (&&) and negative(!!)
look behind operators. Included is a demonstration of using anchors,
operators that match only the beginning and ending positions
of the input string.
'''
print()
print(title)

# construct the grammar object
api = Api()
syntax = '''line = &&line-begin text line-end
line-begin = (%^ / %d10)
line-end = (%$ / %d10)
text = 1*(%d32 / %d97-122 / %d65-90 / %d48-57)
'''
input_string = 'first line\nsecond line'
grammar = api.generate(syntax)
if(api.errors):
    # report any errors
    print('\nGrammar Errors')
    print(api.display_errors())
else:
    # the first line
    parser = Parser(grammar)
    result = parser.parse(
        utils.string_to_tuple(input_string),
        sub_begin=0,
        sub_length=11)
    print('\n1) Parse the first line, begins at the beginning ', end='')
    print('of the input string.')
    print(result)

    # the second line
    result = parser.parse(
        utils.string_to_tuple(input_string),
        sub_begin=11,
        sub_length=11)
    print('\n2) Parse the second line, ends at the end ', end='')
    print('of the input string.')
    print(result)

    # not a line
    result = parser.parse(
        utils.string_to_tuple(input_string),
        sub_begin=1,
        sub_length=10)
    print('\n3) Parse some text that does not begin ', end='')
    print('at the beginning of a line.')
    print(result)

# negative look behind
syntax = '''line = !!crlf text line-end
crlf = %d13.10
line-end = (%$ / %d10)
text = 1*(%d32 / %d97-122 / %d65-90 / %d48-57)
'''
input_string = '\r\nfirst line\nsecond line'
grammar = api.generate(syntax)
if(api.errors):
    # report any errors
    print('\nGrammar Errors')
    print(api.display_errors())
else:
    # the first line
    parser = Parser(grammar)
    # trace = Trace(parser, mode='dc')
    result = parser.parse(
        utils.string_to_tuple(input_string),
        sub_begin=2,
        sub_length=10)
    print('\n4) First line may not be preceeded by CRLF.')
    print(result)

    # the second line
    result = parser.parse(
        utils.string_to_tuple(input_string),
        sub_begin=13,
        sub_length=11)
    print('\n5) Second line is NOT preceeded by CRLF - OK')
    print(result)
