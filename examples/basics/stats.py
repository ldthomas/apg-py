''' @file examples/basics/stats.py
@brief Demonstrates how to display the parser's statistics.

Demonstrate the display of the parser's statistics.
Displays a count of how many nodes of each kind were hit and how many times.
Also displays how many times each rule and UDT name is hit.
Note that operators and rule/UDT names that have
a 0(zero) hit count are not displayed.
'''
import sys
import os
# add the current working directory to the path
# DO NOT MOVE THE FOLLOWING STATEMENT
# if using autopep8 formatter, for example, set argument '--ignore=E402'
sys.path.append(os.getcwd())
from apg_py.lib import utilities as utils
from apg_py.lib import identifiers as id
from apg_py.lib.parser import Parser
from apg_py.lib.stats import Stats
from apg_py.api.api import Api

title = '''Demonstrate the display of the parser's statistics.
Displays a count of how many nodes of each kind were hit and how many times.
Also displays how many times each rule and UDT name is hit.
Note that operators and rule/UDT names that have
a 0(zero) hit count are not displayed.
'''
print()
print(title)


def udt_sign(cbData):
    # matches '+', '-' or empty string
    cbData['phrase_length'] = 0
    cbData['state'] = id.EMPTY
    if(cbData['phrase_index'] < cbData['sub_end']):
        char = cbData['input'][cbData['phrase_index']]
        if(char == 43 or char == 45):
            cbData['phrase_length'] = 1
            cbData['state'] = id.MATCH


def udt_integer(cbData):
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


float = '''float = sign decimal exponent
sign = e_sign ;["+" / "-"]
decimal = integer [dot fraction]
        / dot fraction
integer = u_integer; 1*%d48-57
dot = "."
fraction = *digit
exponent = ["e" esign exp]
esign = ["+" / "-"]
exp = 1*digit
digit = %d48-57
'''
anbncn = 'S = &(A !bb) 1*aa B !cc\n'
anbncn += 'A = aa [A] bb\n'
anbncn += 'B = bb [B] cc\n'
anbncn += 'aa = "a"\n'
anbncn += 'bb = "b"\n'
anbncn += 'cc = "c"\n'

# UDT stats
api = Api()
grammar = api.generate(float)
if(api.errors):
    # report any errors
    print('\n1) Grammar Errors')
    print(api.display_errors())
else:
    # use the grammar object to parse an input string
    # input string must be a tuple of positive integers
    parser = Parser(grammar)
    stats = Stats(parser)
    parser.add_callbacks({'e_sign': udt_sign, 'u_integer': udt_integer})
    input_string = '-123.456789E-10'
    result = parser.parse(utils.string_to_tuple(input_string))
    print('\n1) Parser Result - floating point number with UDTs')
    print(result)
    stats.display()

# look ahead stats
grammar = api.generate(anbncn)
if(api.errors):
    # report any errors
    print('\n2) Grammar Errors')
    print(api.display_errors())
else:
    # use the grammar object to parse an input string
    # input string must be a tuple of positive integers
    parser = Parser(grammar)
    stats = Stats(parser)
    input_string = 'aaaabbbbcccc'
    result = parser.parse(utils.string_to_tuple(input_string))
    print('\n2) Parser Result - grammar with look ahead operators ', end='')
    print('&(AND) and !(NOT)')
    print(result)
    stats.display()
