''' @file examples/basics/trace.py
@brief Demonstrates how to display a trace of the parser's
path through the parse tree.

Tracing my generate a lot of output. It may be advantagous to
pipe stdout to an alternate location for more casual perusal.
For example, if using linux:
> python3 %examples/basics/trace.py | less
or
> python3 %examples/basics/trace.py > /tmp/trace<br>
> vi /tmp/trace
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
from apg_py.lib.trace import Trace
from apg_py.api.api import Api

title = '''Demonstrate the display a trace of the parser's path
through the parse tree.
Tracing my generate a lot of output. It may be advantagous to
pipe stdout to an alternate location for more casual perusal.
For example, if using linux:
python3 examples/trace.py | less
'''
print()
print(title)


float = '''float    = sign decimal exponent
sign     = ["+" / "-"]
decimal  = integer [dot fraction]
           / dot fraction
integer  = 1*%d48-57
dot      = "."
fraction = *%d48-57
exponent = ["e" esign exp]
esign    = ["+" / "-"]
exp      = 1*%d48-57
'''
bad_float = '''float    = sign decimal exponent
sign     = ["+" / "-"]
decimal  = integer [dot fraction]
           / dot fraction
integer  = 1*%d48-57
dot      = ","
fraction = *%d48-57
exponent = ["e" esign exp]
esign    = ["+" / "-"]
exp      = 1*%d48-57
'''

# trace with error
api = Api()
grammar = api.generate(float)
if(api.errors):
    # report any errors
    print('\n1) Grammar Errors')
    print(api.display_errors())
else:
    parser = Parser(grammar)
    # trace using ASCII characters when possible, otherwise decimal digits
    trace = Trace(parser, mode='dc')
    input_string = '-123,456789E-10'
    result = parser.parse(utils.string_to_tuple(input_string))
    print()
    print('\n1) Parser Result - fails on bad input ', end='')
    print('(input string has comma instead of period)')
    print(result)

grammar = api.generate(bad_float)
if(api.errors):
    # report any errors
    print('\n1) Grammar Errors')
    print(api.display_errors())
else:
    parser = Parser(grammar)
    # trace using ASCII characters when possible, otherwise decimal digits
    trace = Trace(parser, mode='dc')
    input_string = '-123.456789E-10'
    result = parser.parse(utils.string_to_tuple(input_string))
    print()
    print('\n2) Parser Result - fails on bad grammar ', end='')
    print('(dot is defined as a comma instead of period)')
    print(result)
